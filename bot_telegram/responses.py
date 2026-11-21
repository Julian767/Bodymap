"""Motor de respuestas por palabras clave del asistente BodyMap."""
import re
import unicodedata

RESPUESTA_POR_DEFECTO = (
    "No pude identificar esa zona o síntoma en mi base orientativa. "
    "Probá indicándome una zona específica como cabeza, cuello, espalda, "
    "pecho, abdomen, brazo o pierna."
)

# (palabras clave, respuesta). El orden define el desempate: gana la primera.
RESPUESTAS = (
    (
        ("hola", "holis", "buenos", "dias", "buenas", "tardes", "noches", "hi"),
        "¡Hola! Bienvenido al asistente virtual de BodyMap. Contame qué zona del "
        "cuerpo te molesta (cabeza, cuello, espalda, pecho, abdomen, brazos o "
        "piernas) para brindarte orientación general.",
    ),
    (
        ("adios", "chao", "chau", "saludos", "hasta", "luego", "bye", "gracias"),
        "¡De nada! Recordá que esta información es orientativa. Ante cualquier "
        "duda o molestia persistente, consultá a un médico. ¡Hasta luego!",
    ),
    (
        ("quien", "sos", "eres", "nombre", "bodymap", "hacen", "sirve"),
        "Soy el asistente virtual de BodyMap, un sistema interactivo educativo "
        "sobre anatomía humana, causas frecuentes de dolores cotidianos y "
        "recomendaciones generales de bienestar.",
    ),
    (
        ("cabeza", "cefalea", "migrana", "mareo", "frente", "sien"),
        "Dolor de cabeza: suele asociarse a tensión muscular, estrés, fatiga "
        "visual por pantallas o deshidratación. Recomendación general: descansá "
        "en un lugar tranquilo, hidratate bien y reducí el brillo de pantallas.",
    ),
    (
        ("cuello", "cervical", "torticolis", "nuca", "rigidez"),
        "Molestia en el cuello: generalmente se debe a malas posturas o uso "
        "prolongado del celular y la computadora. Recomendación general: "
        "realizá pausas activas y estiramientos cervicales suaves sin forzar.",
    ),
    (
        ("espalda", "lumbalgia", "lumbar", "cintura", "columna", "contractura"),
        "Dolor de espalda: suele originarse por mala postura al sentarse, "
        "sedentarismo o esfuerzos físicos. Recomendación general: mantené la "
        "espalda recta, aplicá calor local suave y hacé estiramientos ligeros.",
    ),
    (
        ("pecho", "torax", "respirar", "ansiedad", "opresion"),
        "Molestia en el pecho: puede deberse a tensión muscular o ansiedad, "
        "aunque siempre requiere precaución. Si el dolor es fuerte, opresivo o "
        "se acompaña de falta de aire, acudí de inmediato a una guardia médica.",
    ),
    (
        (
            "abdomen",
            "estomago",
            "panza",
            "colico",
            "gastritis",
            "digestion",
        ),
        "Molestia abdominal: frecuentemente relacionada con digestión pesada, "
        "gastritis o estrés. Recomendación general: optá por comidas livianas, "
        "evitá irritantes y mantenete hidratado.",
    ),
    (
        (
            "brazo",
            "brazos",
            "hombro",
            "muneca",
            "tendinitis",
            "pierna",
            "piernas",
            "calambre",
            "calambres",
            "muscular",
        ),
        "Molestia muscular en extremidades: suele ocurrir por fatiga física, "
        "movimientos repetitivos o falta de hidratación. Recomendación general: "
        "descansá la zona, hidratate y realizá elongación suave.",
    ),
    (
        ("help", "ayuda", "ayudas", "tengo", "un", "problema", "dolor", "sintoma"),
        "Para ayudarte mejor, escribime qué zona del cuerpo te duele (por "
        'ejemplo: "me duele la cabeza", "tengo contractura en la espalda" o '
        '"dolor de cuello").',
    ),
)

_PALABRA = re.compile(r"[\w']+|[.,!?;]")


def _normalizar(texto):
    """Minúsculas sin tildes, para que 'migraña' y 'migrana' sean iguales."""
    descompuesto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(caracter for caracter in descompuesto if not unicodedata.combining(caracter))


_CLAVES = tuple(
    frozenset(_normalizar(palabra) for palabra in palabras)
    for palabras, _ in RESPUESTAS
)


def get_response(message):
    """Devuelve la mejor respuesta para un mensaje del usuario."""
    tokens = _PALABRA.findall(_normalizar(message))
    puntajes = [sum(token in claves for token in tokens) for claves in _CLAVES]
    mejor_puntaje = max(puntajes, default=0)

    if mejor_puntaje == 0:
        return RESPUESTA_POR_DEFECTO

    return RESPUESTAS[puntajes.index(mejor_puntaje)][1]
