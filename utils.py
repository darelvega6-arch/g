import os
import tempfile
from pathlib import Path
from moviepy.editor import VideoFileClip
import librosa
import soundfile as sf

def ensure_directories():
    """Crear directorios necesarios"""
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output", exist_ok=True)

def extract_audio_from_video(video_path):
    """Extraer audio de video"""
    try:
        video = VideoFileClip(video_path)
        audio_path = video_path.replace('.mp4', '.wav').replace('.avi', '.wav').replace('.mov', '.wav')
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video.close()
        return audio_path
    except Exception as e:
        raise Exception(f"Error extrayendo audio: {str(e)}")

def get_audio_duration(audio_path):
    """Obtener duración del audio"""
    try:
        y, sr = librosa.load(audio_path)
        return len(y) / sr
    except Exception as e:
        raise Exception(f"Error obteniendo duración: {str(e)}")

def cleanup_temp_files(*file_paths):
    """Limpiar archivos temporales"""
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass

def create_temp_file(suffix=".wav"):
    """Crear archivo temporal"""
    return tempfile.mktemp(suffix=suffix, dir="temp")