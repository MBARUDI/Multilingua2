# 🎙️ ARIA - Assistente de Voz Inteligente Multiidiomas

Um aplicativo Python avançado que implementa um assistente pessoal inteligente de voz com suporte a múltiplos idiomas.

## ✨ Características Principais

- **🎤 Reconhecimento de Fala**: Transcrição de áudio em tempo real com múltiplos idiomas
- **🌍 Multiidiomas**: Suporte para Português, Inglês, Espanhol, Francês, Alemão, Italiano, Japonês e Chinês
- **🤖 IA Inteligente**: Respostas contextualizadas usando APIs de última geração (OpenAI/Groq)
- **🔊 Síntese de Fala Expressiva**: Conversão de texto em fala com variação de emoções
- **💾 Armazenamento de Áudio**: Gravação e armazenamento automático de conversas
- **🔍 Detecção de Idioma**: Identificação automática do idioma da pergunta
- **📝 Histórico de Conversas**: Manutenção de contexto entre interações

## 📋 Requisitos do Sistema

- **Python**: 3.8 ou superior
- **Microfone**: Funcionando corretamente
- **Internet**: Para APIs de IA e reconhecimento de fala
- **Espaço em Disco**: Mínimo 500MB
- **SO**: Windows, macOS ou Linux

## 🚀 Instalação

### 1. Clone ou copie o projeto

```bash
cd Multilingua2
```

### 2. Execute o setup

```bash
python setup.py
```

Este script irá:
- Criar diretórios necessários
- Instalar todas as dependências
- Criar arquivo de configuração `.env`
- Verificar a instalação

### 3. Configure suas chaves de API

Edite o arquivo `.env`:

```env
OPENAI_API_KEY=sua_chave_openai_aqui
GROQ_API_KEY=sua_chave_groq_aqui
```

### 4. Executar o Assistente

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
Multilingua2/
├── main.py                      # Aplicativo principal
├── config.py                    # Configurações globais
├── setup.py                     # Script de instalação
├── requirements.txt             # Dependências Python
├── audio_module.py             # Gravação e armazenamento de áudio
├── speech_recognition_module.py # Reconhecimento de fala
├── ai_module.py                # Processamento com IA
├── tts_module.py               # Síntese de fala
├── .env                        # Variáveis de ambiente (criado automaticamente)
├── audio_storage/              # Diretório de armazenamento de áudios
├── logs/                       # Diretório de logs
└── README.md                   # Esta documentação
```

## 🎯 Como Usar

### Menu Principal

Após executar `python main.py`, você verá:

```
🎙️ ARIA - Assistente de Voz Inteligente Multiidiomas
=======================================================

📋 MENU PRINCIPAL
1. 🎤 Fazer pergunta (voz)
2. ⌨️  Escrever pergunta (texto)
3. 🌍 Mudar idioma
4. 📁 Ver histórico de áudios
5. 🔍 Ver informações do assistente
6. ❌ Sair
```

### Modo Voz

1. Selecione opção `1`
2. Fale sua pergunta (máximo 30 segundos)
3. O assistente transcreverá, analisará e responderá em voz

### Modo Texto

1. Selecione opção `2`
2. Digite sua pergunta
3. Pressione Enter
4. Receba resposta em voz e texto

### Mudar Idioma

1. Selecione opção `3`
2. Escolha o idioma desejado
3. Todas as futuras interações serão neste idioma

## 🔧 Configurações Personalizadas

### Arquivo `config.py`

Você pode personalizar:

```python
# Configurações de áudio
AUDIO_CONFIG = {
    'sample_rate': 16000,      # Taxa de amostragem
    'duration': 30,            # Duração máxima em segundos
    'threshold': 1000,         # Limiar de detecção de silêncio
}

# Configurações de síntese de fala
TTS_CONFIG = {
    'rate': 150,              # Velocidade (100-200)
    'volume': 0.9,            # Volume (0.0 - 1.0)
    'voice_variant': 'female', # 'male' ou 'female'
}

# Configurações de IA
AI_CONFIG = {
    'model': 'groq',          # 'openai' ou 'groq'
    'temperature': 0.7,       # Criatividade (0.0 - 1.0)
    'max_tokens': 500,        # Comprimento máximo da resposta
}
```

## 📚 Módulos Disponíveis

### `AudioRecorder` (audio_module.py)

```python
recorder = AudioRecorder()

# Gravar áudio
audio_data, filepath = recorder.record_audio(duration=10)

# Gravar com detecção de silêncio
audio_data, filepath = recorder.record_audio_with_detection()

# Listar arquivos
files = recorder.list_audio_files()

# Obter informações
info = recorder.get_audio_info('audio_20240122_145030.wav')
```

### `SpeechRecognizer` (speech_recognition_module.py)

```python
recognizer = SpeechRecognizer()

# Transcrever arquivo
text, language = recognizer.transcribe_audio('audio.wav')

# Transcrever do microfone
text, language = recognizer.transcribe_microphone()

# Detectar idioma
lang_info = recognizer.detect_language("Olá, como você está?")
# Retorna: {'code': 'pt', 'name': 'Português', 'confidence': 0.95}
```

### `AIAssistant` (ai_module.py)

```python
assistant = AIAssistant()

# Gerar resposta
response = assistant.get_response(
    "Como funciona fotossíntese?",
    language='pt'
)

# Limpar histórico
assistant.clear_history()

# Adicionar contexto
assistant.add_context('user_name', 'João')
```

### `TextToSpeech` (tts_module.py)

```python
tts = TextToSpeech()

# Reproduzir fala
tts.speak("Olá mundo!", lang_code='pt')

# Reproduzir com expressão
tts.speak_with_expression(
    "Que dia maravilhoso!",
    emotion='happy',
    lang_code='pt'
)

# Salvar em arquivo
tts.save_to_file("Teste", 'output.mp3')

# Ajustar velocidade e volume
tts.set_rate(150)
tts.set_volume(0.8)
```

## 🌍 Idiomas Suportados

| Código | Idioma | Código de Fala |
|--------|--------|---|
| pt | Português | pt-BR |
| en | Inglês | en-US |
| es | Espanhol | es-ES |
| fr | Francês | fr-FR |
| de | Alemão | de-DE |
| it | Italiano | it-IT |
| ja | Japonês | ja-JP |
| zh | Chinês | zh-CN |

## 🐛 Troubleshooting

### Erro: "Microfone não encontrado"
- Verifique se o microfone está conectado
- Teste com `python -c "import sounddevice; print(sounddevice.query_devices())"`

### Erro: "Chave de API inválida"
- Verifique se as chaves estão corretas no `.env`
- Certifique-se que a chave tem permissões adequadas

### Erro: "Módulo não encontrado"
- Execute `pip install -r requirements.txt` novamente
- Use `python -m pip install --upgrade pip`

### Áudio não está sendo armazenado
- Verifique permissões da pasta `audio_storage`
- Certifique-se de ter espaço em disco suficiente

### Síntese de fala lenta
- Reduza `AI_CONFIG['max_tokens']`
- Considere usar `groq` em vez de `openai`

## 📊 Logging

Os logs são salvos em `logs/assistant.log`. Para visualizar:

```bash
tail -f logs/assistant.log
```

Ou em tempo real:

```bash
python -c "import time; 
while True: 
    with open('logs/assistant.log') as f: print(f.read()); 
    time.sleep(1)"
```

## 🔐 Segurança

- **Nunca** compartilhe suas chaves de API no código
- Use apenas o arquivo `.env` para armazenar credenciais
- Adicione `.env` ao `.gitignore` se usar versionamento
- Os áudios são armazenados localmente por padrão

## 📈 Performance

### Otimizações Aplicadas

- **Cache de modelos**: Reutiliza modelos entre requisições
- **Detecção de silêncio**: Encerra gravação automaticamente
- **Compressão de histórico**: Limita contexto a 5 mensagens
- **Processamento assíncrono**: Não bloqueia a interface

### Métricas Típicas

- Tempo de transcrição: 2-5 segundos
- Tempo de resposta de IA: 1-3 segundos
- Tempo de síntese de fala: 1-2 segundos

## 📝 Exemplos de Uso Avançado

### Iniciar com idioma específico

Modifique `main.py`:

```python
assistant.current_language = 'en'
assistant._greet_user()
```

### Integrar em outro projeto

```python
from ai_module import AIAssistant
from tts_module import TextToSpeech

assistant = AIAssistant()
tts = TextToSpeech()

response = assistant.get_response("Qual é a capital do Brasil?")
tts.speak(response)
```

### Processar arquivo em lote

```python
from speech_recognition_module import SpeechRecognizer

recognizer = SpeechRecognizer()
text, lang = recognizer.transcribe_audio('conversation.wav')
print(f"Transcrito em {lang}: {text}")
```

## 🤝 Contribuição

Para melhorias:

1. Teste localmente
2. Verifique logs em `logs/assistant.log`
3. Mantenha compatibilidade com Python 3.8+

## 📄 Licença

Uso pessoal e educacional.

## 📞 Suporte

Para problemas:
1. Verifique este README
2. Consulte os logs em `logs/assistant.log`
3. Teste cada módulo isoladamente

---

**Desenvolvido com ❤️ para assistência inteligente multiidiomas**

Versão 1.0 | 2024
# Multilingua2
