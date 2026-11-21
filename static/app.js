/* Comportamiento compartido por todas las páginas de BodyMap. */
const CLAVE_TEMA = "modoOscuro";

const INFO_ZONAS = {
    cabeza: "Funciones: alberga el cerebro y órganos sensoriales.\nDolores frecuentes: cefaleas, migrañas.\nCausas comunes: estrés, tensión ocular, deshidratación.",
    cuello: "Funciones: conecta cabeza y tronco, permite movilidad.\nDolores frecuentes: rigidez cervical, tortícolis.\nCausas comunes: mala postura, uso prolongado de pantallas.",
    pecho: "Funciones: protege corazón y pulmones.\nDolores frecuentes: tensión muscular, molestias respiratorias.\nCausas comunes: ansiedad, esfuerzo físico.",
    abdomen: "Funciones: contiene órganos digestivos.\nDolores frecuentes: cólicos, gastritis.\nCausas comunes: mala alimentación, estrés.",
    brazo: "Funciones: movilidad y fuerza.\nDolores frecuentes: tendinitis, dolor muscular.\nCausas comunes: sobreuso, esfuerzo repetitivo.",
    pierna: "Funciones: soporte y desplazamiento.\nDolores frecuentes: calambres, dolor muscular.\nCausas comunes: fatiga, falta de hidratación.",
    default: "Haz clic en una parte del cuerpo para ver información detallada."
};

function toggleDarkMode() {
    const activo = document.documentElement.classList.toggle("dark-mode");
    localStorage.setItem(CLAVE_TEMA, activo ? "activado" : "desactivado");
    actualizarBotonTema(activo);
}

function actualizarBotonTema(activo) {
    const boton = document.getElementById("boton-tema");
    if (!boton) return;
    boton.textContent = activo ? "Modo Claro" : "Modo Oscuro";
    boton.setAttribute("aria-pressed", String(activo));
}

function mostrarInfo(zona) {
    const destino = document.getElementById("infoZona");
    if (!destino) return;
    destino.textContent = INFO_ZONAS[zona] || INFO_ZONAS.default;
}

document.addEventListener("DOMContentLoaded", () => {
    actualizarBotonTema(document.documentElement.classList.contains("dark-mode"));

    document.querySelectorAll("[data-zone]").forEach((elemento) => {
        elemento.addEventListener("click", () => mostrarInfo(elemento.dataset.zone));
        elemento.addEventListener("keydown", (evento) => {
            if (evento.key === "Enter" || evento.key === " ") {
                evento.preventDefault();
                mostrarInfo(elemento.dataset.zone);
            }
        });
    });
});
