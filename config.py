import os

# Token del bot de Telegram
TELEGRAM_TOKEN = "8195405662:AAE6z92H7iz8H6BJB02uhyoHfjXYtXQvj38"

# Configuración de directorios
TEMP_DIR = "temp"
OUTPUT_DIR = "output"

# Configuración de modelos
WHISPER_MODEL = "base"  # base, small, medium, large
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

# Idiomas soportados
SUPPORTED_LANGUAGES = {
    'es': 'español',
    'en': 'english', 
    'fr': 'français',
    'de': 'deutsch',
    'it': 'italiano',
    'pt': 'português',
    'ru': 'русский',
    'ja': '日本語',
    'ko': '한국어',
    'zh': '中文'
}

# Límites
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_DURATION = 300  # 5 minutos