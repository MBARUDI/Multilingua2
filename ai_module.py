"""
Módulo de IA para Análise e Resposta Inteligente
Responsável por fornecer respostas contextualizadas e inteligentes
"""
import logging
import os
from datetime import datetime
from config import AI_CONFIG, OPENAI_API_KEY, GROQ_API_KEY, SUPPORTED_LANGUAGES, LOG_CONFIG

# Configurar logging
logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger(__name__)


class AIAssistant:
    """Classe para geração de respostas inteligentes"""

    def __init__(self):
        self.model = AI_CONFIG['model']
        self.temperature = AI_CONFIG['temperature']
        self.max_tokens = AI_CONFIG['max_tokens']
        self.conversation_history = []
        self.max_context_length = 5

        # Inicializar cliente apropriado
        if self.model == 'openai':
            self._initialize_openai()
        elif self.model == 'groq':
            self._initialize_groq()

    def _initialize_openai(self):
        """Inicializa cliente OpenAI"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model_name = 'gpt-3.5-turbo'
            logger.info("Cliente OpenAI inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar OpenAI: {str(e)}")
            print(f"⚠️  Aviso: OpenAI não está disponível ({str(e)})")

    def _initialize_groq(self):
        """Inicializa cliente Groq"""
        try:
            from groq import Groq
            self.client = Groq(api_key=GROQ_API_KEY)
            self.model_name = 'mixtral-8x7b-32768'
            logger.info("Cliente Groq inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar Groq: {str(e)}")
            print(f"⚠️  Aviso: Groq não está disponível ({str(e)})")

    def get_response(self, user_message, language='pt', context=None):
        """
        Gera resposta inteligente para a pergunta do usuário

        Args:
            user_message (str): Mensagem do usuário
            language (str): Código do idioma
            context (dict): Contexto adicional

        Returns:
            str: Resposta gerada
        """
        try:
            # Adicionar mensagem ao histórico
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })

            # Limitar histórico de conversação
            if len(self.conversation_history) > self.max_context_length * 2:
                self.conversation_history = self.conversation_history[-(self.max_context_length * 2):]

            # Construir sistema prompt
            system_prompt = self._build_system_prompt(language, context)

            # Preparar mensagens
            messages = [{'role': 'system', 'content': system_prompt}]
            messages.extend(self.conversation_history)

            print("🤖 Pensando...")
            logger.info(f"Gerando resposta para: {user_message}")

            # Chamar modelo apropriado
            if self.model == 'openai':
                response = self._call_openai(messages)
            elif self.model == 'groq':
                response = self._call_groq(messages)
            else:
                response = self._get_fallback_response(user_message, language)

            # Adicionar resposta ao histórico
            self.conversation_history.append({
                'role': 'assistant',
                'content': response
            })

            logger.info(f"Resposta gerada: {response[:100]}...")
            return response

        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return self._get_fallback_response(user_message, language)

    def _call_openai(self, messages):
        """Chama API do OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro ao chamar OpenAI: {str(e)}")
            raise

    def _call_groq(self, messages):
        """Chama API do Groq"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro ao chamar Groq: {str(e)}")
            raise

    def _build_system_prompt(self, language, context=None):
        """Constrói o system prompt com contexto"""
        language_name = SUPPORTED_LANGUAGES.get(language, {}).get('name', 'Português')

        system_prompt = f"""Você é ARIA, um assistente pessoal inteligente, amigável e prestativo.

CARACTERÍSTICAS:
- Responda sempre em {language_name}
- Seja conversacional e natural
- Use tom amigável e profissional
- Forneça respostas úteis e precisas
- Se não souber algo, seja honesto
- Mantenha o contexto da conversa anterior
- Use emojis ocasionalmente para expressar emoções
- Adapte sua resposta ao tom da pergunta

CONTEXTO:
- Data e hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}
- Idioma: {language_name}
"""

        if context:
            if context.get('user_name'):
                system_prompt += f"- Nome do usuário: {context['user_name']}\n"
            if context.get('location'):
                system_prompt += f"- Localização: {context['location']}\n"
            if context.get('preferences'):
                system_prompt += f"- Preferências: {context['preferences']}\n"

        return system_prompt

    def _get_fallback_response(self, user_message, language):
        """Fornece resposta de fallback quando IA não está disponível"""
        responses = {
            'pt': [
                f"Entendi sua pergunta: '{user_message}'. Desculpe, não consegui processar isso agora.",
                "Essa é uma boa pergunta! Me desculpe por não conseguir responder agora.",
                f"Você perguntou sobre: {user_message}. Vou tentar ajudar melhor em breve!",
            ],
            'en': [
                f"I understood your question: '{user_message}'. Sorry, I couldn't process that now.",
                "That's a good question! I apologize for not being able to answer right now.",
            ],
            'es': [
                f"Entendí tu pregunta: '{user_message}'. Disculpa, no pude procesar eso ahora.",
                "¡Esa es una buena pregunta! Disculpa por no poder responder ahora.",
            ],
        }

        lang_responses = responses.get(language, responses['pt'])
        import random
        return random.choice(lang_responses)

    def clear_history(self):
        """Limpa o histórico de conversação"""
        self.conversation_history = []
        logger.info("Histórico de conversação limpo")

    def get_conversation_summary(self):
        """Obtém um resumo da conversação"""
        return f"Conversação com {len(self.conversation_history)} mensagens"

    def add_context(self, key, value):
        """Adiciona contexto para futuras respostas"""
        if not hasattr(self, 'context'):
            self.context = {}
        self.context[key] = value
        logger.info(f"Contexto adicionado: {key} = {value}")
