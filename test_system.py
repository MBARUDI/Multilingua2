"""
Versão Simplificada para Teste Rápido
Teste básico dos componentes sem dependências pesadas
"""
import sys


def test_audio_module():
    """Testa módulo de áudio"""
    print("\n" + "=" * 60)
    print("🎤 TESTANDO MÓDULO DE ÁUDIO")
    print("=" * 60)

    try:
        from audio_module import AudioRecorder
        recorder = AudioRecorder()
        print("✓ AudioRecorder inicializado")

        files = recorder.list_audio_files()
        print(f"✓ Arquivos de áudio: {len(files)} arquivos")

        if files:
            info = recorder.get_audio_info(files[0])
            print(f"✓ Informações obtidas: {info['filename']}")

        return True
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False


def test_speech_recognition():
    """Testa módulo de reconhecimento de fala"""
    print("\n" + "=" * 60)
    print("🎙️  TESTANDO RECONHECIMENTO DE FALA")
    print("=" * 60)

    try:
        from speech_recognition_module import SpeechRecognizer
        recognizer = SpeechRecognizer()
        print("✓ SpeechRecognizer inicializado")

        # Testar detecção de idioma
        lang = recognizer.detect_language("Olá, como você está?")
        print(f"✓ Idioma detectado: {lang['name']} ({lang['confidence']:.1%})")

        return True
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False


def test_ai_module():
    """Testa módulo de IA"""
    print("\n" + "=" * 60)
    print("🤖 TESTANDO MÓDULO DE IA")
    print("=" * 60)

    try:
        from ai_module import AIAssistant
        assistant = AIAssistant()
        print("✓ AIAssistant inicializado")

        response = assistant.get_response("Teste simples", language='pt')
        print(f"✓ Resposta gerada: {response[:50]}...")

        return True
    except Exception as e:
        print(f"⚠️  Aviso (pode ser falta de chave de API): {str(e)}")
        return False


def test_tts_module():
    """Testa módulo de síntese de fala"""
    print("\n" + "=" * 60)
    print("🔊 TESTANDO SÍNTESE DE FALA")
    print("=" * 60)

    try:
        from tts_module import TextToSpeech
        tts = TextToSpeech()
        print("✓ TextToSpeech inicializado")

        # Não reproduzir, apenas verificar
        voices = tts.get_available_voices()
        print(f"✓ Vozes disponíveis: {len(voices)}")

        return True
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False


def test_config():
    """Testa configurações"""
    print("\n" + "=" * 60)
    print("⚙️  TESTANDO CONFIGURAÇÕES")
    print("=" * 60)

    try:
        from config import (
            SUPPORTED_LANGUAGES, ASSISTANT_CONFIG,
            AUDIO_CONFIG, TTS_CONFIG, AI_CONFIG
        )

        print(f"✓ Assistente: {ASSISTANT_CONFIG['name']}")
        print(f"✓ Idiomas suportados: {len(SUPPORTED_LANGUAGES)}")
        print(f"✓ Taxa de amostragem: {AUDIO_CONFIG['sample_rate']} Hz")
        print(f"✓ Motor TTS: {TTS_CONFIG['engine']}")
        print(f"✓ Modelo IA: {AI_CONFIG['model']}")

        return True
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "=" * 60)
    print("🧪 TESTES DO SISTEMA - ASSISTENTE DE VOZ MULTIIDIOMAS")
    print("=" * 60)

    tests = [
        ("Configurações", test_config),
        ("Áudio", test_audio_module),
        ("Reconhecimento de Fala", test_speech_recognition),
        ("IA", test_ai_module),
        ("Síntese de Fala", test_tts_module),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erro ao executar teste: {str(e)}")
            results.append((name, False))

    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DOS TESTES")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} testes passaram ({passed*100//total}%)")

    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✓ Sistema pronto para usar")
        print("\nExecute: python main.py")
    else:
        print("\n⚠️  Alguns componentes podem estar faltando")
        print("Verifique as dependências: pip install -r requirements.txt")

    return passed == total


def verify_dependencies():
    """Verifica dependências instaladas"""
    print("\n" + "=" * 60)
    print("📦 VERIFICANDO DEPENDÊNCIAS")
    print("=" * 60 + "\n")

    dependencies = [
        'speech_recognition',
        'pyttsx3',
        'librosa',
        'sounddevice',
        'soundfile',
        'langdetect',
        'dotenv',
        'numpy',
    ]

    missing = []
    for package in dependencies:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - NÃO INSTALADO")
            missing.append(package)

    if missing:
        print(f"\n❌ Pacotes faltando: {', '.join(missing)}")
        print(f"\nInstale com: pip install {' '.join(missing)}")
        return False
    else:
        print("\n✓ Todas as dependências básicas instaladas")
        return True


def main():
    """Função principal"""
    print("\n🚀 TESTE RÁPIDO DO SISTEMA\n")

    # Verificar dependências primeiro
    if not verify_dependencies():
        print("\n⚠️  Execute: pip install -r requirements.txt")
        return False

    # Executar testes
    return run_all_tests()


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        sys.exit(1)
