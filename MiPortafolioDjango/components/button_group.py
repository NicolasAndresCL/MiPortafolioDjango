import reflex as rx
from MiPortafolioDjango.styles import button_group_styles

def button_group() -> rx.Component:
    return rx.hstack(
        rx.button("LinkedIn", as_="a", href="https://linkedin.com/in/nicolascanoleal", target="_blank"),
        rx.button("GitHub", as_="a", href="https://github.com/nicolascanoleal", target="_blank"),
        rx.button("Dev.to", as_="a", href="https://dev.to/nicolascanoleal", target="_blank"),
        **button_group_styles
    )
