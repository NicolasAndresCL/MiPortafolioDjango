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
    """Estado global de la aplicación."""
    
    # Datos cargados desde la API con valores iniciales
    projects: list[dict] = []
    skills: list[dict] = []

    # Estado de carga y errores
    loading: bool = True
    error: str = ""

    # Datos del formulario
    form_data: FormData = FormData()

    def _fetch_data(self, url: str) -> list[dict]:
        """Función auxiliar para hacer peticiones HTTP."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.error = f"Error al cargar datos desde {url}: {str(e)}"
            return []

    async def get_data(self) -> None:
        """Obtiene datos de la API para proyectos y habilidades."""
        try:
            # Obtener datos en paralelo
            projects_data = self._fetch_data("http://localhost:8000/api/projects/")
            skills_data = self._fetch_data("http://localhost:8000/api/skills/")
            
            # Actualizar estado solo si no hay errores
            if not self.error:
                self.projects = projects_data
                self.skills = skills_data
            
        except Exception as e:
            self.error = f"Error inesperado: {str(e)}"
        finally:
            self.loading = False

    # Llamar a get_data automáticamente al iniciar la app
    async def on_load(self):
        await self.get_data()

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
