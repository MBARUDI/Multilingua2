"""
Módulo de Síntese de Fala (TTS)
Responsável pela conversão de texto em fala expressiva
"""
import logging
import os
from config import TTS_CONFIG, LOG_CONFIG, SUPPORTED_LANGUAGES

# Tentar inicializar pyttsx3
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except Exception as e:
    PYTTSX3_AVAILABLE = False
    logger_temp = logging.getLogger(__name__)
    logger_temp.warning(f"pyttsx3 não disponível: {str(e)}")

# Configurar logging
logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger(__name__)


class TextToSpeech:
    """Classe para síntese de fala expressiva"""

    def __init__(self):
        self.engine = None
        self.rate = TTS_CONFIG['rate']
        self.volume = TTS_CONFIG['volume']
        self.language = TTS_CONFIG['language']
        self.voice_variant = TTS_CONFIG['voice_variant']
        
        if PYTTSX3_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                # Configurar engine
                self._configure_engine()
            except Exception as e:
                logger.error(f"Erro ao inicializar pyttsx3: {str(e)}")
                self.engine = None
                logger.warning("TTS será desabilitado nesta sessão")
        else:
            logger.warning("pyttsx3 não disponível, TTS será simulado")

    def _configure_engine(self):
        """Configura o motor TTS"""
        if self.engine is None:
            return
            
        try:
            # Definir taxa de fala
            self.engine.setProperty('rate', self.rate)

            # Definir volume
            self.engine.setProperty('volume', self.volume)

            # Selecionar voz
            self._set_voice()

            logger.info("Motor TTS configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar TTS: {str(e)}")
            self.engine = None

    def _set_voice(self):
        """Define a voz do assistente"""
        if self.engine is None:
            return
            
        try:
            voices = self.engine.getProperty('voices')

            if len(voices) > 0:
                if self.voice_variant == 'female' and len(voices) > 1:
                    self.engine.setProperty('voice', voices[1].id)
                else:
                    self.engine.setProperty('voice', voices[0].id)

                logger.info(f"Voz definida: {self.voice_variant}")
        except Exception as e:
            logger.error(f"Erro ao definir voz: {str(e)}")

    def speak(self, text, lang_code='pt'):
        """
        Converte texto em fala e reproduz

        Args:
            text (str): Texto para converter em fala
            lang_code (str): Código do idioma

        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        try:
            if not text or len(text.strip()) == 0:
                logger.warning("Texto vazio para síntese")
                return False

            logger.info(f"Sintetizando: {text[:100]}...")
            print(f"🔊 Respondendo: {text}")

            # Se engine não está disponível, apenas simular
            if self.engine is None:
                logger.warning("TTS não disponível, apenas exibindo texto")
                return True

            # Reproduzir fala
            self.engine.say(text)
            self.engine.runAndWait()

            logger.info("Síntese concluída com sucesso")
            return True

        except Exception as e:
            logger.error(f"Erro ao sintetizar fala: {str(e)}")
            print(f"❌ Erro na síntese: {str(e)}")
            return False

    def speak_with_expression(self, text, emotion='neutral', lang_code='pt'):
        """
        Reproduz fala com expressão (variando velocidade e volume)

        Args:
            text (str): Texto para converter em fala
            emotion (str): Emoção ('happy', 'sad', 'angry', 'neutral', 'excited')
            lang_code (str): Código do idioma

        Returns:
            bool: True se bem-sucedido
        """
        try:
            original_rate = self.engine.getProperty('rate')
            original_volume = self.engine.getProperty('volume')

            # Ajustar para expressar emoção
            if emotion == 'happy':
                self.engine.setProperty('rate', self.rate + 20)
                self.engine.setProperty('volume', self.volume)
                logger.info("Emoção: Feliz")
            elif emotion == 'sad':
                self.engine.setProperty('rate', self.rate - 20)
                self.engine.setProperty('volume', self.volume - 0.1)
                logger.info("Emoção: Triste")
            elif emotion == 'angry':
                self.engine.setProperty('rate', self.rate + 30)
                self.engine.setProperty('volume', min(self.volume + 0.2, 1.0))
                logger.info("Emoção: Zangado")
            elif emotion == 'excited':
                self.engine.setProperty('rate', self.rate + 40)
                self.engine.setProperty('volume', min(self.volume + 0.1, 1.0))
                logger.info("Emoção: Animado")
            else:
                # neutral
                self.engine.setProperty('rate', self.rate)
                self.engine.setProperty('volume', self.volume)

            print(f"🔊 Respondendo (😊 {emotion}): {text}")
            self.engine.say(text)
            self.engine.runAndWait()

            # Restaurar configurações originais
            self.engine.setProperty('rate', original_rate)
            self.engine.setProperty('volume', original_volume)

            return True

        except Exception as e:
            logger.error(f"Erro na síntese expressiva: {str(e)}")
            return False

    def save_to_file(self, text, filename='output.mp3', lang_code='pt'):
        """
        Salva a síntese de fala em arquivo

        Args:
            text (str): Texto para converter
            filename (str): Nome do arquivo de saída
            lang_code (str): Código do idioma

        Returns:
            bool: True se bem-sucedido
        """
        try:
            filepath = os.path.join('audio_storage', filename)
            logger.info(f"Salvando síntese em: {filepath}")

            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()

            logger.info(f"Síntese salva com sucesso: {filename}")
            print(f"✓ Áudio salvo: {filename}")
            return True

        except Exception as e:
            logger.error(f"Erro ao salvar síntese: {str(e)}")
            print(f"❌ Erro ao salvar: {str(e)}")
            return False

    def set_rate(self, rate):
        """Define a taxa de fala (velocidade)"""
        try:
            self.rate = rate
            self.engine.setProperty('rate', rate)
            logger.info(f"Taxa de fala alterada para: {rate}")
        except Exception as e:
            logger.error(f"Erro ao definir taxa: {str(e)}")

    def set_volume(self, volume):
        """Define o volume (0.0 - 1.0)"""
        try:
            self.volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', self.volume)
            logger.info(f"Volume alterado para: {self.volume}")
        except Exception as e:
            logger.error(f"Erro ao definir volume: {str(e)}")

    def get_available_voices(self):
        """Retorna vozes disponíveis"""
        try:
            voices = self.engine.getProperty('voices')
            voice_info = []
            for voice in voices:
                voice_info.append({
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages,
                })
            return voice_info
        except Exception as e:
            logger.error(f"Erro ao obter vozes: {str(e)}")
            return []

    def stop(self):
        """Para a síntese em andamento"""
        try:
            self.engine.stop()
            logger.info("Síntese interrompida")
        except Exception as e:
            logger.error(f"Erro ao parar síntese: {str(e)}")
