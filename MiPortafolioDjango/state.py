import reflex as rx
import requests
from typing import Any



# 📬 Modelo de datos para el formulario de contacto
class FormData(rx.Base):
    name: str = ""
    email: str = ""
    message: str = ""


# 🧠 Estado global de la aplicación
class State(rx.State):
    # Datos cargados desde la API
    projects: list[dict] = []
    skills: list[dict] = []

    # Estado de carga y errores
    loading: bool = True
    error: str = ""

    # Datos del formulario
    form_data: FormData = FormData()

    # 🔄 Carga de datos desde el backend Django
    async def get_data(self) -> None:
        """Obtiene datos de la API para proyectos y habilidades."""
        try:
            projects_res = requests.get("http://localhost:8000/api/projects/")
            skills_res = requests.get("http://localhost:8000/api/skills/")

            projects_res.raise_for_status()
            skills_res.raise_for_status()

            self.projects = projects_res.json()
            self.skills = skills_res.json()

        except requests.RequestException as e:
            self.error = f"Error al cargar datos: {e}"

        finally:
            self.loading = False

    # 📝 Manejo de cambios en el formulario
    def handle_change(self, name: str, value: str) -> None:
        """Actualiza el campo correspondiente en el formulario."""
        self.form_data = self.form_data.copy(update={name: value})

    # 📤 Envío del formulario

    def handle_submit(self, form_data: dict[str, Any]) -> None:
        """Procesa el envío del formulario."""
        self.form_data = FormData(**form_data)
        print(f"Formulario enviado: {self.form_data.dict()}")
        self.form_data = FormData()


