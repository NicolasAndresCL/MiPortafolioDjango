# mi_portafolio/components/titulo_card.py
import reflex as rx
from .basic_menu import basic_menu
from MiPortafolioDjango.styles import titulo_card_styles

def titulo_card()-> rx.Component:
    return rx.box(
        rx.text("Nicolás Andrés Cano Leal", font_size="2xl", font_weight="bold"),
        **titulo_card_styles
    )

    rx.box(
        rx.box(
            rx.box(
                rx.box(
                    rx.svg(
                        rx.circle(r=512, cx=512, cy=512, fill="url(#hero-gradient)", fill_opacity="0.7"),
                        view_box="0 0 1084 1080",
                        aria_hidden="true",
                        class_name="absolute top-1/2 left-1/2 -z-10 w-[32rem] h-[32rem] -translate-y-1/2 -translate-x-1/2 sm:left-full sm:-ml-80 lg:left-1/2 lg:ml-0 lg:translate-y-0",
                    ),
                    rx.div(
                        rx.box(
                            rx.heading(
                                "Portafolio de Nicolás Andrés Cano Leal",
                                size="lg",
                                font_weight="bold",
                                class_name="text-4xl sm:text-5xl font-bold tracking-tight text-white"
                            ),
                            rx.text(
                                "Desarrollador Backend Python con experiencia en la construcción de APIs robustas y escalables.",
                                font_size="lg",
                                color="slate.300"
                            ),
                            rx.box(
                                basic_menu(),
                                rx.link(
                                    "Descargar CV →",
                                    href="/static/NicolasCano_BackendDeveloper_CV.pdf",
                                    download=True,
                                    font_weight="bold",
                                    class_name="text-lg text-orange-500 hover:text-orange-400 transition transform hover:scale-105"
                                ),
                                class_name="mt-10 flex flex-wrap items-center justify-center gap-6 lg:justify-start"
                            ),
                            class_name="max-w-xl mx-auto text-center lg:text-left lg:mx-0 space-y-6"
                        ),
                        rx.box(
                            rx.box(
                                rx.image(
                                    src="/static/perfil-foto-nc.png",
                                    alt="Foto de Nicolás Cano",
                                    class_name="rounded-full mx-auto w-32 h-32 object-cover border-4 border-orange-500 shadow-md"
                                ),
                                rx.heading("Nicolás Cano", size="lg", text_align="center", mt="6", color="white"),
                                rx.text("Backend & Data Engineering", text_align="center", color="orange.500", mt="2", font_weight="medium", font_size="sm"),
                                rx.text("Arquitectura modular, escalabilidad y documentación impecable.", text_align="center", color="slate.400", mt="2", font_size="xs"),
                                class_name="bg-slate-900 p-8 rounded-3xl ring-1 ring-slate-700 shadow-xl w-full max-w-sm"
                            ),
                            class_name="flex justify-center items-center mt-12 lg:mt-0 lg:flex-shrink-0"
                        ),
                        class_name="relative z-10 px-6 sm:px-16 lg:flex lg:gap-x-20 lg:px-24 py-16"
                    ),
                    class_name="relative overflow-hidden rounded-3xl bg-slate-800 shadow-2xl border border-slate-700"
                ),
                class_name="mx-auto max-w-6xl px-4 sm:px-8 pt-16 lg:pt-24"
            ),
            class_name="w-full"
        )
    )
    
