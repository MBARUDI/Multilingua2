"""
Configurações do Assistente de Voz Multiidiomas
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ===== CONFIGURAÇÕES DE ÁUDIO =====
AUDIO_CONFIG = {
    'sample_rate': 16000,
    'channels': 1,
    'format': 'int16',
    'duration': 30,  # segundos máximos por gravação
    'threshold': 1000,  # limiar de silêncio
}

# Diretório para armazenar arquivos de áudio
AUDIO_STORAGE_DIR = os.path.join(os.getcwd(), 'audio_storage')
os.makedirs(AUDIO_STORAGE_DIR, exist_ok=True)

# ===== CONFIGURAÇÕES DE RECONHECIMENTO DE FALA =====
SPEECH_RECOGNITION_CONFIG = {
    'language': 'pt-BR',
    'timeout': 10,
    'phrase_time_limit': 30,
}

# ===== CONFIGURAÇÕES DE IA =====
AI_CONFIG = {
    'model': 'groq',  # 'openai' ou 'groq'
    'temperature': 0.7,
    'max_tokens': 500,
    'top_p': 0.95,
}

# ===== CONFIGURAÇÕES DE SÍNTESE DE FALA =====
TTS_CONFIG = {
    'engine': 'pyttsx3',  # 'pyttsx3', 'google', ou 'openai'
    'language': 'pt-br',
    'rate': 150,  # velocidade
    'volume': 0.9,  # volume (0.0 - 1.0)
    'voice_variant': 'female',  # 'male' ou 'female'
}

# ===== CHAVES DE API =====
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')

# ===== IDIOMAS SUPORTADOS =====
SUPPORTED_LANGUAGES = {
    'pt': {'name': 'Português', 'code': 'pt-BR'},
    'en': {'name': 'Inglês', 'code': 'en-US'},
    'es': {'name': 'Espanhol', 'code': 'es-ES'},
    'fr': {'name': 'Francês', 'code': 'fr-FR'},
    'de': {'name': 'Alemão', 'code': 'de-DE'},
    'it': {'name': 'Italiano', 'code': 'it-IT'},
    'ja': {'name': 'Japonês', 'code': 'ja-JP'},
    'zh': {'name': 'Chinês', 'code': 'zh-CN'},
}

# ===== CONTEXTO DO ASSISTENTE =====
ASSISTANT_CONFIG = {
    'name': 'ARIA',
    'personality': 'amigável, prestativo e inteligente',
    'max_context_length': 5,  # número de mensagens anteriores a manter
    'auto_detect_language': True,  # detectar idioma automaticamente
}

# ===== LOGGING =====
LOG_DIR = os.path.join(os.getcwd(), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'filename': os.path.join(LOG_DIR, 'assistant.log'),
}
