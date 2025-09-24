from pydantic_settings import BaseSettings, SettingsConfigDict
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
env_file_path = os.path.join(current_dir, "..", ".env")

class Settings(BaseSettings):
    app_title: str
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_default_vhost: str
    rabbitmq_user: str
    rabbitmq_pass: str
    rabbitmq_vhost: str
    queue_name: str
    rabbitmq_host: str
    rabbitmq_api_port: int
    model_config=SettingsConfigDict(env_file=env_file_path)

settings = Settings()
