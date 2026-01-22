"""
Setup do Projeto - Assistente de Voz Multiidiomas
Script para instalar dependências e configurar o ambiente
"""
import os
import sys
import subprocess
from pathlib import Path


def create_env_file():
    """Cria arquivo .env com variáveis de ambiente"""
    env_content = """# Chaves de API (substitua pelos seus valores)
OPENAI_API_KEY=sua_chave_aqui
GROQ_API_KEY=sua_chave_aqui
GOOGLE_APPLICATION_CREDENTIALS=caminho/para/credenciais.json

# Configurações de Áudio
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1

# Configurações de Idioma
DEFAULT_LANGUAGE=pt
AUTO_DETECT_LANGUAGE=true

# Configurações de IA
AI_MODEL=groq
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500
"""
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✓ Arquivo .env criado. Configure com suas chaves de API.")


def install_dependencies():
    """Instala as dependências do projeto"""
    print("\n" + "=" * 60)
    print("📦 INSTALANDO DEPENDÊNCIAS")
    print("=" * 60 + "\n")

    requirements_file = 'requirements.txt'

    if not os.path.exists(requirements_file):
        print(f"❌ Arquivo {requirements_file} não encontrado!")
        return False

    try:
        print("🔄 Atualizando pip...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])

        print("\n🔄 Instalando pacotes...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])

        print("\n✓ Dependências instaladas com sucesso!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False


def create_directories():
    """Cria diretórios necessários"""
    directories = ['audio_storage', 'logs']

    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Diretório criado/verificado: {dir_name}")


def verify_installation():
    """Verifica se todos os módulos foram instalados corretamente"""
    print("\n" + "=" * 60)
    print("✓ VERIFICANDO INSTALAÇÃO")
    print("=" * 60 + "\n")

    modules_to_check = [
        'speech_recognition',
        'pyttsx3',
        'librosa',
        'sounddevice',
        'langdetect',
        'dotenv',
    ]

    all_ok = True
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✓ {module} - OK")
        except ImportError:
            print(f"❌ {module} - NÃO INSTALADO")
            all_ok = False

    return all_ok


def show_usage():
    """Mostra instruções de uso"""
    print("\n" + "=" * 60)
    print("📖 INSTRUÇÕES DE USO")
    print("=" * 60 + "\n")

    usage = """
1. CONFIGURAÇÃO INICIAL
   - Edite o arquivo .env com suas chaves de API
   - Configure as preferências em config.py

2. EXECUTAR O ASSISTENTE
   python main.py

3. MODOS DE INTERAÇÃO
   - Modo voz: Fale com o assistente
   - Modo texto: Digite suas perguntas
   - Suporta múltiplos idiomas

4. RECURSOS DISPONÍVEIS
   - Gravação e armazenamento de áudio
   - Reconhecimento de fala com detecção de idioma
   - Respostas inteligentes com IA
   - Síntese de fala expressiva
   - Histórico de conversas

5. PERSONALIZAÇÕES
   - Mudar idioma durante a execução
   - Ajustar velocidade e volume de fala
   - Definir emoções nas respostas
   - Adicionar contexto ao assistente

6. REQUISITOS DO SISTEMA
   - Python 3.8+
   - Microfone funcionando
   - Conexão com internet (para IA e reconhecimento)
   - ~500MB de espaço em disco

7. TROUBLESHOOTING
   - Se o microfone não funcionar, verifique permissões
   - Para erro de chaves de API, configure o .env
   - Verifique os logs em logs/assistant.log
    """

    print(usage)


def main():
    """Função principal de setup"""
    print("\n" + "=" * 60)
    print("🚀 SETUP - ASSISTENTE DE VOZ INTELIGENTE MULTIIDIOMAS")
    print("=" * 60 + "\n")

    # Criar diretórios
    create_directories()

    # Criar arquivo .env se não existir
    if not os.path.exists('.env'):
        create_env_file()

    # Instalar dependências
    if not install_dependencies():
        print("\n❌ Falha na instalação de dependências")
        return False

    # Verificar instalação
    if not verify_installation():
        print("\n⚠️  Alguns módulos podem estar faltando")

    # Mostrar instruções
    show_usage()

    print("\n" + "=" * 60)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("\nPróximo passo: python main.py\n")

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
