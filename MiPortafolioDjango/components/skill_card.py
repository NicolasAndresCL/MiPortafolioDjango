# mi_portafolio/components/skill_card.py
import reflex as rx

ICON_MAP = {
    "JavaScript": "https://img.icons8.com/color/48/javascript.png",
    "Python": "https://img.icons8.com/color/48/python.png",
    "Django": "https://img.icons8.com/color/48/django.png",
    "React": "https://img.icons8.com/color/48/react-native.png",
    "Node.js": "https://img.icons8.com/color/48/nodejs.png",
    "PostgreSQL": "https://img.icons8.com/color/48/postgresql.png",
    "Docker": "https://img.icons8.com/color/48/docker.png",
    "Git": "https://img.icons8.com/color/48/git.png"
}

def skill_card(skill):
    fallback_icon = "https://img.icons8.com/color/48/source-code.png"
    image_url = skill.get("logo", ICON_MAP.get(skill.get("name", ""), fallback_icon))
    
    return rx.box(
        rx.vstack(
            rx.image(
                src=image_url,
                alt=f"{skill.get('name', 'Tecnología')} icon",
                width="48px",
                height="48px",
                border_radius="md"
            ),
            rx.heading(
                skill.get("name", ""),
                size="4",
                color="orange.500",
                font_weight="bold"
            ),
            rx.badge(
                skill.get("level", "Básico"),
                color_scheme="orange",
                variant="soft",
                size="1"
            ),
            rx.text(
                skill.get("category", ""),
                color="slate.400",
                font_size="xs"
            ),
            spacing="3",
            align="center"
        ),
        class_name="bg-slate-800 rounded-2xl shadow-xl hover:shadow-2xl border border-slate-700 transition duration-300 p-6 flex flex-col items-center text-center"
    )