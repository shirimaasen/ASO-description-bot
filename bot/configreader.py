from pydantic import BaseSettings, Field, RedisDsn, AnyHttpUrl


class Config(BaseSettings):
    bot_token: str = Field(..., env='BOT_TOKEN')
    gpt_url: AnyHttpUrl = Field(..., env='GPT_URL')
    webhook_domain: AnyHttpUrl | None = Field(None, env='WEBHOOK_DOMAIN')
    webhook_path: str = Field("/webhook/SOIDH89asjof86hdso-kdsnfm4kwenr", env='WEBHOOK_PATH')
    redis_dsn: RedisDsn | None = Field(None, env='REDIS_URL')
    app_port: int = Field(5000, env="PORT")
    app_host: str = Field("0.0.0.0", env="HOST")


config = Config()
