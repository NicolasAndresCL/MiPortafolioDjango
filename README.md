
# 🧠 Mi Portafolio Personal – Backend Django & DRF (API para React Frontend)

Este repositorio contiene el backend modular de mi portafolio personal, construido con **Django** y **Django REST Framework**. Expone una API pública y documentada para gestionar mis proyectos, habilidades y mensajes de contacto, integrada con un frontend en **React/Vite/Tailwind**.

> ✅ Este backend reemplaza la versión anterior basada en Django Templates.
> 🔁 En producción será consumido por el nuevo frontend React.

---

## 🚀 Características principales

- ✅ **Arquitectura modular por dominio** (apps desacopladas para `projects`, `skills`, `contact`)
- 🛠️ **Endpoints RESTful con DRF ViewSets** (`ProjectViewSet`, `SkillViewSet`)  
- 📫 **Vista personalizada `contacto_api`** con `send_mail` para recibir mensajes
- 🔐 Autenticación con token DRF (solo escritura protegida)
- 📚 **Swagger/OpenAPI** con DRF Spectacular y `@extend_schema_view` para documentación
- 🎨 Soporte para imágenes en proyectos y logos de habilidades
- ⚙️ Configuración segura con `.env` y `python-decouple`
- 📦 Desplegado en [PythonAnywhere](https://www.pythonanywhere.com/)

---

## 🌐 Endpoints principales

| Endpoint                      | Propósito                    |
|------------------------------|------------------------------|
| `/api/projects/`             | CRUD de proyectos            |
| `/api/skills/`               | CRUD de habilidades          |
| `/api/contacto/`            | Envío de formulario de contacto |
| `/api/schema/swagger-ui/`   | Documentación interactiva    |
| `/admin/`                    | Panel administrativo Django  |

---

## 🧪 Tests

```bash
python manage.py test portfolio_app
```
- Incluye tests unitarios para modelos Project y Skill.

- Preparado para extensión con tests funcionales de API.

## 📸 Captura referencial

- 🔧 Instalación local
```
bash
git clone https://github.com/NicolasAndresCL/MiPortafolioDjango.git
cd MiPortafolioDjango
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
- Crear .env con tus variables:

```
env
SECRET_KEY='...'
EMAIL_HOST_PASSWORD='...'
```
- Migrar y ejecutar:
```
bash
python manage.py migrate
python manage.py runserver
```
## 🛰️ Despliegue
Este backend está desplegado actualmente en PythonAnywhere y será la base del nuevo portafolio React/Vite. La integración entre frontend y backend se realiza mediante fetch API a los endpoints REST.

## 📬 Contacto y mensajes
Los usuarios pueden enviar mensajes desde el frontend a través del endpoint:
```
POST /api/contacto/
```
Este formulario se conecta con React y dispara send_mail con validación.


## 🐛 Debugging real en producción Django + React
🔍 1. Pantalla en blanco tras integración de frontend
Síntoma: Vista en blanco sin errores visibles en consola.

Diagnóstico:

Archivos hashificados duplicados en STATIC_ROOT.

index.html mal referenciado o sin ruta estática adecuada.

Assets no linkeados correctamente por manifest.json post-build.

Solución aplicada:

Limpieza de STATIC_ROOT + regeneración de assets vía npm run build.

Validación manual de rutas en HTML y revisión de settings.py.

Verificación de collectstatic y compatibilidad con STATICFILES_DIRS.

## ⚠️ 2. Error MIME en entorno móvil
Síntoma: Estilos no cargan en dispositivos móviles, consola marca error MIME.

Diagnóstico:

Improper MIME type debido a ruta errónea o archivo vacío.

Confusión entre STATICFILES_DIRS (desarrollo) y STATIC_ROOT (producción).

Solución aplicada:

Revisión de cabeceras en archivos CSS y JS.

Rebuild del frontend asegurando .map y .css válidos.

Ajuste en configuración de Nginx/Gunicorn para servir estáticos correctamente.

## 🖼️ 3. Problemas de visibilidad UX/UI en móvil
Síntoma: Tarjetas invisibles, texto sin contraste en ciertas resoluciones.

Diagnóstico:

Estilos heredados no aplican correctamente en media queries.

Diferencias en layout y z-index por falta de breakpoints específicos.

Solución aplicada:

Refactor con min-width y max-width en breakpoints claves.

Uso de unidades relativas (em, %) para adaptar espaciado.

Validación visual multiplataforma con inspección móvil en DevTools.

## 🤝 Contribuciones
Las contribuciones son bienvenidas. Podés abrir issues o enviar pull requests si querés mejorar la arquitectura, extender los endpoints o documentar nuevas integraciones.

## 📄 Licencia
Este proyecto está bajo licencia MIT.	