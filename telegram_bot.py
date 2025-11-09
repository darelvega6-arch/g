import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN, SUPPORTED_LANGUAGES, MAX_FILE_SIZE, MAX_DURATION
from voice_processor import VoiceProcessor
from audio_mixer import AudioMixer
from utils import *

class TelegramVoiceDubbingBot:
    def __init__(self):
        self.voice_processor = VoiceProcessor()
        self.audio_mixer = AudioMixer()
        self.user_sessions = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome_text = """
🎬 ¡Bienvenido al Bot de Doblaje de Videos! 🎬

Puedo doblar tus videos a diferentes idiomas manteniendo la voz original.

📋 Comandos disponibles:
/start - Mostrar este mensaje
/help - Ayuda detallada
/languages - Ver idiomas soportados
/process - Procesar un video

📤 Para empezar, envía un video (máx. 50MB, 5 min)
        """
        await update.message.reply_text(welcome_text)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """
🔧 Cómo usar el bot:

1️⃣ Envía un video (MP4, AVI, MOV)
2️⃣ Selecciona el idioma de destino
3️⃣ Espera el procesamiento
4️⃣ Recibe tu video doblado

⚙️ Características:
• Detección automática del idioma original
• Clonación de voz con IA
• Separación de múltiples hablantes
• Traducción automática
• Sincronización perfecta

⚠️ Límites:
• Tamaño máximo: 50MB
• Duración máxima: 5 minutos
        """
        await update.message.reply_text(help_text)

    async def languages_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /languages"""
        lang_text = "🌍 Idiomas soportados:\n\n"
        for code, name in SUPPORTED_LANGUAGES.items():
            lang_text += f"• {name} ({code})\n"
        await update.message.reply_text(lang_text)

    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar videos recibidos"""
        try:
            # Verificar tamaño del archivo
            if update.message.video.file_size > MAX_FILE_SIZE:
                await update.message.reply_text("❌ El archivo es demasiado grande (máx. 50MB)")
                return

            # Mostrar mensaje de procesamiento
            processing_msg = await update.message.reply_text("📥 Descargando video...")

            # Descargar video
            file = await context.bot.get_file(update.message.video.file_id)
            video_path = f"temp/{update.message.video.file_id}.mp4"
            await file.download_to_drive(video_path)

            # Extraer audio
            await processing_msg.edit_text("🎵 Extrayendo audio...")
            audio_path = extract_audio_from_video(video_path)

            # Verificar duración
            duration = get_audio_duration(audio_path)
            if duration > MAX_DURATION:
                cleanup_temp_files(video_path, audio_path)
                await processing_msg.edit_text("❌ El video es demasiado largo (máx. 5 minutos)")
                return

            # Transcribir audio
            await processing_msg.edit_text("🎤 Transcribiendo audio...")
            transcription = self.voice_processor.transcribe_audio(audio_path)

            # Guardar sesión del usuario
            user_id = update.effective_user.id
            self.user_sessions[user_id] = {
                'video_path': video_path,
                'audio_path': audio_path,
                'transcription': transcription,
                'duration': duration
            }

            # Mostrar idioma detectado y opciones
            detected_lang = transcription['language']
            lang_name = SUPPORTED_LANGUAGES.get(detected_lang, detected_lang)
            
            keyboard = []
            for code, name in SUPPORTED_LANGUAGES.items():
                if code != detected_lang:
                    keyboard.append([InlineKeyboardButton(name, callback_data=f"lang_{code}")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await processing_msg.edit_text(
                f"✅ Video procesado correctamente\n\n"
                f"🎯 Idioma detectado: {lang_name}\n"
                f"📝 Texto: {transcription['text'][:100]}...\n\n"
                f"🌍 Selecciona el idioma de destino:",
                reply_markup=reply_markup
            )

        except Exception as e:
            await update.message.reply_text(f"❌ Error procesando video: {str(e)}")

    async def handle_language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar selección de idioma"""
        query = update.callback_query
        await query.answer()

        try:
            user_id = update.effective_user.id
            if user_id not in self.user_sessions:
                await query.edit_message_text("❌ Sesión expirada. Envía un nuevo video.")
                return

            target_lang = query.data.replace("lang_", "")
            session = self.user_sessions[user_id]

            # Mostrar progreso
            await query.edit_message_text("🔄 Procesando doblaje...")

            # Extraer muestra de voz
            voice_sample = self.audio_mixer.extract_voice_sample(session['audio_path'])

            # Procesar segmentos
            progress_msg = await query.edit_message_text("🎭 Clonando voz y traduciendo...")
            
            segments = self.voice_processor.process_segments(
                session['transcription']['segments'],
                voice_sample,
                target_lang
            )

            # Combinar audio
            await query.edit_message_text("🎵 Combinando audio...")
            final_audio_path = "temp/final_audio.wav"
            self.audio_mixer.combine_segments(segments, session['duration'], final_audio_path)

            # Reemplazar audio del video
            await query.edit_message_text("🎬 Generando video final...")
            output_video = f"output/dubbed_{user_id}_{target_lang}.mp4"
            self.audio_mixer.replace_video_audio(
                session['video_path'],
                final_audio_path,
                output_video
            )

            # Enviar video doblado
            await query.edit_message_text("📤 Enviando video doblado...")
            
            with open(output_video, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=video_file,
                    caption=f"🎬 Video doblado al {SUPPORTED_LANGUAGES[target_lang]}"
                )

            await query.edit_message_text("✅ ¡Video doblado enviado correctamente!")

            # Limpiar archivos temporales
            cleanup_temp_files(
                session['video_path'],
                session['audio_path'],
                voice_sample,
                final_audio_path,
                output_video,
                *[seg.get('audio_file') for seg in segments if seg.get('audio_file')]
            )

            # Limpiar sesión
            del self.user_sessions[user_id]

        except Exception as e:
            await query.edit_message_text(f"❌ Error en el doblaje: {str(e)}")

    def run(self):
        """Ejecutar el bot"""
        ensure_directories()
        
        # Crear aplicación
        app = Application.builder().token(TELEGRAM_TOKEN).build()

        # Agregar handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("languages", self.languages_command))
        app.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        app.add_handler(CallbackQueryHandler(self.handle_language_selection, pattern="^lang_"))

        print("🤖 Bot iniciado. Presiona Ctrl+C para detener.")
        app.run_polling()

if __name__ == "__main__":
    bot = TelegramVoiceDubbingBot()
    bot.run()