import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings:
    APP_BASE_DIR = Path(__file__).resolve().parent.parent.parent
    APP_TITLE: str = os.getenv('APP_TITLE')
    APP_VERSION: str = os.getenv('APP_VERSION')
    APP_DESCRIPTION: str = os.getenv('APP_DESCRIPTION')

    API_PREFIX = os.getenv('API_PREFIX')
    API_V1_PREFIX = API_PREFIX + os.getenv('API_V1_PREFIX')

    APP_422_CODE_STATUS: int = int(os.getenv('APP_422_CODE_STATUS'))


class SwaggerSettings:
    pass


class Tags:
    TECH_TAG = os.getenv('APP1_TECH_TAG')
    # USERS_TAG = os.getenv('USERS_TAG')
    ROOT_TAG = os.getenv('APP1_ROOT_TAG')
    SWAGGER_TAG = os.getenv('APP1_SWAGGER_TAG')
    # PRODUCTS_TAG = os.getenv('PRODUCTS_TAG')
    AUTH_TAG = os.getenv('APP1_AUTH_TAG')
    JWT_AUTH_TAG = os.getenv('APP1_JWT_AUTH_TAG')


# class DB:
#
#     DB_NAME = os.getenv('DB_NAME_TEST') if 'pytest' in sys.modules else os.getenv('DB_NAME')
#     DB_ENGINE = os.getenv('DB_ENGINE')
#     DB_USER = os.getenv('DB_USER')
#     DB_PASSWORD = os.getenv('DB_PASSWORD')
#     DB_HOST = os.getenv('DB_HOST')
#     DB_PORT = os.getenv('DB_PORT')
#
#     DB_TABLE_PREFIX = os.getenv('DB_TABLE_PREFIX')
#
#     DB_ECHO_MODE = True if os.getenv('DB_ECHO_MODE') == 'True' else False
#
#     DB_URL = None


# class AuthJWT:
#     private_key = AppSettings.APP_BASE_DIR / "src" / "core" / "config"/"certs"/"jwt-private.pem"
#     public_key = AppSettings.APP_BASE_DIR / "src" / "core" / "config"/"certs"/"jwt-public.pem"
#     algorithm = os.getenv('JWT_ALGORYTHM')
#     token_type_field = os.getenv('TOKEN_TYPE_FIELD')
#     access_token_expire_minutes = float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
#     refresh_token_expire_minutes = float(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES'))
#     access_token_type = os.getenv('ACCESS_TOKEN_TYPE')
#     refresh_token_type = os.getenv('REFRESH_TOKEN_TYPE')
#     default_password = os.getenv('DEFAULT_PASSWORD')


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    swagger: SwaggerSettings = SwaggerSettings()
    tags: Tags = Tags()
    # db: DB = DB()
    # auth_jwt: AuthJWT = AuthJWT()


settings = Settings()


# def get_db_connection():
#     return '{}://{}:{}@{}:{}/{}'.format(
#         settings.db.DB_ENGINE,
#         settings.db.DB_USER,
#         settings.db.DB_PASSWORD,
#         settings.db.DB_HOST,
#         settings.db.DB_PORT,
#         settings.db.DB_NAME,
#     )
#
#
# settings.db.DB_URL = get_db_connection()