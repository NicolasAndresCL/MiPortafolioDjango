import reflex as rx

def project_card(project):
    return rx.box(
        rx.vstack(
            rx.heading(
                project.get("title", "Sin título"), 
                size="3",  # Tamaño más apropiado para cards
                color="white",
                text_align="center"
            ),
            rx.image(
                src=project.get("image", ""),
                alt=f"Imagen del proyecto {project.get('title', '')}",
                height="200px",
                object_fit="cover",
                border_radius="md"
            ),
            rx.text(
                project.get("description", ""),
                color="gray.300",
                font_size="sm",
                text_align="justify"
            ),
            rx.text(
                f"Tecnologías: {project.get('technologies', 'No especificadas')}",
                color="gray.400",
                font_size="xs"
            ),
            rx.link(
                rx.hstack(
                    rx.icon(tag="github", size=16),
                    rx.text("Ver en GitHub"),
                    spacing="2"
                ),
                href=project.get("github_link", "#"),
                is_external=True,
                color="orange.500",
                _hover={"color": "orange.400"}
            ),
            spacing="4",
            align="stretch",
        ),
        class_name="bg-slate-800 rounded-2xl shadow-xl hover:shadow-2xl transition duration-300 p-6 flex flex-col items-center space-y-6 border border-slate-700"
    )