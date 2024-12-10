# application/use_cases/generate_text_use_case.py
import logging
from typing import List, Dict
from app.domain.entities import GeneratedResult
from app.domain.ports.llm_port import LLMPort
import re

logger = logging.getLogger(__name__)

def extract_placeholders(text: str) -> List[str]:
    logger.debug(f"Extracting placeholders from text: {text}")
    return re.findall(r"{([^{}]+)}", text)

def validate_and_replace_placeholders(prompt: str, data: Dict[str, str]) -> str:
    logger.debug(f"Validating and replacing placeholders in prompt: {prompt} with data: {data}")
    placeholders = extract_placeholders(prompt)
    for ph in placeholders:
        if ph not in data:
            logger.error(f"Missing placeholder '{ph}' in reference data")
            raise ValueError(f"Missing placeholder '{ph}' in reference data")
        prompt = prompt.replace(f"{{{ph}}}", data[ph])
    logger.debug(f"Final prompt after replacement: {prompt}")
    return prompt

class GenerateTextUseCase:
    def __init__(self, llm: LLMPort):
        self.llm = llm
        logger.info("GenerateTextUseCase initialized")

    def execute(self, system_prompt: str, user_prompt: str, num_return_sequences: int, max_new_tokens: int,
                num_executions: int, reference_data: Dict[str, str]) -> List[GeneratedResult]:
        logger.info(f"Executing text generation with system_prompt: {system_prompt}, user_prompt: {user_prompt}, "
                    f"num_return_sequences: {num_return_sequences}, max_new_tokens: {max_new_tokens}, "
                    f"num_executions: {num_executions}, reference_data: {reference_data}")

        # Validate num_return_sequences
        if num_return_sequences <= 0 or max_new_tokens <= 0 or num_executions <= 0:
            logger.error("num_return_sequences, max_new_tokens and num_executions must be greater than 0")
            raise ValueError("num_return_sequences, max_new_tokens and num_executions must be greater than 0")

        all_placeholders = set(extract_placeholders(system_prompt)) | set(extract_placeholders(user_prompt))

        if all_placeholders and not reference_data:
            logger.error("Placeholders defined but no reference data provided.")
            raise ValueError("Placeholders defined but no reference data provided.")

        results = []
        if reference_data:
            final_system = validate_and_replace_placeholders(system_prompt, reference_data)
            final_user = validate_and_replace_placeholders(user_prompt, reference_data)
            for _ in range(num_executions):
                # Wrap in try-except when calling the LLM
                try:
                    responses = self.llm.generate(final_system, final_user, num_return_sequences, max_new_tokens)
                    for resp in responses:
                        results.append(GeneratedResult(resp))
                except Exception as e:
                    logger.exception(f"Error generating text: {str(e)}")
                    raise RuntimeError(f"Error generating text: {str(e)}")
        else:
            for _ in range(num_executions):
                try:
                    responses = self.llm.generate(system_prompt, user_prompt, num_return_sequences, max_new_tokens)
                    for resp in responses:
                        results.append(GeneratedResult(resp))
                except Exception as e:
                    logger.exception(f"Error generating text: {str(e)}")
                    raise RuntimeError(f"Error generating text: {str(e)}")

        logger.info(f"Generated {len(results)} results")
        return results