# 🏗️ Arquitetura do Assistente de Voz Multiidiomas

## Visão Geral

O assistente é uma aplicação modular que integra captura de áudio, reconhecimento de fala, processamento com IA e síntese de fala expressiva.

```
┌─────────────────────────────────────────────────────────┐
│         Interface Principal (main.py)                   │
│  - Menu de interação                                    │
│  - Fluxo de conversação                                 │
│  - Gerenciamento de idiomas                             │
└────────┬────────────────────────────────────────────────┘
         │
    ┌────┴────┐────────┬──────────────┐
    ▼         ▼        ▼              ▼
┌────────┐┌─────┐┌──────┐        ┌────────┐
│ Áudio  ││ Fala││  IA  │        │  TTS   │
│ Module ││Recon││Module│        │Module  │
└────────┘└─────┘└──────┘        └────────┘
    │         │        │              │
    ▼         ▼        ▼              ▼
┌──────────────────────────────────────────┐
│        Configurações Centralizadas        │
│              (config.py)                  │
└──────────────────────────────────────────┘
```

## Módulos Principais

### 1. **audio_module.py** - Captura de Áudio
**Responsabilidades:**
- Gravação de áudio do microfone
- Detecção automática de silêncio
- Armazenamento em disco
- Gerenciamento de arquivos de áudio

**Classes:**
- `AudioRecorder` - Gerencia toda a captura e armazenamento

**Métodos principais:**
```python
record_audio()                    # Grava áudio simples
record_audio_with_detection()    # Grava com detecção de silêncio
list_audio_files()               # Lista arquivos salvos
get_audio_info()                 # Obtém informações do arquivo
delete_audio_file()              # Remove arquivo
```

### 2. **speech_recognition_module.py** - Reconhecimento de Fala
**Responsabilidades:**
- Transcrição de áudio em texto
- Detecção automática de idioma
- Reconhecimento via API do Google

**Classes:**
- `SpeechRecognizer` - Gerencia transcrição e detecção

**Métodos principais:**
```python
transcribe_audio()               # Transcreve arquivo
transcribe_microphone()          # Transcreve do microfone
detect_language()                # Identifica idioma
get_language_code()              # Converte nome em código
```

### 3. **ai_module.py** - Processamento Inteligente
**Responsabilidades:**
- Geração de respostas contextualizadas
- Manutenção de histórico de conversação
- Integração com APIs de IA (OpenAI/Groq)
- Gerenciamento de contexto

**Classes:**
- `AIAssistant` - Gerencia processamento de IA

**Métodos principais:**
```python
get_response()                   # Gera resposta inteligente
clear_history()                  # Limpa histórico
add_context()                    # Adiciona contexto
get_conversation_summary()       # Resumo da conversa
```

### 4. **tts_module.py** - Síntese de Fala
**Responsabilidades:**
- Conversão de texto em fala
- Variação de emoções nas respostas
- Controle de velocidade e volume
- Salvamento de áudio sintetizado

**Classes:**
- `TextToSpeech` - Gerencia síntese de fala

**Métodos principais:**
```python
speak()                          # Reproduz fala simples
speak_with_expression()          # Reproduz com emoção
save_to_file()                   # Salva em arquivo
set_rate()                       # Define velocidade
set_volume()                     # Define volume
```

### 5. **config.py** - Configurações Centralizadas
**Gerencia:**
- Configurações de áudio
- Configurações de IA
- Configurações de síntese de fala
- Idiomas suportados
- Chaves de API
- Diretórios de armazenamento

### 6. **main.py** - Interface Principal
**Gerencia:**
- Loop principal da aplicação
- Menu de interação
- Fluxo de conversação
- Mudança de idioma
- Histórico de áudios
- Encerramento gracioso

## Fluxo de Funcionamento

### Modo Voz
```
1. Usuário seleciona "Fazer pergunta (voz)"
   ↓
2. AudioRecorder.record_audio_with_detection()
   ↓
3. SpeechRecognizer.transcribe_audio()
   ↓
4. Detecta idioma (detect_language)
   ↓
5. AIAssistant.get_response()
   ↓
6. TextToSpeech.speak_with_expression()
   ↓
7. Apresenta resposta em voz e texto
```

### Modo Texto
```
1. Usuário seleciona "Escrever pergunta (texto)"
   ↓
2. Entrada de texto do usuário
   ↓
3. Detecta idioma (detect_language)
   ↓
4. AIAssistant.get_response()
   ↓
5. TextToSpeech.speak_with_expression()
   ↓
6. Apresenta resposta em voz e texto
```

## Padrões de Design

### 1. **Encapsulamento**
Cada módulo é responsável por sua área específica:
- `AudioRecorder` - Só lida com áudio
- `SpeechRecognizer` - Só lida com reconhecimento
- `AIAssistant` - Só lida com IA
- `TextToSpeech` - Só lida com síntese

### 2. **Configuração Centralizada**
Todas as configurações em `config.py` para fácil manutenção e ajustes.

### 3. **Logging**
Cada módulo registra suas operações para debugging e auditoria.

### 4. **Tratamento de Erros**
Cada módulo trata seus próprios erros e fornece feedback claro.

### 5. **Contexto Persistente**
O `AIAssistant` mantém histórico para respostas contextualizadas.

## Fluxo de Dados

```
┌─────────────┐
│ Usuário     │
└──────┬──────┘
       │
       │ (áudio/texto)
       ▼
┌──────────────────────┐
│ Interface (main.py)  │
└──────┬───────────────┘
       │
       ├─────────────────────────┐
       │                         │
       ▼ (áudio)               ▼ (texto)
┌────────────────┐       ┌────────────────┐
│ AudioRecorder  │       │ Usuário input  │
└────────┬───────┘       └────────┬───────┘
         │                        │
         ▼ (arquivo wav)          ▼ (string)
┌────────────────────────────────────────┐
│ SpeechRecognizer                       │
└────────┬─────────────────────────────┬─┘
         │ (detecção de idioma)       │
         ▼                            ▼
┌──────────────────────────────────────────┐
│ AIAssistant (get_response)               │
├──────────────────────────────────────────┤
│ - Context + Message                      │
│ - API Call (OpenAI/Groq)                 │
│ - Response Generation                    │
└────────┬─────────────────────────────────┘
         │
         ▼ (resposta em texto)
┌──────────────────────────────────────────┐
│ TextToSpeech                             │
├──────────────────────────────────────────┤
│ - Emotional Expression                   │
│ - Speech Synthesis                       │
│ - Audio Output                           │
└────────┬─────────────────────────────────┘
         │
         ▼ (áudio + texto)
┌──────────────────────────┐
│ Usuário recebe resposta  │
└──────────────────────────┘
```

## Estrutura de Diretórios

```
Multilingua2/
├── 📄 main.py                       # Aplicativo principal
├── 📄 config.py                     # Configurações
├── 📄 setup.py                      # Script de instalação
├── 📄 test_system.py               # Testes do sistema
├── 📄 examples.py                   # Exemplos de uso
├── 📄 audio_module.py              # Gravação de áudio
├── 📄 speech_recognition_module.py # Reconhecimento de fala
├── 📄 ai_module.py                 # Processamento com IA
├── 📄 tts_module.py                # Síntese de fala
├── 📄 requirements.txt              # Dependências
├── 📄 .env.example                 # Template de configuração
├── 📄 README.md                    # Documentação principal
├── 📄 ARCHITECTURE.md              # Este arquivo
├── 📄 QUICK_START.md               # Guia rápido
│
├── 📁 audio_storage/               # Arquivos de áudio gravados
│   └── audio_20240122_145030.wav   # Exemplo
│
├── 📁 logs/                        # Arquivos de log
│   └── assistant.log               # Log principal
│
└── 📁 __pycache__/                 # Cache Python (ignorar)
```

## Integração de APIs

### OpenAI
```python
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=messages
)
```

### Groq
```python
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)
response = client.chat.completions.create(
    model='mixtral-8x7b-32768',
    messages=messages
)
```

### Google Speech Recognition
```python
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio, language='pt-BR')
```

## Performance

### Benchmarks Típicos

| Operação | Tempo | Fatores |
|----------|-------|---------|
| Gravação (10s) | ~11s | Tempo real + processamento |
| Transcrição | 2-5s | Tamanho do áudio, rede |
| IA Response | 1-3s | Comprimento, complexidade |
| Síntese de Fala | 1-2s | Comprimento do texto |
| **Total (uma conversa)** | **5-11s** | Soma de tudo |

### Otimizações

1. **Cache de modelos** - Reutiliza modelos entre requisições
2. **Compressão de histórico** - Limita a 5 mensagens anteriores
3. **Detecção de silêncio** - Encerra gravação automaticamente
4. **API selection** - Groq é mais rápido que OpenAI

## Escalabilidade

### Melhorias Futuras
1. Banco de dados para histórico persistente
2. Cache de respostas frequentes
3. Processamento em background
4. Sincronização em nuvem
5. Múltiplas conversas simultâneas
6. Web interface
7. API REST

## Segurança

### Implementadas
- ✓ Armazenamento local de áudios
- ✓ Variáveis de ambiente para chaves
- ✓ Logging sem exposição de dados sensíveis
- ✓ Validação de entrada

### Recomendações
- ☐ Criptografia de dados em repouso
- ☐ Autenticação de usuário
- ☐ Controle de acesso
- ☐ Auditoria de operações

## Testabilidade

Cada módulo pode ser testado isoladamente:

```python
# Testar AudioRecorder
from audio_module import AudioRecorder
recorder = AudioRecorder()
audio, path = recorder.record_audio()

# Testar SpeechRecognizer
from speech_recognition_module import SpeechRecognizer
recognizer = SpeechRecognizer()
text, lang = recognizer.transcribe_audio(path)

# Testar AIAssistant
from ai_module import AIAssistant
assistant = AIAssistant()
response = assistant.get_response(text)

# Testar TextToSpeech
from tts_module import TextToSpeech
tts = TextToSpeech()
tts.speak(response)
```

---

**Documentação de Arquitetura v1.0**
