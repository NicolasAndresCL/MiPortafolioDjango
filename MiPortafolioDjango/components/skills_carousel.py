import reflex as rx
from .skill_card import skill_card

def skills_carousel(skills):
    return rx.box(
        rx.grid(
            rx.foreach(skills, skill_card),
            spacing="4",
            columns="2",
            sm_columns="3",
            md_columns="4",
            lg_columns="5",
        ),
        class_name="w-full px-4 py-8"
    )