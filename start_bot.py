#!/usr/bin/env python3
"""
Bot de Telegram para Doblaje de Videos - Versión 24/7
"""
import os
import sys
import signal
import time
from telegram_bot import TelegramVoiceDubbingBot

def signal_handler(sig, frame):
    print('\n🛑 Deteniendo bot...')
    sys.exit(0)

def main():
    print("🎬 INICIANDO BOT DE DOBLAJE 24/7")
    print("=" * 50)
    
    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    while True:
        try:
            print("🚀 Iniciando bot...")
            bot = TelegramVoiceDubbingBot()
            bot.run()
            
        except KeyboardInterrupt:
            print("\n👋 Bot detenido por el usuario")
            break
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Reiniciando en 10 segundos...")
            time.sleep(10)
            continue

if __name__ == "__main__":
    main()