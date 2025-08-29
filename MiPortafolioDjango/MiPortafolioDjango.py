import reflex as rx
from .state import State
from MiPortafolioDjango.components.titulo_card import titulo_card
from MiPortafolioDjango.components.basic_menu import basic_menu
from MiPortafolioDjango.components.sobre_mi import sobre_mi
from MiPortafolioDjango.components.carrusel_projects import carrusel_projects
from MiPortafolioDjango.components.skills_carousel import skills_carousel
from MiPortafolioDjango.components.contact_card import contact_card
from MiPortafolioDjango.components.footer_card import footer_card
from MiPortafolioDjango.components.section_title import section_title
from MiPortafolioDjango.components.button_group import button_group
from MiPortafolioDjango.components.section_title import section_title

# 🌀 Loader y errores
def loading_view():
    return rx.center(
        rx.spinner(size="3", color="orange.500"),
        rx.text("Cargando datos...", mt=4, color="gray.300"),
        height="80vh"
    )

def error_view():
    return rx.center(
        rx.text(State.error, color="red.500", font_weight="bold"),
        height="80vh"
    )

# 🧩 Secciones condicionales
def proyectos_section():
    return rx.box(
        section_title("Proyectos destacados"),
        rx.cond(
            ~State.loading,
            rx.cond(
                State.projects,
                carrusel_projects(State.projects),
                rx.text("¡Pronto añadiré más proyectos!", text_align="center", color="gray.500")
            ),
            rx.spinner(size="3", color="orange.500")
        ),
        id="Proyectos"
    )

def habilidades_section():
    return rx.box(
        section_title("Habilidades destacadas"),
        rx.cond(
            ~State.loading,
            rx.cond(
                State.skills,
                skills_carousel(State.skills),
                rx.text("¡Pronto añadiré más habilidades!", text_align="center", color="gray.500")
            ),
            rx.spinner(size="3", color="orange.500")
        ),
        id="Habilidades"
    )

def contacto_section():
    return rx.box(
        section_title("Contacto"),
        contact_card(),
        id="Contactame"
    )

# 🏠 Página principal
def index():
    return rx.theme(
        rx.box(
            rx.vstack(
                rx.cond(
                    State.loading,
                    loading_view(),
                    rx.cond(
                        State.error,
                        error_view(),
                        rx.vstack(
                            titulo_card(),
                            button_group(),
                            rx.box(sobre_mi(), id="Sobre-mi"),
                            proyectos_section(),
                            habilidades_section(),
                            contacto_section(),
                            rx.spacer(height="64px"),
                            footer_card(),
                            spacing="6",
                            align="stretch"
                        )
                    )
                )
            ),
            max_w="960px",
            mx="auto",
            px=4,
            py=12,
        ),
        appearance="dark",
        accent_color="orange",
        on_load=State.on_load,
    )

app = rx.App(
    style={
        "font_family": "Inter, sans-serif",
        "background_color": "black",
        "color": "white",
    },
    theme=rx.theme(
        appearance="dark",
        accent_color="orange",
    ),
)

app.add_page(index, route="/", title="Mi Portafolio — Nicolás Cano")
