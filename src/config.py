from pydantic_settings import BaseSettings, SettingsConfigDict
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
# env_file_path = os.path.join(current_dir, "..", ".env")
env_file_path = os.path.join(current_dir, "..", "dev.env")

class Settings(BaseSettings):
    app_title: str
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_default_vhost: str
    rabbitmq_user: str
    rabbitmq_pass: str
    rabbitmq_vhost: str
    QUEUE_NAME: str
    RABBITMQ_HOST: str
    rabbitmq_api_port: int
    RABBITMQ_AMQP_PORT: int
    model_config=SettingsConfigDict(env_file=env_file_path)

settings = Settings()
