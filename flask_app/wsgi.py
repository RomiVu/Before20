from application import create_app
from config import DevelopmentConfig, ProductionConfig

app = create_app(DevelopmentConfig)

# if __name__ == "__main__":
#     app.run("127.0.0.1:3000", debug=True)