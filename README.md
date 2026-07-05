# NEXUS CTF Challenge

> Multi-stage web challenge: recon, header authentication, token exchange, and flag capture.

## Overview

NEXUS is a Capture The Flag challenge for cybersecurity enthusiasts. The goal is to traverse a 3-step authentication chain to retrieve a hidden flag.

**Difficulty:** Medium  
**Category:** Web — Multi-stage Authentication Bypass  
**Flag format:** `CTF{...}`

## Challenge Flow

```
/robots.txt  →  /init  →  /portal  →  /flag
```

| Step | Endpoint | Method | Required | Response |
|------|----------|--------|----------|----------|
| 1 | `/init` | POST | Header `X-Bootstrap: enable` | `session_id` |
| 2 | `/portal` | POST | JSON `{"session_id":"..."}` | `auth_token` |
| 3 | `/flag` | GET | Header `Authorization: Bearer <token>` | **Flag** |

Hints are hidden in the main page source (base64-encoded) and in `/robots.txt`.

## Quick Start

### Requirements

- [Podman](https://podman.io/) or [Docker](https://docker.com/)
- Port 9090 available

### Run

```bash
podman build -t ctf-nexus challenge/
podman run -d --name ctf-nexus --network host ctf-nexus
```

Or with Docker:

```bash
docker build -t ctf-nexus challenge/
docker run -d --name ctf-nexus -p 9090:9090 ctf-nexus
```

### Access

- **Local:** http://localhost:9090/
- **Network:** http://&lt;server-ip&gt;:9090/

## Solution

Open `solution/index.html` in any browser for a complete step-by-step walkthrough with copy-paste commands.

> **Note for CTF organizers:** Remove or restrict access to `solution/` during the event if you don't want participants to see the walkthrough.

## Project Structure

```
ctf-nexus/
├── challenge/
│   ├── app.py              # Flask challenge server
│   ├── Dockerfile          # Container image
│   └── requirements.txt    # Python dependencies
├── solution/
│   └── index.html          # Standalone walkthrough (open in browser)
├── README.md
├── LICENSE
└── .gitignore
```

## License

MIT
