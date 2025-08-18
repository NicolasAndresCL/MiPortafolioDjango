# mi_portafolio/styles.py

# 🎯 Paleta base y sombras
DARK_BG = "rgb(15, 23, 42)"         # slate.900
LIGHT_BG = "rgb(255, 255, 255)"     # white
GRAY_BORDER = "rgb(229, 231, 235)"  # gray.200
TEXT_WHITE = "white"

# 🧩 Estilos reutilizables
base_card = {
    "bg": DARK_BG,
    "color": TEXT_WHITE,
    "rounded": "xl",
    "shadow": "md",
    "p": "8",
}

base_section = {
    "bg": LIGHT_BG,
    "border": "1px",
    "border_color": GRAY_BORDER,
    "rounded": "lg",
    "shadow": "md",
    "p": "6",
    "text_align": "center",
    "max_w": "md",
    "mx": "auto",
}

# 🧠 Estilos específicos por componente

titulo_card_styles = {
    "font_size": "2em",
    "font_weight": "bold",
    "color": TEXT_WHITE,
    "text_align": "center",
    "mb": "4",
}

button_group_styles = {
    "spacing": "4",
    "justify": "center",
    "mt": "4",
}

sobre_mi_styles = {
    **base_card,
    "line_height": "1.75",
    "max_w": "4xl",
    "mx": "auto",
}

contact_card_styles = {
    **base_card,
    "max_w": "lg",
    "mx": "auto",
}

section_title_styles = {
    **base_section,
    "font_size": "1.5em",
    "font_weight": "semibold",
}

carrusel_projects_styles = {
    "bg": DARK_BG,
    "p": "6",
    "rounded": "lg",
    "shadow": "lg",
    "overflow_x": "auto",
    "scroll_behavior": "smooth",
    "gap": "6",
}

skills_carousel_styles = {
    "bg": DARK_BG,
    "p": "6",
    "rounded": "lg",
    "shadow": "lg",
    "display": "flex",
    "flex_wrap": "wrap",
    "justify": "center",
    "gap": "4",
}

footer_card_styles = {
    "bg": DARK_BG,
    "color": TEXT_WHITE,
    "p": "6",
    "text_align": "center",
    "font_size": "sm",
    "border_top": "1px",
    "border_color": GRAY_BORDER,
}
