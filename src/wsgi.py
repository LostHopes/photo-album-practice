from app import create_app
from app import config


app = create_app(config.ProdConfig)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
