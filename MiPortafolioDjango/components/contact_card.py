# mi_portafolio/components/contact_card.py

import reflex as rx
from MiPortafolioDjango.state import State
from ..styles import contact_card_styles

def contact_card() -> rx.Component:
    """Componente de contacto con formulario controlado."""
    return rx.box(
        rx.vstack(
            rx.text(
                "¿Tienes preguntas o quieres colaborar? ¡Escríbeme!",
                font_size="sm",
                color="gray.300"
            ),
            rx.form(
                rx.vstack(
                    rx.text("Nombre", font_size="sm", color="gray.400"),
                    rx.input(
                        name="name",
                        value=State.form_data.name,
                        on_change=lambda e: State.handle_change("name", e),
                        placeholder="Tu nombre",
                        is_required=True
                    ),
                    rx.text("Email", font_size="sm", color="gray.400"),
                    rx.input(
                        name="email",
                        type="email",
                        value=State.form_data.email,
                        on_change=lambda e: State.handle_change("email", e),
                        placeholder="Tu correo",
                        is_required=True
                    ),
                    rx.text("Mensaje", font_size="sm", color="gray.400"),
                    rx.text_area(
                        name="message",
                        value=State.form_data.message,
                        on_change=lambda e: State.handle_change("message", e),
                        placeholder="Tu mensaje",
                        rows="5",
                        is_required=True
                    ),
                    rx.button("Enviar mensaje", type="submit", color_scheme="teal"),
                    spacing="4"
                ),
                on_submit=State.handle_submit
            ),
            spacing="6",
            align="stretch"
        ),
        **contact_card_styles
    )
