#!/usr/bin/env python3
import sys
print("🔧 Verificando imports...")

try:
    import telegram
    print("✅ telegram OK")
except ImportError as e:
    print(f"❌ telegram: {e}")

try:
    import whisper
    print("✅ whisper OK")
except ImportError as e:
    print(f"❌ whisper: {e}")

try:
    from google_trans_new import google_translator
    print("✅ google_trans_new OK")
except ImportError as e:
    print(f"❌ google_trans_new: {e}")

try:
    import pyttsx3
    print("✅ pyttsx3 OK")
except ImportError as e:
    print(f"❌ pyttsx3: {e}")

try:
    import librosa
    print("✅ librosa OK")
except ImportError as e:
    print(f"❌ librosa: {e}")

try:
    import soundfile
    print("✅ soundfile OK")
except ImportError as e:
    print(f"❌ soundfile: {e}")

try:
    from moviepy.editor import VideoFileClip
    print("✅ moviepy OK")
except ImportError as e:
    print(f"❌ moviepy: {e}")

print("\n🚀 Iniciando bot básico...")
from config import TELEGRAM_TOKEN
print(f"Token configurado: {TELEGRAM_TOKEN[:10]}...")