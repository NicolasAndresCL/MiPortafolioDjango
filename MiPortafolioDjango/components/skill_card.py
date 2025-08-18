# mi_portafolio/components/skill_card.py
import reflex as rx

ICON_MAP = {
    "JavaScript": "https://img.icons8.com/color/48/javascript.png",
    "Python": "https://img.icons8.com/color/48/python.png",
    "Django": "https://img.icons8.com/color/48/django.png",
    # ... otros íconos
}

def skill_card(skill):
    fallback_icon = "https://img.icons8.com/color/48/source-code.png"
    image_url = skill.get("logo", ICON_MAP.get(skill.get("name"), fallback_icon))
    
    return rx.box(
        rx.vstack(
            rx.image(src=image_url, alt=f"{skill['name']} icon", class_name="w-12 h-12"),
            rx.heading(skill["name"], size="4", color="orange.500", font_weight="bold"),
            rx.text(skill["level"], color="slate.400", font_size="sm", font_weight="medium"),
            rx.text(skill["category"], color="slate.500", font_size="xs"),
            spacing="4",
            align="center"
        ),
        class_name="bg-slate-800 rounded-2xl shadow-xl hover:shadow-2xl border border-slate-700 transition duration-300 p-6 flex flex-col items-center text-center space-y-4"
    )