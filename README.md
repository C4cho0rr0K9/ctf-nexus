# NEXUS CTF Challenge 🔐

> Multi-stage web challenge: recon, header authentication, token exchange, and flag capture.
> Ideal para eventos CTF, workshops de ciberseguridad, o práctica personal.

## 📋 Overview

NEXUS simula un sistema con **3 capas de autenticación**. El objetivo es atravesarlas en orden para obtener la flag oculta.

| Atributo | Valor |
|----------|-------|
| **Dificultad** | 🟡 Media |
| **Categoría** | Web — Multi-stage Authentication Bypass |
| **Formato flag** | `CTF{...}` |
| **Puerto** | `9090` |
| **Stack** | Python + Flask + Podman/Docker |

## 🧩 Flujo del reto

```
Página principal  ──→  /robots.txt  ──→  /init  ──→  /portal  ──→  /flag
```

| Paso | Endpoint | Método | Qué enviar | Qué recibes |
|------|----------|--------|------------|-------------|
| 1 | `/init` | `POST` | Header `X-Bootstrap: enable` | `session_id` |
| 2 | `/portal` | `POST` | JSON `{"session_id":"..."}` | `auth_token` |
| 3 | `/flag` | `GET` | Header `Authorization: Bearer <token>` | **🚩 Flag** |

Las pistas están ocultas en la página principal (base64) y en `/robots.txt`.

## 🚀 Despliegue (3 formas)

### Opción 1 — Script automático (recomendado)

```bash
./deploy.sh
```

### Opción 2 — Docker Compose

```bash
docker compose up -d
# o con podman:
podman-compose up -d
```

### Opción 3 — Manual

```bash
# 1. Construir la imagen
podman build -t ctf-nexus challenge/

# 2. Ejecutar
podman run -d --name ctf-nexus --network host ctf-nexus

# Alternativa con Docker:
docker build -t ctf-nexus challenge/
docker run -d --name ctf-nexus -p 9090:9090 ctf-nexus
```

### Verificar que funciona

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/
# Debe responder: 200
```

## 🌐 Acceso

| Desde | URL |
|-------|-----|
| **Misma máquina** | http://localhost:9090/ |
| **Red local** | http://<IP_DEL_SERVIDOR>:9090/ |

Para obtener la IP del servidor: `ip addr show | grep "inet " | grep -v 127.0.0.1`

## 📚 Solución

Abre `solution/index.html` en cualquier navegador — es una guía interactiva paso a paso con comandos listos para copiar y pegar.

> ⚠️ **Para organizadores:** Si no quieres que los participantes vean la solución, borra la carpeta `solution/` antes del evento.

## 📁 Estructura del proyecto

```
ctf-nexus/
├── challenge/                 # 🎯 El CTF en sí
│   ├── app.py                 # Servidor Flask (el reto)
│   ├── Dockerfile             # Imagen Docker/Podman
│   └── requirements.txt       # Dependencias (solo flask)
├── solution/                  # 📖 Walkthrough (abrir en navegador)
│   └── index.html
├── deploy.sh                  # 🚀 Script de despliegue automático
├── docker-compose.yml         # 🐳 Orquestación simple
├── README.md                  # Este archivo
├── LICENSE                    # MIT
└── .gitignore
```

## 🛑 Comandos útiles

```bash
# Ver logs del servidor
podman logs -f ctf-nexus

# Detener
podman stop ctf-nexus

# Reiniciar
podman restart ctf-nexus

# Eliminar contenedor
podman rm -f ctf-nexus
```

## 📄 Licencia

MIT — haz lo que quieras con esto.
