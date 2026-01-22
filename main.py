"""
Aplicativo Principal - Assistente de Voz Multiidiomas
Interface completa integrando todos os módulos
"""
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# Importar módulos
from audio_module import AudioRecorder
from speech_recognition_module import SpeechRecognizer
from ai_module import AIAssistant
from tts_module import TextToSpeech
from config import (
    LOG_CONFIG, SUPPORTED_LANGUAGES, ASSISTANT_CONFIG,
    AUDIO_STORAGE_DIR
)

# Configurar logging
logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger(__name__)


class VoiceAssistant:
    """Classe principal do assistente de voz"""

    def __init__(self):
        """Inicializa o assistente"""
        logger.info("=" * 50)
        logger.info("Iniciando Assistente de Voz Multiidiomas")
        logger.info("=" * 50)

        print("\n" + "=" * 60)
        print("🎙️  ARIA - Assistente de Voz Inteligente Multiidiomas")
        print("=" * 60)
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

        # Inicializar módulos
        try:
            print("🔧 Inicializando módulos...")
            self.audio_recorder = AudioRecorder()
            self.speech_recognizer = SpeechRecognizer()
            self.ai_assistant = AIAssistant()
            self.tts = TextToSpeech()

            print("✓ Todos os módulos inicializados com sucesso\n")
            logger.info("Todos os módulos inicializados")

            # Variáveis de controle
            self.current_language = 'pt'
            self.is_running = True
            self.conversation_count = 0

            # Saudação inicial
            self._greet_user()

        except Exception as e:
            logger.error(f"Erro ao inicializar: {str(e)}")
            print(f"❌ Erro ao inicializar: {str(e)}")
            sys.exit(1)

    def _greet_user(self):
        """Saudação inicial do assistente"""
        greeting = "Olá! Sou a ARIA, seu assistente de voz inteligente. Como posso ajudá-lo hoje?"
        print(f"🤖 {ASSISTANT_CONFIG['name']}: {greeting}\n")
        self.tts.speak_with_expression(greeting, emotion='happy', lang_code=self.current_language)

    def show_menu(self):
        """Exibe menu principal"""
        print("\n" + "=" * 60)
        print("📋 MENU PRINCIPAL")
        print("=" * 60)
        print("1. 🎤 Fazer pergunta (voz)")
        print("2. ⌨️  Escrever pergunta (texto)")
        print("3. 🌍 Mudar idioma")
        print("4. 📁 Ver histórico de áudios")
        print("5. 🔍 Ver informações do assistente")
        print("6. ❌ Sair")
        print("=" * 60 + "\n")

    def voice_input_mode(self):
        """Modo de entrada por voz"""
        print("\n🎤 MODO VOZ")
        print("-" * 40)

        try:
            # Gravar e transcrever
            _, audio_path = self.audio_recorder.record_audio_with_detection()

            if audio_path is None:
                print("❌ Falha ao gravar áudio")
                return

            # Transcrever
            user_text, detected_lang = self.speech_recognizer.transcribe_audio(
                audio_file_path=audio_path,
                language='pt-BR'
            )

            if user_text is None:
                self.tts.speak("Desculpe, não consegui entender. Tente novamente.", lang_code=self.current_language)
                return

            # Processar resposta
            self._process_and_respond(user_text, detected_lang)

        except Exception as e:
            logger.error(f"Erro no modo voz: {str(e)}")
            print(f"❌ Erro: {str(e)}")

    def text_input_mode(self):
        """Modo de entrada por texto"""
        print("\n⌨️  MODO TEXTO")
        print("-" * 40)

        try:
            user_text = input("💬 Você: ").strip()

            if not user_text:
                print("❌ Entrada vazia")
                return

            # Detectar idioma
            detected_lang_info = self.speech_recognizer.detect_language(user_text)

            # Processar resposta
            self._process_and_respond(user_text, detected_lang_info)

        except Exception as e:
            logger.error(f"Erro no modo texto: {str(e)}")
            print(f"❌ Erro: {str(e)}")

    def _process_and_respond(self, user_text, detected_lang):
        """Processa pergunta e gera resposta"""
        try:
            self.conversation_count += 1
            lang_code = detected_lang.get('code', 'pt') if isinstance(detected_lang, dict) else detected_lang

            # Log
            logger.info(f"[Pergunta {self.conversation_count}] {user_text}")
            logger.info(f"Idioma detectado: {lang_code}")

            # Gerar resposta
            response = self.ai_assistant.get_response(
                user_text,
                language=lang_code
            )

            # Exibir e reproduzir resposta
            print(f"\n🤖 {ASSISTANT_CONFIG['name']}: {response}\n")
            logger.info(f"[Resposta {self.conversation_count}] {response}")

            # Reproduzir resposta com expressão
            self._speak_response(response, user_text, lang_code)

        except Exception as e:
            logger.error(f"Erro ao processar resposta: {str(e)}")
            print(f"❌ Erro: {str(e)}")

    def _speak_response(self, response, user_text, lang_code):
        """Reproduz resposta com expressão apropriada"""
        try:
            # Detectar emoção apropriada baseada na pergunta e resposta
            emotion = self._detect_appropriate_emotion(user_text, response)
            self.tts.speak_with_expression(response, emotion=emotion, lang_code=lang_code)
        except Exception as e:
            logger.warning(f"Erro ao reproduzir com expressão, tentando sem: {str(e)}")
            self.tts.speak(response, lang_code=lang_code)

    def _detect_appropriate_emotion(self, question, response):
        """Detecta emoção apropriada para a resposta"""
        emotion = 'neutral'

        # Palavras-chave para alegria
        happy_keywords = ['ótimo', 'excelente', 'perfeito', 'adorei', 'gostei', 'feliz', 'sucesso']
        if any(word in response.lower() for word in happy_keywords):
            emotion = 'happy'

        # Palavras-chave para tristeza
        sad_keywords = ['desculp', 'infelizment', 'não posso', 'não consegui', 'problemas']
        if any(word in response.lower() for word in sad_keywords):
            emotion = 'sad'

        # Palavras-chave para animação
        excited_keywords = ['incrível', 'maravilhoso', 'fantástico', 'sensacional']
        if any(word in response.lower() for word in excited_keywords):
            emotion = 'excited'

        return emotion

    def change_language(self):
        """Muda o idioma do assistente"""
        print("\n🌍 MUDAR IDIOMA")
        print("-" * 40)
        print("Idiomas suportados:")

        for i, (code, info) in enumerate(SUPPORTED_LANGUAGES.items(), 1):
            print(f"{i}. {info['name']} ({code})")

        try:
            choice = input("\n✍️  Escolha um idioma (número): ").strip()
            idx = int(choice) - 1

            lang_list = list(SUPPORTED_LANGUAGES.items())
            if 0 <= idx < len(lang_list):
                self.current_language = lang_list[idx][0]
                lang_name = lang_list[idx][1]['name']
                print(f"✓ Idioma alterado para: {lang_name}")
                logger.info(f"Idioma alterado para: {self.current_language}")

                # Confirmação em voz
                self.tts.speak(
                    f"Idioma alterado para {lang_name}",
                    lang_code=self.current_language
                )
            else:
                print("❌ Opção inválida")

        except ValueError:
            print("❌ Entrada inválida")

    def show_audio_history(self):
        """Mostra histórico de áudios gravados"""
        print("\n📁 HISTÓRICO DE ÁUDIOS")
        print("-" * 40)

        audio_files = self.audio_recorder.list_audio_files()

        if not audio_files:
            print("Nenhum áudio gravado ainda.")
            return

        print(f"Total de arquivos: {len(audio_files)}\n")

        for i, filename in enumerate(audio_files[-10:], 1):
            info = self.audio_recorder.get_audio_info(filename)
            if info:
                print(f"{i}. {filename}")
                print(f"   ⏱️  Duração: {info['duration']:.1f}s | Tamanho: {info['file_size']/1024:.1f}KB")

    def show_info(self):
        """Mostra informações do assistente"""
        print("\n🔍 INFORMAÇÕES DO ASSISTENTE")
        print("-" * 40)
        print(f"Nome: {ASSISTANT_CONFIG['name']}")
        print(f"Personalidade: {ASSISTANT_CONFIG['personality']}")
        print(f"Idioma atual: {SUPPORTED_LANGUAGES.get(self.current_language, {}).get('name')}")
        print(f"Total de conversas: {self.conversation_count}")
        print(f"Histórico de mensagens: {self.ai_assistant.get_conversation_summary()}")
        print(f"Diretório de áudios: {AUDIO_STORAGE_DIR}")
        print(f"Log: {LOG_CONFIG['file']}")

    def run(self):
        """Executa o loop principal do assistente"""
        logger.info("Assistente iniciado")

        while self.is_running:
            try:
                self.show_menu()
                choice = input("✍️  Escolha uma opção: ").strip()

                if choice == '1':
                    self.voice_input_mode()
                elif choice == '2':
                    self.text_input_mode()
                elif choice == '3':
                    self.change_language()
                elif choice == '4':
                    self.show_audio_history()
                elif choice == '5':
                    self.show_info()
                elif choice == '6':
                    self._shutdown()
                    break
                else:
                    print("❌ Opção inválida. Tente novamente.")

            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupção detectada")
                self._shutdown()
                break
            except Exception as e:
                logger.error(f"Erro no loop principal: {str(e)}")
                print(f"❌ Erro: {str(e)}")

    def _shutdown(self):
        """Encerra o assistente"""
        print("\n" + "=" * 60)
        goodbye_msg = "Até logo! Foi um prazer conversar com você. 😊"
        print(f"🤖 {ASSISTANT_CONFIG['name']}: {goodbye_msg}")
        print("=" * 60 + "\n")

        try:
            self.tts.speak(goodbye_msg, lang_code=self.current_language)
        except:
            pass

        logger.info(f"Assistente encerrado. Total de conversas: {self.conversation_count}")
        self.is_running = False


def main():
    """Função principal"""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        logger.critical(f"Erro crítico: {str(e)}")
        print(f"❌ Erro crítico: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
