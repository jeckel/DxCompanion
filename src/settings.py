from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    __app_name__ = 'Project Manager'
    # pocket_consumer_key: str = Field()
    # pocket_access_token: str = Field('')
    # pocket_username: str = Field('')
    # mastodon_access_token: str = Field('')
    # mastodon_api_url: str = Field('')


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())