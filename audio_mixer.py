import librosa
import soundfile as sf
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip

class AudioMixer:
    def __init__(self):
        pass

    def combine_segments(self, segments, original_duration, output_path):
        """Combinar segmentos de audio procesados"""
        try:
            # Crear audio silencioso de la duración original
            sample_rate = 22050
            final_audio = np.zeros(int(original_duration * sample_rate))
            
            for segment in segments:
                if 'audio_file' not in segment:
                    continue
                    
                try:
                    # Cargar audio del segmento
                    audio, sr = librosa.load(segment['audio_file'], sr=sample_rate)
                    
                    # Calcular posiciones en el audio final
                    start_sample = int(segment['start'] * sample_rate)
                    end_sample = int(segment['end'] * sample_rate)
                    segment_duration = end_sample - start_sample
                    
                    # Ajustar duración del audio generado
                    if len(audio) > segment_duration:
                        audio = audio[:segment_duration]
                    elif len(audio) < segment_duration:
                        audio = np.pad(audio, (0, segment_duration - len(audio)))
                    
                    # Insertar en el audio final
                    if start_sample + len(audio) <= len(final_audio):
                        final_audio[start_sample:start_sample + len(audio)] = audio
                        
                except Exception as e:
                    print(f"Error procesando segmento: {str(e)}")
                    continue
            
            # Guardar audio final
            sf.write(output_path, final_audio, sample_rate)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error combinando segmentos: {str(e)}")

    def replace_video_audio(self, video_path, new_audio_path, output_path):
        """Reemplazar audio del video"""
        try:
            # Cargar video original
            video = VideoFileClip(video_path)
            
            # Cargar nuevo audio
            new_audio = AudioFileClip(new_audio_path)
            
            # Ajustar duración del audio al video
            if new_audio.duration > video.duration:
                new_audio = new_audio.subclip(0, video.duration)
            elif new_audio.duration < video.duration:
                # Extender audio con silencio si es necesario
                pass
            
            # Combinar video con nuevo audio
            final_video = video.set_audio(new_audio)
            
            # Exportar video final
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Limpiar recursos
            video.close()
            new_audio.close()
            final_video.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error reemplazando audio del video: {str(e)}")

    def extract_voice_sample(self, audio_path, start_time=0, duration=10):
        """Extraer muestra de voz para clonación"""
        try:
            audio, sr = librosa.load(audio_path, offset=start_time, duration=duration)
            
            # Normalizar audio
            audio = librosa.util.normalize(audio)
            
            # Guardar muestra
            sample_path = "temp/voice_sample.wav"
            sf.write(sample_path, audio, sr)
            
            return sample_path
            
        except Exception as e:
            raise Exception(f"Error extrayendo muestra de voz: {str(e)}")