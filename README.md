# 🎬 Bot de Telegram para Doblaje de Videos

Bot completo que dobla videos a diferentes idiomas manteniendo la voz original usando IA.

## 🚀 Características

- **Transcripción automática** con Whisper (OpenAI)
- **Detección de múltiples hablantes** con pyannote.audio
- **Traducción automática** con Google Translate
- **Clonación de voz** con TTS (Coqui)
- **Procesamiento de video** completo
- **Interfaz de Telegram** intuitiva

## 📋 Idiomas Soportados

- Español, Inglés, Francés, Alemán, Italiano
- Portugués, Ruso, Japonés, Coreano, Chino

## ⚡ Instalación Rápida

```bash
# Clonar y entrar al directorio
git clone <repo>
cd telegram-voice-dubbing-bot

# Instalar todo automáticamente
chmod +x install.sh
bash install.sh

# Ejecutar el bot
python run.py
```

## 🔧 Instalación Manual

```bash
# Instalar dependencias del sistema
apt-get update
apt-get install -y ffmpeg espeak espeak-data libespeak1 libespeak-dev

# Instalar dependencias de Python
pip install -r requirements.txt

# Descargar modelo de Whisper
python -c "import whisper; whisper.load_model('base')"
```

## 🎯 Uso del Bot

1. **Iniciar**: `/start`
2. **Enviar video** (máx. 50MB, 5 min)
3. **Seleccionar idioma** de destino
4. **Esperar procesamiento**
5. **Recibir video doblado**

## 📁 Estructura del Proyecto

```
├── telegram_bot.py      # Bot principal
├── voice_processor.py   # Procesamiento de voz
├── audio_mixer.py       # Mezclado de audio
├── utils.py            # Utilidades
├── config.py           # Configuración
├── requirements.txt    # Dependencias
├── install.sh         # Instalación automática
└── run.py             # Ejecutor principal
```

## ⚙️ Configuración

Edita `config.py` para:
- Cambiar token del bot
- Ajustar límites de archivo
- Modificar modelos de IA
- Agregar idiomas

## 🔒 Límites

- **Tamaño máximo**: 50MB
- **Duración máxima**: 5 minutos
- **Formatos soportados**: MP4, AVI, MOV

## 🛠️ Comandos del Bot

- `/start` - Mensaje de bienvenida
- `/help` - Ayuda detallada
- `/languages` - Ver idiomas soportados

## 🚨 Solución de Problemas

### Error de dependencias
```bash
bash install.sh
```

### Error de memoria
- Usar videos más cortos
- Cambiar modelo Whisper a "tiny"

### Error de pyannote
- Registrarse en Hugging Face
- Aceptar términos del modelo

## 📝 Notas Técnicas

- **Whisper**: Transcripción de audio
- **pyannote.audio**: Separación de hablantes
- **Google Translate**: Traducción de texto
- **Coqui TTS**: Clonación de voz
- **MoviePy**: Procesamiento de video

## 🎭 Flujo de Procesamiento

1. **Descarga** del video
2. **Extracción** de audio
3. **Transcripción** con Whisper
4. **Detección** de hablantes
5. **Traducción** del texto
6. **Clonación** de voz
7. **Combinación** de segmentos
8. **Reemplazo** de audio en video
9. **Envío** del resultado