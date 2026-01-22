"""
Módulo de Reconhecimento de Fala e Transcrição
Responsável pela transcrição de áudio em texto e detecção de idioma
"""
import logging
import speech_recognition as sr
from langdetect import detect, detect_langs
import numpy as np
from config import SPEECH_RECOGNITION_CONFIG, SUPPORTED_LANGUAGES, LOG_CONFIG

# Configurar logging
logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """Classe para reconhecimento de fala e transcrição"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000

    def transcribe_audio(self, audio_file_path=None, audio_data=None, language='pt-BR'):
        """
        Transcreve áudio para texto

        Args:
            audio_file_path (str): Caminho do arquivo de áudio
            audio_data: Dados de áudio em memória
            language (str): Código do idioma (ex: 'pt-BR', 'en-US')

        Returns:
            str: Texto transcrito
            str: Idioma detectado
        """
        try:
            if audio_file_path:
                with sr.AudioFile(audio_file_path) as source:
                    audio = self.recognizer.record(source)
            elif audio_data is not None:
                audio = sr.AudioData(
                    audio_data.tobytes(),
                    16000,
                    2
                )
            else:
                logger.error("Sem dados de áudio fornecidos")
                print("❌ Sem dados de áudio")
                return None, None

            print("🔄 Transcrevendo áudio...")
            logger.info("Iniciando transcrição")

            # Transcrever usando Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=language)

            logger.info(f"Transcrição bem-sucedida: {text}")
            print(f"✓ Transcrição: {text}")

            # Detectar idioma
            detected_language = self.detect_language(text)

            return text, detected_language

        except sr.UnknownValueError:
            logger.warning("Áudio não pôde ser entendido")
            print("❌ Não consegui entender o áudio")
            return None, None
        except sr.RequestError as e:
            logger.error(f"Erro na requisição de transcrição: {str(e)}")
            print(f"❌ Erro na transcrição: {str(e)}")
            return None, None
        except Exception as e:
            logger.error(f"Erro inesperado na transcrição: {str(e)}")
            print(f"❌ Erro: {str(e)}")
            return None, None

    def detect_language(self, text):
        """
        Detecta o idioma do texto

        Args:
            text (str): Texto para análise

        Returns:
            dict: Informações sobre o idioma detectado
        """
        try:
            if not text or len(text.strip()) < 3:
                return {'code': 'pt', 'name': 'Português', 'confidence': 0}

            # Detectar idioma
            lang_code = detect(text)
            probabilities = detect_langs(text)

            # Encontrar confiança
            confidence = 0
            for prob in probabilities:
                if prob.lang == lang_code:
                    confidence = prob.prob
                    break

            # Mapear código de idioma
            language_name = SUPPORTED_LANGUAGES.get(lang_code, {}).get('name', lang_code)

            result = {
                'code': lang_code,
                'name': language_name,
                'confidence': confidence,
                'probabilities': [(p.lang, p.prob) for p in probabilities[:3]]
            }

            logger.info(f"Idioma detectado: {lang_code} (confiança: {confidence:.2%})")
            return result

        except Exception as e:
            logger.error(f"Erro ao detectar idioma: {str(e)}")
            return {'code': 'pt', 'name': 'Português', 'confidence': 0}

    def transcribe_microphone(self, timeout=10, language='pt-BR'):
        """
        Grava do microfone e transcreve em tempo real

        Args:
            timeout (int): Tempo máximo de espera
            language (str): Código do idioma

        Returns:
            str: Texto transcrito
            str: Idioma detectado
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Escutando... (fale agora)")
                logger.info("Escutando do microfone")

                # Ajustar ruído ambiente
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # Gravar áudio
                audio = self.recognizer.listen(source, timeout=timeout)

            print("🔄 Transcrevendo...")
            text = self.recognizer.recognize_google(audio, language=language)

            logger.info(f"Transcrição do microfone: {text}")
            print(f"✓ Você disse: {text}")

            detected_language = self.detect_language(text)

            return text, detected_language

        except sr.UnknownValueError:
            logger.warning("Áudio não foi entendido")
            print("❌ Não consegui entender. Tente novamente.")
            return None, None
        except sr.RequestError as e:
            logger.error(f"Erro: {str(e)}")
            print(f"❌ Erro: {str(e)}")
            return None, None
        except Exception as e:
            logger.error(f"Erro: {str(e)}")
            print(f"❌ Erro: {str(e)}")
            return None, None

    def get_language_code(self, lang_name):
        """Obtém código de idioma a partir do nome"""
        for code, info in SUPPORTED_LANGUAGES.items():
            if info['name'].lower() == lang_name.lower():
                return info['code']
        return 'pt-BR'
