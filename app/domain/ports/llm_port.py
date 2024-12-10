# domain/ports/llm_port.py

from typing import List

class LLMPort:
    def generate(self, system_prompt: str, user_prompt: str, num_responses:int=1, max_new_tokens:int=100) -> List[str]:
        raise NotImplementedError
