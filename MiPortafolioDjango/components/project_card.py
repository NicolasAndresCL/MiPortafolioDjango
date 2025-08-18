import reflex as rx

def project_card(project):
    return rx.box(
        rx.vstack(
            rx.heading(project.title, size="1", text_align="center"),
            rx.image(src=project.image, alt=f"Imagen del proyecto {project.title}"),
            rx.text(project.description, color="gray.300", font_size="sm"),
            rx.text(f"Tecnologías: {project.technologies}", color="gray.400", font_size="xs"),
            rx.link("Ir a GitHub", href=project.github_link, is_external=True),
            spacing="4",
            align="stretch",
        ),
        class_name="bg-slate-800 rounded-2xl shadow-xl hover:shadow-2xl transition duration-300 p-6 flex flex-col items-center space-y-6 border border-slate-700"
    )