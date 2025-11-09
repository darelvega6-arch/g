#!/bin/bash
echo "Instalando dependencias del sistema..."
apt-get update
apt-get install -y ffmpeg espeak espeak-data libespeak1 libespeak-dev

echo "Instalando dependencias de Python..."
pip install -r requirements.txt

echo "Descargando modelo de Whisper..."
python -c "import whisper; whisper.load_model('base')"

echo "Configurando pyannote.audio..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo "¡Instalación completada!"