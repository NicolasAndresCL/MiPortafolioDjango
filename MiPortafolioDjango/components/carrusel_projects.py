# mi_portafolio/components/carrusel_projects.py
import reflex as rx
from .project_card import project_card

def carrusel_projects(projects):
    return rx.box(
        rx.grid(
            rx.foreach(projects, project_card),
            spacing="4",
            columns="1",
            md_columns="2",
            lg_columns="3",
        ),
        class_name="w-full px-4 py-8"
    )
