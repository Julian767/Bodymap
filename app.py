"""Aplicación web Flask del proyecto BodyMap."""
import os

from flask import Flask, render_template, request

from bot_telegram.config import BOT_USERNAME
from bot_telegram.responses import get_response

app = Flask(__name__)


@app.context_processor
def inject_bot_data():
    """Expone el usuario del bot a todas las plantillas."""
    return {
        "bot_username": BOT_USERNAME,
        "bot_url": f"https://t.me/{BOT_USERNAME}",
    }


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/mapa")
def mapa():
    return render_template("mapa.html")


@app.route("/recomendaciones")
def recomendaciones():
    return render_template("recomendaciones.html")


@app.route("/informacion")
def informacion():
    return render_template("informacion.html")


@app.route("/asistente", methods=["GET", "POST"])
def asistente():
    respuesta = ""
    sintoma = ""

    if request.method == "POST":
        sintoma = request.form.get("sintoma", "").strip()
        if sintoma:
            respuesta = get_response(sintoma)

    return render_template("asistente.html", respuesta=respuesta, sintoma=sintoma)


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
