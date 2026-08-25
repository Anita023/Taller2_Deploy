# TechGear - Sistema Híbrido de Catálogo y Pedidos

Proyecto académico para gestionar productos tecnológicos y pedidos.

La aplicación utiliza una arquitectura híbrida:

- **FastAPI** funciona como API REST y backend principal.
- **MongoDB Atlas** almacena productos y pedidos.
- **Pydantic** valida los datos.
- **Django** funciona como frontend web utilizando el patrón MVT.
- **Requests** permite que Django consuma la API FastAPI mediante peticiones HTTP.
- **Swagger UI** permite probar y documentar los endpoints de la API.

## Autor

- Ana María Deossa

## Arquitectura

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

## Tecnologías utilizadas

- Python
- FastAPI
- Uvicorn
- Pydantic
- PyMongo Async
- MongoDB Atlas
- Django
- Requests
- HTML y CSS
- Git y GitHub
- Render

## Funcionalidades

- Conexión con MongoDB Atlas.
- Validación de datos con Pydantic.
- CRUD de productos.
- Registro de pedidos.
- Validación de stock.
- Actualización de stock después de un pedido.
- Documentación automática con Swagger UI.
- Catálogo de productos usando Django.
- Integración HTTP entre Django y FastAPI.

## Estructura general

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
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## Ejecución local

### Backend FastAPI

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

Ejecutar el servidor:

```bash
python -m uvicorn app.main:app --reload
```

El backend estará disponible en:

- [API local](http://127.0.0.1:8000/)
- [Swagger UI local](http://127.0.0.1:8000/docs)

### Frontend Django

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
python manage.py runserver 8001
```

El frontend estará disponible en:

- [Catálogo local](http://127.0.0.1:8001/)

## Variables de entorno

Crear el archivo:

```text
backend/.env
```

Agregar:

```env
MONGODB_URL=tu_url_de_mongodb_atlas
DATABASE_NAME=ambiente502
```

> El archivo `.env` contiene datos privados y no debe subirse a GitHub.

## Desarrollo por clases

| Clase | Tema principal | Resultado |
|---|---|---|
| Clase 1 | Entorno, MongoDB Atlas y modelos Pydantic | Estructura inicial, conexión a base de datos y esquemas |
| Clase 2 | FastAPI, CRUD y Swagger UI | API REST funcional para productos y pedidos |
| Clase 3 | Django y consumo de API | Integración HTTP entre frontend y backend |
| Clase 4 | Templates y catálogo | Interfaz gráfica para mostrar productos |

## Repositorio

- [Repositorio en GitHub](https://github.com/Anita023/Taller2_Deploy)

## Despliegue en Render

El backend FastAPI está desplegado en Render.

- [API desplegada en Render](https://taller2-deploy-q01n.onrender.com/)
- [Swagger UI desplegado](https://taller2-deploy-q01n.onrender.com/docs)

## Seguridad

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
