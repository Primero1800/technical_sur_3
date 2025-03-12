import os
import sys
from pathlib import Path

from pydantic import BaseModel
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


class AppRunConfig(CustomSettings):
    app_path: str
    app_host: str
    app_port: int
    app_reload: bool


class AppSettings(CustomSettings):
    APP_BASE_DIR: str = str(Path(__file__).resolve().parent.parent)
    APP_TITLE: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    API_PREFIX: str
    API_V1_PREFIX: str

    APP_422_CODE_STATUS: int


class SwaggerSettings(BaseModel):
    pass


class AccessTokenSettings(CustomSettings):
    ACCESS_TOKEN_LIFETIME: int
    RESET_PASSWORD_TOKEN_SECRET: str
    VERIFICATION_TOKEN_SECRET: str


class Tags(CustomSettings):
    TECH_TAG: str
    ROOT_TAG: str
    SWAGGER_TAG: str
    AUTH_TAG: str
    AUTH_PREFIX: str
    JWT_AUTH_TAG: str
    USERS_TAG: str
    USERS_PREFIX: str


class DB(CustomSettings):

    DB_NAME: str = os.getenv('DB_NAME_TEST') if 'pytest' in sys.modules else os.getenv('DB_NAME')
    DB_NAME_TEST: str
    DB_ENGINE: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    DB_TABLE_PREFIX: str

    DB_ECHO_MODE: bool
    DB_POOL_SIZE: int

    DB_URL: str = ''
    DB_TEST_URL: str = ''

    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


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


class Auth(CustomSettings):
    @property
    def TRANSPORT_TOKEN_URL(self) -> str:
        return "{}{}{}/login".format(
            settings.app.API_PREFIX,
            settings.app.API_V1_PREFIX,
            settings.tags.AUTH_PREFIX,
        )


class RunConfig(BaseModel):
    app1: AppRunConfig = AppRunConfig()


class Settings(CustomSettings):
    app: AppSettings = AppSettings()
    swagger: SwaggerSettings = SwaggerSettings()
    tags: Tags = Tags()
    run: RunConfig = RunConfig()
    db: DB = DB()
    access_token: AccessTokenSettings = AccessTokenSettings()
    # auth_jwt: AuthJWT = AuthJWT()
    auth: Auth = Auth()


settings = Settings()


def get_db_connection(db_name: str) -> str:
    return '{}://{}:{}@{}:{}/{}'.format(
        settings.db.DB_ENGINE,
        settings.db.DB_USER,
        settings.db.DB_PASSWORD,
        settings.db.DB_HOST,
        settings.db.DB_PORT,
        db_name,
    )


settings.db.DB_URL = get_db_connection(settings.db.DB_NAME)
settings.db.DB_TEST_URL = get_db_connection(settings.db.DB_NAME_TEST)
