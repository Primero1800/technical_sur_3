import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv('../.env.app1', override=False)
load_dotenv('.env.app1', override=False)


class AppRunConfig(BaseModel):
    app_path: str
    app_host: str
    app_port: int
    app_reload: bool


class AppSettings(BaseModel):
    APP_BASE_DIR: str = Path(__file__).resolve().parent.parent
    APP_TITLE: str = os.getenv('APP_TITLE')
    APP_VERSION: str = os.getenv('APP_VERSION')
    APP_DESCRIPTION: str = os.getenv('APP_DESCRIPTION')

    API_PREFIX: str = os.getenv('API_PREFIX')
    API_V1_PREFIX: str = API_PREFIX + os.getenv('API_V1_PREFIX')

    APP_422_CODE_STATUS: int = int(os.getenv('APP_422_CODE_STATUS'))


class SwaggerSettings(BaseModel):
    pass


class Tags(BaseModel):
    TECH_TAG: str = os.getenv('TECH_TAG')
    ROOT_TAG: str = None
    SWAGGER_TAG: str = os.getenv('SWAGGER_TAG')
    AUTH_TAG: str = os.getenv('AUTH_TAG')
    JWT_AUTH_TAG: str = os.getenv('JWT_AUTH_TAG')


class DB(BaseModel):

    DB_NAME: str = os.getenv('DB_NAME_TEST') if 'pytest' in sys.modules else os.getenv('DB_NAME')
    DB_ENGINE: str = os.getenv('DB_ENGINE')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = int(os.getenv('DB_PORT'))

    DB_TABLE_PREFIX: str = os.getenv('DB_TABLE_PREFIX')

    DB_ECHO_MODE: bool = True if os.getenv('DB_ECHO_MODE') == 'True' else False
    DB_POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE'))

    DB_URL: str = None


# class AuthJWT(BaseModel):
#     private_key = AppSettings.APP_BASE_DIR / "src" / "core" / "config"/"certs"/"jwt-private.pem"
#     public_key = AppSettings.APP_BASE_DIR / "src" / "core" / "config"/"certs"/"jwt-public.pem"
#     algorithm = os.getenv('JWT_ALGORYTHM')
#     token_type_field = os.getenv('TOKEN_TYPE_FIELD')
#     access_token_expire_minutes = float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
#     refresh_token_expire_minutes = float(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES'))
#     access_token_type = os.getenv('ACCESS_TOKEN_TYPE')
#     refresh_token_type = os.getenv('REFRESH_TOKEN_TYPE')
#     default_password = os.getenv('DEFAULT_PASSWORD')


class RunConfig(BaseModel):
    app1: AppRunConfig = AppRunConfig(
        app_path=os.getenv('APP_PATH'),
        app_host=os.getenv('APP_HOST'),
        app_port=int(os.getenv('APP_PORT')),
        app_reload=True if os.getenv('APP_RELOAD') == 'True' else False,
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env.app1',
        case_sensitive=False,
        extra='ignore',
    )
    app: AppSettings = AppSettings()
    swagger: SwaggerSettings = SwaggerSettings()
    tags: Tags = Tags()
    run: RunConfig = RunConfig()
    db: DB = DB()
    test: str
    # auth_jwt: AuthJWT = AuthJWT()


settings = Settings()


def get_db_connection() -> str:
    return '{}://{}:{}@{}:{}/{}'.format(
        settings.db.DB_ENGINE,
        settings.db.DB_USER,
        settings.db.DB_PASSWORD,
        settings.db.DB_HOST,
        settings.db.DB_PORT,
        settings.db.DB_NAME,
    )


settings.db.DB_URL = get_db_connection()
