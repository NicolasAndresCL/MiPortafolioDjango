# mi_portafolio/components/titulo_card.py
import reflex as rx
from .basic_menu import basic_menu
from MiPortafolioDjango.styles import titulo_card_styles

def titulo_card() -> rx.Component:
    return rx.box(
        rx.box(
            rx.box(
                rx.heading(
                    "Portafolio de Nicolás Andrés Cano Leal",
                    size="1",  # Cambiado de "lg" a "1" para el tamaño más grande
                    font_weight="bold",
                    class_name="text-4xl sm:text-5xl font-bold tracking-tight text-white"
                ),
                rx.text(
                    "Desarrollador Backend Python con experiencia en la construcción de APIs robustas y escalables.",
                    font_size="lg",
                    color="slate.300"
                ),
                rx.hstack(
                    rx.box(
                        rx.image(
                            src="/static/perfil-foto-nc.png",
                            alt="Foto de Nicolás Cano",
                            class_name="rounded-full w-32 h-32 object-cover border-4 border-orange-500 shadow-md"
                        ),
                    ),
                    rx.vstack(
                        basic_menu(),
                        rx.link(
                            "Descargar CV →",
                            href="/static/NicolasCano_BackendDeveloper_CV.pdf",
                            download=True,
                            font_weight="bold",
                            class_name="text-orange-500 hover:text-orange-400 transition transform hover:scale-105"
                        ),
                        align="center",
                        spacing="4"
                    ),
                    justify="center",
                    spacing="8",
                    py="8"
                ),
                spacing="6",
                align="center"
            ),
            class_name="bg-slate-800 rounded-3xl shadow-2xl border border-slate-700 p-8"
        ),
        **titulo_card_styles
    )
