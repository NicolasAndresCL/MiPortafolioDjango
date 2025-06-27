# Mi Portafolio Personal (Django & DRF Backend)

Este repositorio contiene el backend de mi portafolio personal, construido con **Django** y **Django REST Framework (DRF)**. Proporciona una API robusta y segura para gestionar mis proyectos y habilidades, permitiendo una fácil integración con cualquier frontend (actualmente utilizando Django Templates).

---
## 🚀 Características

* **API RESTful Completa y Segura:**
    * Endpoints dedicados para `Projects` (proyectos) y `Skills` (habilidades).
    * Soporte completo para operaciones CRUD (Crear, Leer, Actualizar, Eliminar) a través de los `ViewSets` de DRF.
    * **Acceso Controlado:** Las operaciones de lectura (GET) son públicas, mientras que las operaciones de escritura (POST, PUT, PATCH, DELETE) requieren autenticación mediante un token (TokenAuthentication de DRF), garantizando la integridad de los datos.
* **Documentación API Interactiva:**
    * Integración de **DRF Spectacular** para generar automáticamente una interfaz Swagger/OpenAPI. Explora y prueba la API directamente desde tu navegador.
* **Gestión de Medios:**
    * Manejo de subida de imágenes para proyectos (configurado para desarrollo).
* **Gestión de Archivos Estáticos:**
    * Archivos CSS, imágenes y otros assets estáticos organizados eficientemente dentro de las aplicaciones Django.
* **Pruebas Unitarias Robustas:**
    * Cobertura de pruebas unitarias para los modelos `Project` y `Skill`, asegurando la integridad y el comportamiento esperado de los datos.
* **Base de Datos Relacional:**
    * Utiliza SQLite por defecto para desarrollo (fácilmente escalable a PostgreSQL u otras en producción).
* **Configuración Segura de Entorno:**
    * Uso de `python-decouple` para gestionar variables de entorno sensibles (como `SECRET_KEY` y credenciales de correo electrónico), manteniendo la información confidencial fuera del control de versiones.
* **Configuración Frontend Flexible:**
    * Actualmente sirve el frontend básico utilizando Django Templates y archivos estáticos, listo para ser conectado con frameworks modernos como React o Vue si se desea en el futuro.

## 📋 Requisitos

Para ejecutar este proyecto localmente, necesitarás:

* Python 3.8+
* pip (gestor de paquetes de Python)

## 🛠️ Configuración Local

Sigue estos pasos para poner el proyecto en marcha en tu máquina local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/NicolasAndresCL/MiPortafolioDjango.git](https://github.com/NicolasAndresCL/MiPortafolioDjango.git)
    cd MiPortafolioDjango
    ```

2.  **Crear y Activar un Entorno Virtual:**
    ```bash
    python -m venv .venv
    # En Windows:
    .venv\Scripts\activate
    # En macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crear un archivo `.env`:**
    Este archivo contendrá tus variables de entorno sensibles. Créalo en la raíz de tu proyecto (`MiPortafolioDjango/.env`) y **asegúrate de que esté listado en tu `.gitignore`** para que no se suba al repositorio.
    ```
    SECRET_KEY='tu_secret_key_aqui_generada'
    EMAIL_HOST_PASSWORD='tu_password_de_email_aqui'
    # Agrega cualquier otra variable de entorno que uses en settings.py
    ```
    Puedes generar una `SECRET_KEY` de Django con:
    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

5.  **Aplicar Migraciones de la Base de Datos:**
    ```bash
    python manage.py migrate
    ```

6.  **Crear un Superusuario (para acceder al Admin de Django y generar un Token API):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Generar Token de Autenticación para tu Superusuario:**
    Si deseas realizar operaciones de escritura (POST, PUT, DELETE) en la API, necesitarás un token. Genera uno para el superusuario que acabas de crear:
    ```bash
    python manage.py drf_create_token <nombre_de_usuario_del_superusuario>
    ```
    Guarda este token de forma segura, ya que lo usarás en las cabeceras `Authorization: Token <tu_token>` para solicitudes protegidas.

8.  **Ejecutar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    ```

    El backend estará disponible en `http://127.0.0.1:8000/`.

## 🌐 Endpoints de la API

Una vez que el servidor esté corriendo, puedes acceder a:

* **API Root:** `http://127.0.0.1:8000/api/`
* **Documentación Swagger UI:** `http://127.0.0.1:8000/api/schema/swagger-ui/`
* **Proyectos:** `http://127.0.0.1:8000/api/projects/`
* **Habilidades:** `http://127.0.0.1:8000/api/skills/`

**Nota sobre la seguridad de la API:** Las solicitudes `GET` a los endpoints de Proyectos y Habilidades son públicas. Para realizar operaciones `POST`, `PUT`, `PATCH` o `DELETE`, deberás incluir la cabecera `Authorization` con tu token generado:
`Authorization: Token <tu_token_generado_aqui>`

El frontend principal (si está configurado) estará en la raíz: `http://127.0.0.1:8000/`

## 🧪 Ejecutar Pruebas

Para ejecutar las pruebas unitarias del proyecto:

```bash
python manage.py test portfolio_app
```

***
🤝 Contribuciones
Las contribuciones son bienvenidas. Siéntete libre de abrir un issue o enviar un pull request.

📄 Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.