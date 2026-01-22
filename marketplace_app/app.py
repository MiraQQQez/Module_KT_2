from __future__ import annotations

from dataclasses import dataclass

from flask import Flask, redirect, render_template, request, session, url_for


@dataclass(frozen=True)
class DemoUser:
    """Тестовый пользователь демо-маркетплейса."""

    email: str
    password: str


def create_app() -> Flask:
    """Фабрика Flask-приложения."""

    app = Flask(__name__)
    app.secret_key = "demo-marketplace-secret"

    demo_user = DemoUser(email="user@example.com", password="Password123!")

    def is_authenticated() -> bool:
        return bool(session.get("user_email"))

    @app.get("/")
    def index():
        if is_authenticated():
            return redirect(url_for("profile"))
        return redirect(url_for("login"))

    @app.get("/login")
    def login():
        if is_authenticated():
            return redirect(url_for("profile"))

        msg = (request.args.get("msg") or "").strip().lower()
        info_message = "Вы вышли из системы" if msg == "logged_out" else ""
        return render_template(
            "login.html", error_message="", info_message=info_message
        )

    @app.post("/login")
    def login_post():
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""

        if not email or not password:
            return render_template(
                "login.html",
                error_message="Поля email и пароль обязательны",
                info_message="",
            )

        if email != demo_user.email or password != demo_user.password:
            return render_template(
                "login.html",
                error_message="Неверный email или пароль",
                info_message="",
            )

        session["user_email"] = email
        return redirect(url_for("profile"))

    @app.get("/profile")
    def profile():
        if not is_authenticated():
            return redirect(url_for("login"))

        return render_template("profile.html", user_email=session.get("user_email"))

    @app.post("/logout")
    def logout():
        session.pop("user_email", None)
        return redirect(url_for("login", msg="logged_out"))

    return app
