from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            '.env.app1.template', '.env.app1', 'app1/.env.app1.template', 'app1/.env.app1',
        ),
        case_sensitive=False,
        extra='allow',
        env_prefix='',
        env_nested_delimiter='',
    )
