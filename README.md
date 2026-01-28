# Space Reserve – Backend API

Backend REST API para la gestión de espacios, reservas y usuarios, desarrollada con Flask, PostgreSQL y autenticación JWT. Este proyecto forma parte de una aplicación Full Stack cuyo frontend será construido con React y Tailwind CSS.

## Tecnologías Utilizadas
- Python 3
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Flask JWT Extended
- PostgreSQL
- Python Dotenv

## Funcionalidades
### Autenticación y Usuarios
- Registro de usuarios
- Inicio de sesión (login)
- Autenticación mediante JWT
- Sistema de roles (Usuario y Administrador)

### Espacios
- Creación de espacios
- Listado de espacios disponibles

### Reservas
- Creación de reservas (requiere autenticación)
- Listar reservas por espacio
- Consultar disponibilidad horaria por día
- Cancelar reservas


## Configuración del Proyecto
### Clonar el repositorio
- git clone https://github.com/Exeq-dev/space-reserve-backend.git
- cd space-reserve-backend

### Crear entorno virtual
- python3 -m venv venv
- source venv/bin/activate

### Instalar dependencias
- pip install -r requirements.txt

### Variables de entorno
Crear un archivo .env en la raíz del proyecto basado en .env.example con las siguientes variables:
- FLASK_ENV=development
- DATABASE_URL=postgresql://user:password@localhost:5432/db_name
- SECRET_KEY=your-secret-key
- JWT_SECRET_KEY=your-jwt-secret

El archivo .env no debe subirse al repositorio.

## Base de Datos
Inicializar migraciones:
- flask db init
- flask db migrate
- flask db upgrade
  
Cargar datos iniciales (roles, espacios, etc.):
- python seed.py

## Ejecutar el servidor
- flask run
  
El servidor quedará disponible en http://127.0.0.1:5000

## Autenticación JWT
Los endpoints protegidos requieren el header Authorization con el formato:
- Authorization: Bearer <TOKEN>

El token se obtiene al iniciar sesión.

## Endpoints Principales
- POST /auth/register Registro de usuario
- POST /auth/login Login y obtención de JWT
- GET /spaces Listar espacios
- POST /reservations Crear reserva
- GET /spaces/{id}/availability Consultar disponibilidad horaria
- DELETE /reservations/{id} Cancelar reserva

## Seguridad
- Contraseñas almacenadas con hash
- Autenticación basada en JWT
- Variables sensibles protegidas mediante variables de entorno
- Archivo .env excluido del repositorio mediante .gitignore

## Estado del Proyecto
Backend funcional y seguro. Próximo paso: desarrollo del frontend con React y Tailwind CSS.

## Autor
Exequiel Albornoz Aránguiz

Proyecto educativo con enfoque profesional.
