import reflex as rx

config = rx.Config(
    app_name="MiPortafolioDjango",
    api_url="http://localhost:8000",
    frontend_port=3000,
    backend_port=8000,
    tailwind={
        "theme": {
            "extend": {
                "colors": {
                    "background": "#000000",
                    "content": "#FFFFFF",
                }
            }
        },
        "plugins": ["@tailwindcss/typography"]
    },
    
    # Configuración del tema por defecto
    default_theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="medium",
        accent_color="orange",
    ),

    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)