# section_title.py
import reflex as rx
from ..styles import section_title_styles

def section_title(text: str) -> rx.Component:
    """Componente reutilizable para títulos de sección."""
    return rx.box(
        rx.text(text),
        **section_title_styles
    )
