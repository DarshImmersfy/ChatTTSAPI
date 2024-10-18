"""Model wrapper to interact with OpenAI models."""

import os, time, json
import abc
import io
import logging

import soundfile as sf
import ChatTTS
import torch
import torchaudio

torch._dynamo.config.cache_size_limit = 64
torch._dynamo.config.suppress_errors = True
torch.set_float32_matmul_precision("high")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

EMBEDDINGDIR = r"voices\embed"


class ChatTTSWrapper(abc.ABC):
    def __init__(self):
        try:
            self.chat = ChatTTS.Chat()
            self.chat.load(compile=False)
        except Exception as exc:
            logging.error(f"Error: {exc}")

    def get_voice_embedding(self, voice: str = "Narration-1"):
        try:
            with open(os.path.join(EMBEDDINGDIR, voice + ".txt")) as f:
                voice_embedding = f.readlines()[0].strip()

            return voice_embedding
        except Exception as exc:
            logging.error(f"Error: {exc}")

    def load_params(self, speaker, temperature, top_P, top_K, manual_seed):
        params_infer_code = ChatTTS.Chat.InferCodeParams(spk_emb=speaker, temperature=temperature, top_P=top_P, top_K=top_K, manual_seed=manual_seed)

        # use oral_(0-9), laugh_(0-2), break_(0-7)
        # to generate special token in text to synthesize.
        params_refine_text = ChatTTS.Chat.RefineTextParams(prompt="[break_3][oral_2]", manual_seed=42)

        return params_infer_code, params_refine_text

    def encode(self, wavs):
        # Convert to io Bytes
        audio_bytes_list = []
        for i in range(len(wavs)):
            audio_bytes = io.BytesIO()
            sf.write(audio_bytes, wavs[i], 24000, format="WAV")
            audio_bytes.seek(0)
            audio_bytes_list.append(audio_bytes)

        return audio_bytes_list

    def generate_response(self, texts: list | str, voice: str = "Narration-3", temperature: float = 0.5, top_P: float = 0.7, top_K: float = 20, manual_seed: int = None):
        try:
            if isinstance(texts, str):
                texts = [texts]

            # Load speaker and params
            speaker = self.get_voice_embedding(voice)
            params_infer_code, params_refine_text = self.load_params(speaker, temperature, top_P, top_K, manual_seed)

            # Generate wav
            wavs = self.chat.infer(texts, params_refine_text=params_refine_text, params_infer_code=params_infer_code)

            return self.encode(wavs)

        except Exception as exc:
            logging.error(f"Error: {exc}")
