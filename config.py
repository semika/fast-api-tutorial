from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    agent_arn: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    opensearch_host: str
    opensearch_user: str
    opensearch_password: str

    class Config:
        env_file = ".env"

settings = Settings()
