# mi_portafolio/components/basic_menu.py
import reflex as rx

def basic_menu():
    return rx.menu(
        rx.menu_button("Menú", color_scheme="teal"),
        rx.menu_list(
            rx.menu_item("Sobre mí", href="#Sobre-mi"),
            rx.menu_item("Proyectos", href="#Proyectos"),
            rx.menu_item("Habilidades", href="#Habilidades"),
            rx.menu_item("Contacto", href="#Contactame"),
        )
    )