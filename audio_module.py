"""
Módulo de Captura e Armazenamento de Áudio
Responsável pela gravação de áudio do microfone e armazenamento em disco
"""
import os
import logging
import numpy as np
import soundfile as sf
from datetime import datetime
from pathlib import Path
import threading
from config import AUDIO_CONFIG, AUDIO_STORAGE_DIR, LOG_CONFIG

# Tentar usar sounddevice, se não disponível, usar pyaudio
try:
    import sounddevice as sd
    USE_SOUNDDEVICE = True
    AUDIO_BACKEND = "sounddevice"
except (ImportError, OSError):
    try:
        import pyaudio
        USE_SOUNDDEVICE = False
        AUDIO_BACKEND = "pyaudio"
    except ImportError:
        # Sem bibliotecas disponíveis, usar simulador
        USE_SOUNDDEVICE = None
        AUDIO_BACKEND = "simulator"

# Configurar logging
logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger(__name__)


class AudioRecorder:
    """Classe para gravação e armazenamento de áudio"""

    def __init__(self):
        self.sample_rate = AUDIO_CONFIG['sample_rate']
        self.channels = AUDIO_CONFIG['channels']
        self.duration = AUDIO_CONFIG['duration']
        self.is_recording = False
        self.audio_data = None
        self.recording_thread = None

    def record_audio(self, duration=None, filename=None):
        """
        Grava áudio do microfone

        Args:
            duration (int): Duração da gravação em segundos
            filename (str): Nome do arquivo a salvar

        Returns:
            np.ndarray: Dados de áudio gravados
            str: Caminho do arquivo salvo
        """
        try:
            if duration is None:
                duration = self.duration

            logger.info(f"Iniciando gravação de áudio por {duration}s...")
            print(f"🎤 Gravando por {duration} segundos... (fale agora)")

            # Gravar áudio
            if USE_SOUNDDEVICE:
                audio_data = sd.rec(
                    int(self.sample_rate * duration),
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype='int16'
                )
                sd.wait()
            elif USE_SOUNDDEVICE is False:
                # Usar PyAudio como alternativa
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=1024
                )
                
                frames = []
                for _ in range(0, int(self.sample_rate / 1024 * duration)):
                    data = stream.read(1024)
                    frames.append(np.frombuffer(data, dtype=np.int16))
                
                stream.stop_stream()
                stream.close()
                p.terminate()
                
                audio_data = np.concatenate(frames)
            else:
                # Usar simulador de áudio como fallback
                logger.warning(f"Usando simulador de áudio (backend: {AUDIO_BACKEND})")
                print(f"📡 Usando simulador de áudio (sem biblioteca real disponível)")
                
                # Gerar áudio simulado (silêncio com algum ruído)
                num_samples = int(self.sample_rate * duration)
                audio_data = np.random.randint(-100, 100, num_samples, dtype=np.int16)

            logger.info("Gravação concluída com sucesso")
            print("✓ Gravação concluída")

            # Salvar arquivo
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"audio_{timestamp}.wav"

            filepath = os.path.join(AUDIO_STORAGE_DIR, filename)
            sf.write(filepath, audio_data, self.sample_rate)

            logger.info(f"Áudio salvo em: {filepath}")
            print(f"✓ Áudio salvo: {filename}")

            return audio_data, filepath

        except Exception as e:
            logger.error(f"Erro ao gravar áudio: {str(e)}")
            print(f"❌ Erro na gravação: {str(e)}")
            return None, None

    def record_audio_with_detection(self, max_duration=30, silence_duration=2):
        """
        Grava áudio com detecção automática de silêncio
        Para de gravar quando detecta silêncio prolongado

        Args:
            max_duration (int): Duração máxima da gravação
            silence_duration (int): Tempo de silêncio para parar

        Returns:
            np.ndarray: Dados de áudio gravados
            str: Caminho do arquivo salvo
        """
        try:
            logger.info("Iniciando gravação com detecção de silêncio...")
            print("🎤 Fale agora (gravação com detecção de silêncio)...")

            frames = []
            threshold = AUDIO_CONFIG['threshold']
            silence_counter = 0
            silence_limit = int(silence_duration * (self.sample_rate / 1024))

            # Gravar chunks
            if USE_SOUNDDEVICE:
                with sd.InputStream(
                    channels=self.channels,
                    samplerate=self.sample_rate,
                    blocksize=1024,
                    dtype='int16'
                ) as stream:
                    for _ in range(int(max_duration * self.sample_rate / 1024)):
                        chunk, _ = stream.read(1024)
                        frames.append(chunk)

                        # Detectar silêncio
                        if np.abs(chunk).mean() < threshold:
                            silence_counter += 1
                        else:
                            silence_counter = 0

                        # Se silêncio prolongado, parar
                        if silence_counter > silence_limit:
                            logger.info("Silêncio detectado, encerrando gravação")
                            print("✓ Silêncio detectado, encerrando...")
                            break
            elif USE_SOUNDDEVICE is False:
                # Usar PyAudio
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=1024
                )
                
                for _ in range(int(max_duration * self.sample_rate / 1024)):
                    data = stream.read(1024)
                    chunk = np.frombuffer(data, dtype=np.int16)
                    frames.append(chunk)
                    
                    # Detectar silêncio
                    if np.abs(chunk).mean() < threshold:
                        silence_counter += 1
                    else:
                        silence_counter = 0
                    
                    # Se silêncio prolongado, parar
                    if silence_counter > silence_limit:
                        logger.info("Silêncio detectado, encerrando gravação")
                        print("✓ Silêncio detectado, encerrando...")
                        break
                
                stream.stop_stream()
                stream.close()
                p.terminate()
            else:
                # Usar simulador de áudio como fallback
                logger.warning(f"Usando simulador de áudio (backend: {AUDIO_BACKEND})")
                print(f"📡 Usando simulador de áudio (sem biblioteca real disponível)")
                
                # Gerar áudio simulado
                for _ in range(int(max_duration * self.sample_rate / 1024)):
                    chunk = np.random.randint(-100, 100, 1024, dtype=np.int16)
                    frames.append(chunk)
                    # Simulador termina rapidamente
                    break

            audio_data = np.concatenate(frames)

            # Salvar arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_{timestamp}.wav"
            filepath = os.path.join(AUDIO_STORAGE_DIR, filename)
            sf.write(filepath, audio_data, self.sample_rate)

            logger.info(f"Áudio com detecção salvo em: {filepath}")
            print(f"✓ Áudio salvo: {filename}")

            return audio_data, filepath

        except Exception as e:
            logger.error(f"Erro ao gravar com detecção: {str(e)}")
            print(f"❌ Erro: {str(e)}")
            return None, None

    def list_audio_files(self):
        """Lista todos os arquivos de áudio armazenados"""
        try:
            files = sorted(os.listdir(AUDIO_STORAGE_DIR))
            audio_files = [f for f in files if f.endswith(('.wav', '.mp3', '.ogg'))]
            return audio_files
        except Exception as e:
            logger.error(f"Erro ao listar arquivos: {str(e)}")
            return []

    def get_audio_file(self, filename):
        """Carrega um arquivo de áudio"""
        try:
            filepath = os.path.join(AUDIO_STORAGE_DIR, filename)
            audio_data, sr = sf.read(filepath)
            logger.info(f"Áudio carregado: {filename}")
            return audio_data, sr
        except Exception as e:
            logger.error(f"Erro ao carregar áudio: {str(e)}")
            return None, None

    def delete_audio_file(self, filename):
        """Remove um arquivo de áudio"""
        try:
            filepath = os.path.join(AUDIO_STORAGE_DIR, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Arquivo removido: {filename}")
                print(f"✓ Arquivo removido: {filename}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover arquivo: {str(e)}")
            return False

    def get_audio_info(self, filename):
        """Obtém informações sobre um arquivo de áudio"""
        try:
            filepath = os.path.join(AUDIO_STORAGE_DIR, filename)
            audio_data, sr = sf.read(filepath)
            duration = len(audio_data) / sr
            return {
                'filename': filename,
                'sample_rate': sr,
                'duration': duration,
                'channels': 1 if len(audio_data.shape) == 1 else audio_data.shape[1],
                'file_size': os.path.getsize(filepath),
            }
        except Exception as e:
            logger.error(f"Erro ao obter informações: {str(e)}")
            return None
