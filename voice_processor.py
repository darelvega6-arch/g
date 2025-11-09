import whisper
from google_trans_new import google_translator
import pyttsx3
import librosa
import soundfile as sf
import numpy as np
from config import WHISPER_MODEL

class VoiceProcessor:
    def __init__(self):
        self.whisper_model = whisper.load_model(WHISPER_MODEL)
        self.translator = google_translator()
        self.tts = pyttsx3.init()
        
        # Separación de hablantes deshabilitada por simplicidad
        self.speaker_pipeline = None

    def transcribe_audio(self, audio_path):
        """Transcribir audio con Whisper"""
        try:
            result = self.whisper_model.transcribe(audio_path)
            return {
                'text': result['text'],
                'language': result['language'],
                'segments': result['segments']
            }
        except Exception as e:
            raise Exception(f"Error en transcripción: {str(e)}")

    def detect_speakers(self, audio_path):
        """Detectar diferentes hablantes"""
        if not self.speaker_pipeline:
            return None
        
        try:
            diarization = self.speaker_pipeline(audio_path)
            speakers = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                speakers.append({
                    'start': turn.start,
                    'end': turn.end,
                    'speaker': speaker
                })
            return speakers
        except Exception as e:
            print(f"Error en detección de hablantes: {str(e)}")
            return None

    def translate_text(self, text, target_language):
        """Traducir texto"""
        try:
            translated = self.translator.translate(text, lang_tgt=target_language)
            return translated
        except Exception as e:
            raise Exception(f"Error en traducción: {str(e)}")

    def clone_voice_and_speak(self, text, reference_audio_path, output_path, target_language='es'):
        """Generar audio con TTS"""
        try:
            # Configurar TTS
            self.tts.setProperty('rate', 150)
            self.tts.setProperty('volume', 0.9)
            
            # Generar audio
            self.tts.save_to_file(text, output_path)
            self.tts.runAndWait()
            return output_path
        except Exception as e:
            raise Exception(f"Error en generación de voz: {str(e)}")

    def process_segments(self, segments, reference_audio, target_language):
        """Procesar segmentos de audio individualmente"""
        processed_segments = []
        
        for i, segment in enumerate(segments):
            try:
                # Traducir texto del segmento
                translated_text = self.translate_text(segment['text'], target_language)
                
                # Crear archivo temporal para el segmento
                segment_output = f"temp/segment_{i}.wav"
                
                # Generar audio con voz clonada
                self.clone_voice_and_speak(
                    translated_text, 
                    reference_audio, 
                    segment_output, 
                    target_language
                )
                
                processed_segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'original_text': segment['text'],
                    'translated_text': translated_text,
                    'audio_file': segment_output
                })
                
            except Exception as e:
                print(f"Error procesando segmento {i}: {str(e)}")
                continue
                
        return processed_segments