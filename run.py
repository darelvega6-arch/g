#!/usr/bin/env python3
"""
Bot de Telegram para Doblaje de Videos
Ejecutar con: python run.py
"""

import sys
import os

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramVoiceDubbingBot

def main():
    print("🎬 Iniciando Bot de Doblaje de Videos...")
    print("🔧 Verificando dependencias...")
    
    try:
        # Verificar imports críticos
        import whisper
        import telegram
        from TTS.api import TTS
        print("✅ Todas las dependencias están instaladas")
        
        # Iniciar bot
        bot = TelegramVoiceDubbingBot()
        bot.run()
        
    except ImportError as e:
        print(f"❌ Error: Falta instalar dependencias - {e}")
        print("💡 Ejecuta: bash install.sh")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Bot detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()