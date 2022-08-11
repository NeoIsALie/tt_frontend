from app.main import app
from app.config import DEBUG


if __name__ == '__main__':
    app.run_server(debug=DEBUG)
