TechGear - Sistema Híbrido de Catálogo y Pedidos
Proyecto académico para gestionar productos tecnológicos y pedidos.
La aplicación utiliza una arquitectura híbrida:
FastAPI funciona como API REST y backend principal.
MongoDB Atlas almacena productos y pedidos.
Pydantic valida los datos.
Django funciona como frontend web utilizando el patrón MVT.
Requests permite que Django consuma la API FastAPI mediante peticiones HTTP.
Swagger UI permite probar y documentar los endpoints de la API.
Autor
Ana María Deossa
Arquitectura
```text
Usuario
   |
   v
Django - Frontend
   |
   | Peticiones HTTP con requests
   v
FastAPI - Backend
   |
   v
MongoDB Atlas
```
Django no se conecta directamente a MongoDB. El frontend consulta FastAPI y la API administra los datos almacenados en MongoDB Atlas.
Tecnologías utilizadas
Python
FastAPI
Uvicorn
Pydantic
PyMongo Async
MongoDB Atlas
Django
Requests
HTML y CSS
Git y GitHub
Render
Vercel
Funcionalidades
Conexión con MongoDB Atlas.
Validación de datos con Pydantic.
CRUD de productos.
Registro de pedidos.
Validación de stock.
Actualización de stock después de un pedido.
Documentación automática con Swagger UI.
Catálogo de productos usando Django.
Integración HTTP entre Django y FastAPI.
Estructura general
```text
TALLER2_DEPLOY/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── database.py
│   │   ├── main.py
│   │   └── schemas.py
│   └── requirements.txt
│
├── frontend/
│   ├── config/
│   ├── tienda/
│   ├── manage.py
│   ├── vercel.json
│   └── requirements.txt
│
├── .gitignore
└── README.md
```
Ejecución local
Backend FastAPI
```bash
cd backend
python -m venv .venv
```
Activar el entorno virtual en Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
Instalar dependencias:
```bash
python -m pip install -r requirements.txt
```
Ejecutar el servidor (el puerto 8001 es obligatorio, es el que espera el frontend):
```bash
python -m uvicorn app.main:app --reload --port 8001
```
El backend estará disponible en:
API local
Swagger UI local
Frontend Django
En otra terminal:
```bash
cd frontend
python -m venv .venv
```
Activar el entorno virtual en Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
Instalar dependencias:
```bash
python -m pip install -r requirements.txt
```
Ejecutar migraciones:
```bash
python manage.py migrate
```
Iniciar Django:
```bash
python manage.py runserver 8000
```
El frontend estará disponible en:
Catálogo local
Variables de entorno
Backend (`backend/.env`)
```env
MONGODB_URL=tu_url_de_mongodb_atlas
DATABASE_NAME=ambiente502
```
> El archivo `.env` contiene datos privados y no debe subirse a GitHub.
Frontend (opcional, `FASTAPI_URL`)
En local no es necesario definirla: por defecto `config/settings.py` usa `http://127.0.0.1:8001`.
En producción (Vercel) se define como variable de entorno del proyecto para no tocar el código:
```env
FASTAPI_URL=https://taller2-deploy-q01n.onrender.com
```
Desarrollo por clases
Clase	Tema principal	Resultado
Clase 1	Entorno, MongoDB Atlas y modelos Pydantic	Estructura inicial, conexión a base de datos y esquemas
Clase 2	FastAPI, CRUD y Swagger UI	API REST funcional para productos y pedidos
Clase 3	Django y consumo de API	Integración HTTP entre frontend y backend
Clase 4	Templates y catálogo	Interfaz gráfica para mostrar productos
Clase 5	Formularios y pedidos	Vista de checkout, creación de pedidos vía POST
Clase 6	Refinamiento y entrega final	Manejo de excepciones, README y despliegue
Repositorio
Repositorio en GitHub
Despliegue en Render (Backend - FastAPI)
El backend FastAPI está desplegado en Render.
API desplegada en Render
Swagger UI desplegado
Despliegue en Vercel (Frontend - Django)
El frontend de Django se despliega en Vercel usando el builder `@vercel/python`, apuntando al `wsgi.py` real del proyecto dentro de `config/`.
`frontend/vercel.json`:
```json
{
    "builds": [
        {
            "src": "config/wsgi.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "config/wsgi.py"
        }
    ]
}
```
Pasos:
Importar el repositorio en Vercel, con Root Directory = `frontend`.
En "Environment Variables" del proyecto de Vercel, agregar:
`FASTAPI_URL` = `https://taller2-deploy-q01n.onrender.com`
Desplegar. Vercel instala `frontend/requirements.txt` y sirve la app a través de `config/wsgi.py`.
Para que esto funcione, `frontend/config/settings.py` incluye:
`ALLOWED_HOSTS = [".vercel.app", "localhost", "127.0.0.1"]`
`CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]`
`SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` (para que el formulario de pedidos no falle por CSRF detrás del proxy de Vercel)
`FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://127.0.0.1:8001")` (usa la variable de entorno en producción, y localhost en desarrollo)
Seguridad
El proyecto utiliza `.gitignore` para evitar subir archivos sensibles o innecesarios:
```text
.env
*.env
.venv/
venv/
__pycache__/
*.py[cod]
db.sqlite3
.vscode/
```