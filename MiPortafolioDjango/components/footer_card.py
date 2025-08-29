# mi_portafolio/components/footer_card.py
import reflex as rx
from MiPortafolioDjango.styles import footer_card_styles

def footer_card():
    return rx.box(
        rx.vstack(
            rx.text("Mi Portafolio", font_size="lg", font_weight="bold"),
            rx.hstack(
                rx.link(
                    rx.icon(tag="github", size=32),
                    href="https://github.com/NicolasAndresCL",
                    is_external=True
                ),
                rx.link(
                    rx.icon(tag="linkedin", size=32),
                    href="https://www.linkedin.com/in/nicolascano-leal",
                    is_external=True
                ),
                spacing="4"
            ),
            rx.text(
                "© 2025 Nicolás Andrés Cano Leal™. All Rights Reserved.",
                font_size="xs",
                text_align="center"
            ),
            spacing="4"
        ),
        **footer_card_styles
    )