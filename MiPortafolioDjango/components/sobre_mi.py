# mi_portafolio/components/sobre_mi.py
import reflex as rx
from MiPortafolioDjango.styles import sobre_mi_styles

def sobre_mi():
    return rx.box(
        rx.vstack(
            rx.heading("Sobre mí", size="4"),
            rx.text(
                "Desarrollador backend autodidacta con vocación por la arquitectura modular, la escalabilidad y la documentación profesional. Me especializo en Django, DRF, FastAPI, Flask y APIs RESTful...",
                font_size="sm",
                color="gray.300"
            ),
            rx.text(
                "En transición hacia data engineering, enfoco mis avances en soluciones limpias, testeables y listas para producción...",
                font_size="sm",
                color="gray.300"
            ),
            spacing="4",
            align="start"
        ),
        style=sobre_mi_styles
    )

# mi_portafolio/styles.py
sobre_mi_styles = {
    "bg": "rgb(15, 23, 42)",
    "color": "white",
    "rounded": "xl",
    "shadow": "md",
    "p": "8"
}