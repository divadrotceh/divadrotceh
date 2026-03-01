from app import app
import views
import auth

if __name__ == "__main__":
    app.secret_key = "dev‑key‑change‑me-after-testing"
    app.register_blueprint(views.bp)
    app.register_blueprint(auth.bp)
    app.run(debug = True)
