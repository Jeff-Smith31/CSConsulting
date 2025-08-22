import os
from datetime import timedelta
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "CodeSmith Consulting API")
    environment: str = os.getenv("ENV", "development")

    # CORS
    allowed_origins: list[str] = (
        os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
        .split(",")
        if os.getenv("ALLOWED_ORIGINS")
        else ["http://localhost:5173", "http://localhost:3000"]
    )

    # Security / JWT
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me-in-prod")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expires_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", "60"))
    refresh_token_expires_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRES_DAYS", "7"))

    # DynamoDB
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_access_key_id: str | None = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")
    dynamodb_endpoint_url: str | None = os.getenv("DYNAMODB_ENDPOINT_URL")  # for local testing

    # Rate limiting
    rate_limit: str = os.getenv("RATE_LIMIT", "100/minute")

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.access_token_expires_minutes)

    @property
    def refresh_token_expires(self) -> timedelta:
        return timedelta(days=self.refresh_token_expires_days)

# Admin configuration: comma-separated list of admin emails
class AdminSettings(BaseModel):
    admin_emails: list[str] = (
        os.getenv("ADMIN_EMAILS", "").split(",") if os.getenv("ADMIN_EMAILS") else []
    )


settings = Settings()
admin_settings = AdminSettings()

# Sensible defaults for local DynamoDB when developing
try:
    if settings.environment.lower() == "development":
        if not settings.dynamodb_endpoint_url:
            settings.dynamodb_endpoint_url = "http://localhost:8000"
        # If pointing to local dynamodb and creds are missing, set local placeholders
        if settings.dynamodb_endpoint_url and "localhost:8000" in settings.dynamodb_endpoint_url:
            if not settings.aws_access_key_id:
                settings.aws_access_key_id = "local"
            if not settings.aws_secret_access_key:
                settings.aws_secret_access_key = "local"
except Exception:
    # Fail open: if anything goes wrong, leave settings as-is
    pass
