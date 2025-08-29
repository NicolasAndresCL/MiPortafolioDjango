# mi_portafolio/components/contact_card.py

import reflex as rx
from MiPortafolioDjango.state import State
from ..styles import contact_card_styles

def contact_card() -> rx.Component:
    """Componente de contacto con formulario controlado."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "¿Tienes preguntas o quieres colaborar?",
                size="4",
                color="orange.500",
                text_align="center"
            ),
            rx.text(
                "¡Escríbeme un mensaje y me pondré en contacto contigo!",
                font_size="sm",
                color="gray.300",
                text_align="center"
            ),
            rx.form(
                rx.vstack(
                    rx.vstack(
                        rx.text("Nombre", color="gray.300", as_="label", for_="name"),
                        rx.input(
                            id="name",
                            name="name",
                            value=State.form_data.name,
                            on_change=lambda e: State.handle_change("name", e),
                            placeholder="Tu nombre completo",
                            is_required=True,
                            bg="slate.700",
                            border_color="slate.600"
                        ),
                    ),
                    rx.vstack(
                        rx.text("Email", color="gray.300", as_="label", for_="email"),
                        rx.input(
                            name="email",
                            type="email",
                            value=State.form_data.email,
                            on_change=lambda e: State.handle_change("email", e),
                            placeholder="tu.email@ejemplo.com",
                            is_required=True,
                            bg="slate.700",
                            border_color="slate.600"
                        ),
                    ),
                    rx.vstack(
                        rx.text("Mensaje", color="gray.300", as_="label", for_="message"),
                        rx.text_area(
                            id="message",
                            name="message",
                            value=State.form_data.message,
                            on_change=lambda e: State.handle_change("message", e),
                            placeholder="Escribe tu mensaje aquí...",
                            rows="5",
                            is_required=True,
                            bg="slate.700",
                            border_color="slate.600"
                        ),
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="send"),
                            rx.text("Enviar mensaje"),
                            spacing="2"
                        ),
                        type="submit",
                        color_scheme="orange",
                        width="full"
                    ),
                    spacing="4"
                ),
                on_submit=State.handle_submit
            ),
            spacing="6",
            align="stretch"
        ),
        **contact_card_styles
    )
