import os
import time
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai", "gemini"] = "gemini"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self, max_retries: int = 3, retry_delay: int = 5):
        """
        Load and return the LLM model with retry logic for rate limits.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        
        for attempt in range(max_retries):
            try:
                if self.model_provider == "groq":
                    print("Loading LLM from Groq...")
                    groq_api_key = os.getenv("GROQ_API_KEY")
                    model_name = self.config["llm"]["groq"]["model_name"]
                    llm = ChatGroq(
                        model=model_name, 
                        api_key=groq_api_key,
                        temperature=0.7,
                        max_retries=3
                    )
                elif self.model_provider == "openai":
                    print("Loading LLM from OpenAI...")
                    openai_api_key = os.getenv("OPENAI_API_KEY")
                    model_name = self.config["llm"]["openai"]["model_name"]
                    llm = ChatOpenAI(
                        model_name=model_name, 
                        api_key=openai_api_key,
                        max_retries=3
                    )
                elif self.model_provider == "gemini":
                    print("Loading LLM from Google Gemini...")
                    google_api_key = os.getenv("GOOGLE_API_KEY")
                    model_name = self.config["llm"]["gemini"]["model_name"]
                    llm = ChatGoogleGenerativeAI(
                        model=model_name,
                        google_api_key=google_api_key,
                        temperature=0.7,
                        max_retries=3
                    )
                
                return llm
                
            except Exception as e:
                if "rate" in str(e).lower() or "429" in str(e):
                    print(f"Rate limit hit, waiting {retry_delay}s before retry {attempt + 1}/{max_retries}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise e
        
        # If all retries failed, still return the LLM (error will be handled at request time)
        return llm