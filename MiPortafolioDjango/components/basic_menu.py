# mi_portafolio/components/basic_menu.py
import reflex as rx

def basic_menu():
    return rx.hstack(
        rx.link(
            "Sobre mí",
            href="#Sobre-mi",
            color="gray.300",
            _hover={"color": "orange.500"}
        ),
        rx.link(
            "Proyectos",
            href="#Proyectos",
            color="gray.300",
            _hover={"color": "orange.500"}
        ),
        rx.link(
            "Habilidades",
            href="#Habilidades",
            color="gray.300",
            _hover={"color": "orange.500"}
        ),
        rx.link(
            "Contacto",
            href="#Contactame",
            color="gray.300",
            _hover={"color": "orange.500"}
        ),
        spacing="6",
        justify="center"
    )