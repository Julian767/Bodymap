from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/recomendaciones')
def recomendaciones():
    return render_template('recomendaciones.html')

@app.route('/asistente', methods=['GET', 'POST'])
def asistente():
    respuesta = ""
    if request.method == 'POST':
        sintoma = request.form['sintoma'].lower()
        if "cabeza" in sintoma:
            respuesta = "Podría ser tensión o estrés. Se recomienda descanso y buena hidratación."
        elif "espalda" in sintoma:
            respuesta = "Puede deberse a mala postura. Realice estiramientos suaves."
        else:
            respuesta = "Sintoma no reconocido. Consulte un profesional si persiste."
    return render_template('asistente.html', respuesta=respuesta)

@app.route('/informacion')
def informacion():
    return render_template('informacion.html')

if __name__ == '__main__':
    app.run(debug=True)
