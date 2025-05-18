# Authify

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

Authify es un microservicio de autenticación modular que permite gestionar usuarios y controlar el acceso a diferentes módulos de aplicación mediante tokens JWT.

## Características

- 🔐 **Autenticación completa**: Registro, inicio de sesión y verificación de tokens
- 🧩 **Sistema modular**: Control de acceso basado en módulos
- 🔑 **Tokens JWT**: Generación y validación segura de tokens
- 🌐 **API REST con FastAPI**: Alto rendimiento y documentación automática
- 📦 **Containerización**: Despliegue sencillo con Docker
- 🚀 **CI/CD**: Integración continua con GitHub Actions

## Estructura del proyecto

```
├── app/
│   ├── auth/           # Módulo de autenticación
│   │   ├── main.py     # Funciones principales de autenticación
│   │   ├── models.py   # Modelos de datos (ORM)
│   │   ├── routes.py   # Endpoints de la API
│   │   └── schemas.py  # Esquemas de datos (Pydantic)
│   ├── database.py     # Configuración de conexión a BD
│   └── main.py         # Aplicación FastAPI principal
├── docker-compose.yml  # Configuración para producción 
├── docker-compose.dev.yml # Configuración para desarrollo
├── Dockerfile          # Instrucciones para construir la imagen
├── requirements.txt    # Dependencias del proyecto
└── Makefile            # Comandos útiles para desarrollo
```

## Endpoints principales

- `POST /auth/register`: Registro de nuevos usuarios
- `POST /auth/login`: Inicio de sesión para usuarios existentes
- `POST /auth/{module_name}/login`: Inicio de sesión específico para un módulo
- `GET /auth/check-token`: Verifica la validez de un token
- `POST /auth/refresh-token`: Refresca un token existente
- `POST /auth/modules`: Crea un nuevo módulo
- `POST /auth/modules/assign`: Asigna un usuario a un módulo

## Requisitos previos

- Docker y Docker Compose
- PostgreSQL (o usar la versión containerizada)

## Configuración

### Variables de entorno

Crea un archivo `.env` con la siguiente configuración:

```
POSTGRES_USER=auth_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=authify_db
DATABASE_URL=postgresql://auth_user:your_secure_password@db:5432/authify_db
SECRET_KEY=your_secret_key_for_jwt_tokens
FRONTEND_URLS=http://localhost:3000,https://your-app-domain.com
VIRTUAL_HOST=api.your-domain.com
VIRTUAL_PORT=8000
```

## Ejecución

### Desarrollo local

```bash
# Levantar servicios de desarrollo (incluye PGAdmin)
make up

# O manualmente
docker-compose -f docker-compose.dev.yml up
```

### Producción

```bash
# Levantar servicios de producción
docker-compose up -d
```

## Despliegue

El proyecto incluye un flujo de trabajo de GitHub Actions para desplegar automáticamente en un servidor con GitHub Actions Runner.

## Seguridad

- Los tokens JWT tienen una expiración configurable
- Las contraseñas se almacenan con hash usando bcrypt
- El CORS se configura mediante la variable FRONTEND_URLS

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu función (`git checkout -b feature/amazing-feature`)
3. Realiza tus cambios y haz commit (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

[MIT](LICENSE)

---

![GitHub language count](https://img.shields.io/github/languages/count/nikip11/authify)
![GitHub top language](https://img.shields.io/github/languages/top/nikip11/authify)
![GitHub last commit](https://img.shields.io/github/last-commit/nikip11/authify)
