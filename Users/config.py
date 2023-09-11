import os


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
    SQLALCHEMY_TEST_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL", f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@localhost:5432/test_users")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
