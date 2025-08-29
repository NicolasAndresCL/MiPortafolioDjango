# section_title.py
import reflex as rx
from ..styles import section_title_styles

def section_title(text: str) -> rx.Component:
    """Componente reutilizable para títulos de sección."""
    return rx.box(
        rx.heading(
            text,
            size="2",  # Usando el formato correcto de tamaño
            color="orange.500",
            text_align="center",
            font_weight="bold",
            mb="6"  # Margin bottom para espaciado consistente
        ),
        **section_title_styles
    )
