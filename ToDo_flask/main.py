from app import app
from views import bp

if __name__ == "__main__":
    app.secret_key = "jdkfosvns"
    app.register_blueprint(bp)
    app.run(debug = True)
