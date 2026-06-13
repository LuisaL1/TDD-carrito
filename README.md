# Carrito de Compras - API REST

API REST para gestionar un carrito de compras, construida con Python y Flask, con persistencia en PostgreSQL y contenerizada con Docker.

## Tecnologías

- Python 3.12 + Flask
- PostgreSQL 16
- Docker y Docker Compose
- pytest

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | / | Estado de la API |
| POST | /productos | Agregar producto |
| GET | /productos | Listar productos |
| DELETE | /productos/<id> | Eliminar producto |
| GET | /carrito/total | Calcular total |

## Ejecución

```bash
docker compose up -d
```

La API queda disponible en `http://localhost:5000`.

## Pruebas

```bash
docker compose exec app python -m pytest test_carrito.py -v
```
