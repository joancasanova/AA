# infrastructure/llm/instruct_model.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Optional
from app.domain.ports.llm_port import LLMPort
import re

class InstructModel(LLMPort):
    def __init__(self, model_name: str = "EleutherAI/gpt-neo-125M"):
        self.instruct_mode = True if "instruct" in model_name.lower() else False
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def _extract_assistant_response(self, text: str) -> str:
        # Intentar extraer lo posterior a "assistant\n"
        match = re.search(r"assistant\n(.*)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()  # Si no se encuentra, devolver todo el texto

    def generate(self, system_prompt: str, user_prompt: str, num_responses:int=1, max_new_tokens:int=100) -> List[str]:
        if self.instruct_mode:
            # Build the message in the Instruct format
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]                        
            
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
        else:
            # Modo normal: lógica actual
            prompt = f"{system_prompt}\n{user_prompt}"

        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            num_return_sequences=num_responses,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

        if self.instruct_mode:
            # En modo instruct intentamos extraer sólo la parte del asistente
            # para cada respuesta generada
            final_responses = []
            for resp in decoded:
                final_responses.append(self._extract_assistant_response(resp))
            return final_responses
        else:
            # Modo normal: devolver tal cual
            return decoded




