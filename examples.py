"""
Exemplos de Uso Avançado do Assistente de Voz
Demonstra casos de uso e integrações personalizadas
"""

# ============================================================================
# EXEMPLO 1: Usar o assistente em um script externo
# ============================================================================

def exemplo_1_uso_basico():
    """Uso básico do assistente em outro projeto"""
    from ai_module import AIAssistant
    from tts_module import TextToSpeech

    # Inicializar assistente
    assistant = AIAssistant()
    tts = TextToSpeech()

    # Fazer pergunta
    pergunta = "O que é inteligência artificial?"
    response = assistant.get_response(pergunta, language='pt')

    # Reproduzir resposta
    print(f"Pergunta: {pergunta}")
    print(f"Resposta: {response}")
    tts.speak(response)


# ============================================================================
# EXEMPLO 2: Processar múltiplos áudios em lote
# ============================================================================

def exemplo_2_processar_lote():
    """Processa vários arquivos de áudio"""
    from speech_recognition_module import SpeechRecognizer
    from ai_module import AIAssistant
    import os

    recognizer = SpeechRecognizer()
    assistant = AIAssistant()

    audio_files = [f for f in os.listdir('audio_storage') if f.endswith('.wav')]

    for audio_file in audio_files[:5]:  # Processar primeiros 5
        filepath = os.path.join('audio_storage', audio_file)

        # Transcrever
        text, lang = recognizer.transcribe_audio(filepath)

        if text:
            # Gerar resposta
            response = assistant.get_response(text, language=lang.get('code', 'pt'))
            print(f"\n[{audio_file}]")
            print(f"  Texto: {text}")
            print(f"  Resposta: {response}")


# ============================================================================
# EXEMPLO 3: Conversa interativa com contexto
# ============================================================================

def exemplo_3_conversa_contextualizada():
    """Mantém conversação com contexto"""
    from ai_module import AIAssistant
    from tts_module import TextToSpeech
    from speech_recognition_module import SpeechRecognizer

    assistant = AIAssistant()
    tts = TextToSpeech()
    recognizer = SpeechRecognizer()

    # Adicionar contexto
    assistant.add_context('user_name', 'João')
    assistant.add_context('location', 'São Paulo')

    print("Conversa com contexto ativado (3 turnos)")
    print("-" * 40)

    for i in range(3):
        # Obter entrada do usuário
        text, lang = recognizer.transcribe_microphone()

        if text:
            # Gerar resposta mantendo contexto
            response = assistant.get_response(
                text,
                language=lang.get('code', 'pt'),
                context=assistant.context if hasattr(assistant, 'context') else None
            )

            print(f"\n🤖: {response}")
            tts.speak(response)


# ============================================================================
# EXEMPLO 4: Análise de emoções na resposta
# ============================================================================

def exemplo_4_analise_emocoes():
    """Detecta e ajusta a emoção na resposta"""
    from ai_module import AIAssistant
    from tts_module import TextToSpeech

    assistant = AIAssistant()
    tts = TextToSpeech()

    perguntas = [
        ("Você pode me felicitar?", "happy"),
        ("Estou muito triste hoje", "sad"),
        ("Que notícia incrivelmente maravilhosa!", "excited"),
    ]

    print("Exemplos com diferentes emoções")
    print("-" * 40)

    for pergunta, emotion_esperada in perguntas:
        response = assistant.get_response(pergunta, language='pt')
        print(f"\nPergunta: {pergunta}")
        print(f"Emoção: {emotion_esperada}")
        print(f"Resposta: {response}")

        # Reproduzir com a emoção apropriada
        tts.speak_with_expression(response, emotion=emotion_esperada)


# ============================================================================
# EXEMPLO 5: Salvar e recuperar conversas
# ============================================================================

def exemplo_5_salvar_conversas():
    """Salva conversas e permite recuperar o histórico"""
    from ai_module import AIAssistant
    import json
    from datetime import datetime

    assistant = AIAssistant()

    # Simular conversa
    perguntas = [
        "Qual é a capital do Brasil?",
        "Qual é o planeta mais próximo do sol?",
        "Quantos continentes existem?",
    ]

    for pergunta in perguntas:
        response = assistant.get_response(pergunta, language='pt')

    # Salvar conversa
    conversa_data = {
        'timestamp': datetime.now().isoformat(),
        'mensagens': assistant.conversation_history,
        'total_turnos': len(assistant.conversation_history) // 2,
    }

    with open('ultima_conversa.json', 'w', encoding='utf-8') as f:
        json.dump(conversa_data, f, ensure_ascii=False, indent=2)

    print("Conversa salva em 'ultima_conversa.json'")
    print(f"Total de turnos: {conversa_data['total_turnos']}")


# ============================================================================
# EXEMPLO 6: Transcrição com pós-processamento
# ============================================================================

def exemplo_6_transcricao_avancada():
    """Transcreve e processa o texto"""
    from speech_recognition_module import SpeechRecognizer
    import re

    recognizer = SpeechRecognizer()

    # Transcrever do microfone
    print("Fale algo para transcrever e processar")
    text, lang_info = recognizer.transcribe_microphone()

    if text:
        # Análise do texto
        print("\n" + "=" * 50)
        print("ANÁLISE DA TRANSCRIÇÃO")
        print("=" * 50)

        print(f"Texto: {text}")
        print(f"Idioma: {lang_info['name']} (confiança: {lang_info['confidence']:.1%})")
        print(f"Palavras: {len(text.split())}")
        print(f"Caracteres: {len(text)}")

        # Detectar padrões
        if any(word in text.lower() for word in ['o quê', 'como', 'por quê', 'quando']):
            print("Tipo: Pergunta")
        elif any(word in text.lower() for word in ['por favor', 'obrigado']):
            print("Tipo: Cortesia")
        else:
            print("Tipo: Afirmação")


# ============================================================================
# EXEMPLO 7: Ajustar qualidade de áudio
# ============================================================================

def exemplo_7_configurar_audio():
    """Configura parâmetros de áudio otimizados"""
    from audio_module import AudioRecorder
    from config import AUDIO_CONFIG

    print("Configurações de Áudio Disponíveis")
    print("-" * 40)

    recorder = AudioRecorder()

    # Exibir configurações atuais
    print(f"Taxa de amostragem: {AUDIO_CONFIG['sample_rate']} Hz")
    print(f"Canais: {AUDIO_CONFIG['channels']}")
    print(f"Duração máxima: {AUDIO_CONFIG['duration']}s")
    print(f"Limiar de silêncio: {AUDIO_CONFIG['threshold']}")

    # Gravar com detecção otimizada
    print("\n🎤 Gravando com detecção de silêncio...")
    audio_data, filepath = recorder.record_audio_with_detection(
        max_duration=30,
        silence_duration=2  # 2 segundos de silêncio para parar
    )

    if filepath:
        info = recorder.get_audio_info(filepath.split('/')[-1])
        print(f"\n✓ Áudio gravado com sucesso")
        print(f"  Duração: {info['duration']:.1f}s")
        print(f"  Tamanho: {info['file_size']/1024:.1f}KB")


# ============================================================================
# EXEMPLO 8: Integração com múltiplos idiomas
# ============================================================================

def exemplo_8_multiidiomas():
    """Demonstra suporte a múltiplos idiomas"""
    from ai_module import AIAssistant
    from tts_module import TextToSpeech

    assistant = AIAssistant()
    tts = TextToSpeech()

    conversas = {
        'pt': {
            'pergunta': 'Olá, como você está?',
            'emoji': '🇧🇷'
        },
        'en': {
            'pergunta': 'Hello, how are you?',
            'emoji': '🇺🇸'
        },
        'es': {
            'pergunta': '¿Hola, cómo estás?',
            'emoji': '🇪🇸'
        },
        'fr': {
            'pergunta': 'Bonjour, comment allez-vous?',
            'emoji': '🇫🇷'
        },
    }

    print("CONVERSAS MULTIIDIOMAS")
    print("=" * 50)

    for lang, dados in conversas.items():
        assistant.clear_history()  # Novo contexto para cada idioma

        response = assistant.get_response(dados['pergunta'], language=lang)

        print(f"\n{dados['emoji']} {lang.upper()}")
        print(f"  Pergunta: {dados['pergunta']}")
        print(f"  Resposta: {response}")

        # Reproduzir em fala
        tts.speak(response, lang_code=lang)


# ============================================================================
# EXEMPLO 9: Criar relatório de conversação
# ============================================================================

def exemplo_9_relatorio():
    """Gera relatório detalhado da sessão"""
    from ai_module import AIAssistant
    from datetime import datetime
    import json

    assistant = AIAssistant()

    # Simular conversação
    perguntas = [
        "Qual é a hora?",
        "Qual é a data hoje?",
    ]

    for pergunta in perguntas:
        assistant.get_response(pergunta, language='pt')

    # Gerar relatório
    relatorio = {
        'data_hora': datetime.now().isoformat(),
        'idioma': 'pt',
        'total_mensagens': len(assistant.conversation_history),
        'total_turnos': len(assistant.conversation_history) // 2,
        'conversacao': [
            {
                'turno': i // 2 + 1,
                'role': msg['role'],
                'content': msg['content'][:100] + '...' if len(msg['content']) > 100 else msg['content']
            }
            for i, msg in enumerate(assistant.conversation_history)
        ]
    }

    print("\n" + "=" * 60)
    print("RELATÓRIO DE CONVERSAÇÃO")
    print("=" * 60)
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))

    # Salvar relatório
    with open('relatorio_conversacao.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)

    print("\n✓ Relatório salvo em 'relatorio_conversacao.json'")


# ============================================================================
# EXEMPLO 10: Sistema de perguntas frequentes
# ============================================================================

def exemplo_10_faq():
    """Sistema de FAQ com respostas pré-definidas"""
    from ai_module import AIAssistant
    from tts_module import TextToSpeech

    assistant = AIAssistant()
    tts = TextToSpeech()

    faqs = {
        'o que é python': 'Python é uma linguagem de programação versátil e poderosa.',
        'como aprender programação': 'Você pode aprender com práticas, cursos online e projetos reais.',
        'qual é o melhor editor': 'VS Code é muito popular, mas escolha o que melhor se adapta a você.',
    }

    print("SISTEMA DE FAQ")
    print("=" * 50)

    pergunta_usuario = "Como aprender programação"

    # Procurar resposta no FAQ
    resposta_encontrada = False
    for faq_pergunta, faq_resposta in faqs.items():
        if faq_pergunta.lower() in pergunta_usuario.lower():
            print(f"\n📌 Pergunta: {pergunta_usuario}")
            print(f"📝 Resposta (FAQ): {faq_resposta}")
            tts.speak(faq_resposta)
            resposta_encontrada = True
            break

    if not resposta_encontrada:
        # Se não encontrou, usar IA
        response = assistant.get_response(pergunta_usuario, language='pt')
        print(f"\n📌 Pergunta: {pergunta_usuario}")
        print(f"🤖 Resposta (IA): {response}")
        tts.speak(response)


# ============================================================================
# MENU DE EXEMPLOS
# ============================================================================

def menu_exemplos():
    """Menu para escolher qual exemplo executar"""
    exemplos = {
        '1': ('Uso Básico', exemplo_1_uso_basico),
        '2': ('Processar Lote', exemplo_2_processar_lote),
        '3': ('Conversa Contextualizada', exemplo_3_conversa_contextualizada),
        '4': ('Análise de Emoções', exemplo_4_analise_emocoes),
        '5': ('Salvar Conversas', exemplo_5_salvar_conversas),
        '6': ('Transcrição Avançada', exemplo_6_transcricao_avancada),
        '7': ('Configurar Áudio', exemplo_7_configurar_audio),
        '8': ('Multiidiomas', exemplo_8_multiidiomas),
        '9': ('Relatório', exemplo_9_relatorio),
        '10': ('FAQ', exemplo_10_faq),
    }

    print("\n" + "=" * 60)
    print("📚 EXEMPLOS DE USO AVANÇADO")
    print("=" * 60)

    for key, (nome, _) in exemplos.items():
        print(f"{key}. {nome}")

    print("0. Sair")

    escolha = input("\n✍️  Escolha um exemplo: ").strip()

    if escolha in exemplos:
        nome, funcao = exemplos[escolha]
        print(f"\n▶️  Executando: {nome}")
        print("-" * 60)
        try:
            funcao()
        except Exception as e:
            print(f"❌ Erro ao executar: {str(e)}")
            import traceback
            traceback.print_exc()
    elif escolha != '0':
        print("❌ Opção inválida")


if __name__ == '__main__':
    try:
        menu_exemplos()
    except KeyboardInterrupt:
        print("\n\n⚠️  Exemplos interrompidos")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
