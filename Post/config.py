import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    #SQLALCHEMY_DATABASE_URI ="postgresql://postgres:LosAndes1234@localhost:5432/routes"
    
    #SQLALCHEMY_DATABASE_URI ="postgresql://postgres:LosAndes1234@localhost:5434/posts"
    

    #SQLALCHEMY_TEST_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@localhost:5432/test_posts")
    #SQLALCHEMY_TEST_DATABASE_URI = "postgresql://postgres:LosAndes1234@localhost:5434/posts"
    SQLALCHEMY_TRACK_MODIFICATIONS = False