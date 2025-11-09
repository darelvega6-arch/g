import whisper
import torch
from pyannote.audio import Pipeline
from googletrans import Translator
from TTS.api import TTS
import librosa
import soundfile as sf
import numpy as np
from config import WHISPER_MODEL, TTS_MODEL

class VoiceProcessor:
    def __init__(self):
        self.whisper_model = whisper.load_model(WHISPER_MODEL)
        self.translator = Translator()
        self.tts = TTS(TTS_MODEL)
        
        # Inicializar pipeline de separación de hablantes
        try:
            self.speaker_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
        except:
            self.speaker_pipeline = None
            print("Advertencia: No se pudo cargar el modelo de separación de hablantes")

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
            translated = self.translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            raise Exception(f"Error en traducción: {str(e)}")

    def clone_voice_and_speak(self, text, reference_audio_path, output_path, target_language='es'):
        """Clonar voz y generar audio"""
        try:
            # Generar audio con voz clonada
            self.tts.tts_to_file(
                text=text,
                speaker_wav=reference_audio_path,
                language=target_language,
                file_path=output_path
            )
            return output_path
        except Exception as e:
            raise Exception(f"Error en clonación de voz: {str(e)}")

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