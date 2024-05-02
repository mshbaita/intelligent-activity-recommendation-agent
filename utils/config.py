from pydantic import BaseSettings


class ConfigBase(BaseSettings):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


config = ConfigBase()
