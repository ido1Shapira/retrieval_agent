from typing import List, Optional, Any

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM, BaseLLM
from langchain_google_genai import GoogleGenerativeAI


class LLMClient(LLM):
    model_name: str = None
    client: BaseLLM = None

    def __init__(self,
                 model_name: str,
                 temperature: float,
                 api_key: Optional[str]):
        super().__init__(model_name=model_name, temperature=temperature)
        self.client = GoogleGenerativeAI(temperature=temperature,
                                         google_api_key=api_key,
                                         model=model_name)

    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
        return self.client(prompt, stop, run_manager, **kwargs)

    @property
    def _llm_type(self) -> str:
        return self.model_name
