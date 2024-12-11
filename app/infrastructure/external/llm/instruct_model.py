# infrastructure/external/llm/instruct_model.py
from typing import List, Optional, Dict
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
import re
from datetime import datetime
from ....domain.ports.llm_port import LLMPort
from ....domain.model.entities.generation import GeneratedResult, GenerationMetadata

logger = logging.getLogger(__name__)

class InstructModel(LLMPort):
    def __init__(
        self,
        model_name: str = "EleutherAI/gpt-neo-125M",
        device: Optional[str] = None,
        cache_dir: Optional[str] = None,
        max_length: int = 2048
    ):
        self.model_name = model_name
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.cache_dir = cache_dir
        self.max_length = max_length
        self.instruct_mode = "instruct" in model_name.lower()
        
        logger.info(f"Initializing InstructModel with {model_name} on {self.device}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
            self.model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir)
            self.model.to(self.device)
        except Exception as e:
            logger.error(f"Error initializing LLM model: {str(e)}")
            raise

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        num_sequences: int = 1,
        max_tokens: int = 100,
        temperature: float = 1.0,
        stop_sequences: Optional[List[str]] = None
    ) -> List[GeneratedResult]:
        start_time = datetime.now()
        
        try:
            # Prepare input based on model type
            if self.instruct_mode:
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
                prompt = f"{system_prompt}\n{user_prompt}"

            # Tokenize input
            inputs = self.tokenizer(
                [prompt],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.max_length - max_tokens
            ).to(self.device)

            # Generate responses
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                num_return_sequences=num_sequences,
                do_sample=True,
                temperature=temperature,
                pad_token_id=self.tokenizer.eos_token_id,
                attention_mask=inputs['attention_mask']
            )

            # Decode outputs
            decoded_outputs = self.tokenizer.batch_decode(
                outputs,
                skip_special_tokens=True
            )

            # Process outputs
            results = []
            for output in decoded_outputs:
                content = self._extract_assistant_response(output) if self.instruct_mode else output
                
                # Apply stop sequences if provided
                if stop_sequences:
                    for stop_seq in stop_sequences:
                        if stop_seq in content:
                            content = content[:content.index(stop_seq)]

                # Create generation metadata
                metadata = GenerationMetadata(
                    model_name=self.model_name,
                    tokens_used=len(self.tokenizer.encode(content)),
                    generation_time=(datetime.now() - start_time).total_seconds()
                )

                results.append(GeneratedResult(
                    content=content.strip(),
                    metadata=metadata
                ))

            return results

        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise

    def get_token_count(self, text: str) -> int:
        try:
            return len(self.tokenizer.encode(text))
        except Exception as e:
            logger.error(f"Error counting tokens: {str(e)}")
            raise

    def _extract_assistant_response(self, text: str) -> str:
        # Extract content after "assistant" or "Assistant:"
        match = re.search(r"(?:assistant|Assistant):\s*(.*)", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return text.strip()