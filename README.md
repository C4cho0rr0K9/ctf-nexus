# NEXUS

multi-stage web authentication challenge

```
  _   _ _____  _____ _   __  __
 | \ | | ____|/ ___| | | \ \/ /
 |  \| |  _| | |   | |_| |\  /
 | |\  | |___| |___|  _  |/  \
 |_| \_|_____|\____|_| |_/_/\_\
```

## description

nexus is a flash ctf challenge: 3 authentication layers to traverse in order.
the goal is to retrieve a hidden flag. designed for V-SANDBOX events.

attribute       | value
----------------|-------
difficulty      | flash easy
category        | web -- multi-stage auth bypass
flag format     | CTF{...}
port            | 9090
stack           | python + flask + podman/docker
event           | V-SANDBOX by VULTAETHEL

## flow

```
/robots.txt  -->  /init  -->  /portal  -->  /flag
```

step | endpoint | method | input | output
-----|----------|--------|-------|-------
1    | /init    | POST   | header `X-Bootstrap: enable` | `session_id`
2    | /portal  | POST   | json `{"session_id":"..."}`  | `auth_token`
3    | /flag    | GET    | header `Authorization: Bearer <token>` | flag

hints are embedded in the main page (base64) and /robots.txt.

## deploy

### option 1 -- automatic script

```
$ chmod +x deploy.sh
$ ./deploy.sh
```

### option 2 -- docker compose

```
$ docker compose up -d
```

### option 3 -- manual

```
$ podman build -t ctf-nexus challenge/
$ podman run -d --name ctf-nexus --network host ctf-nexus
```

with docker:

```
$ docker build -t ctf-nexus challenge/
$ docker run -d --name ctf-nexus -p 9090:9090 ctf-nexus
```

### verify

```
$ curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/
200
```

## access

```
local:   http://localhost:9090/
network: http://<server-ip>:9090/
```

find the server ip:

```
$ ip addr show | grep "inet " | grep -v 127.0.0.1
```

## solution

open solution/index.html in a browser for a step-by-step walkthrough.

> for organizers: remove the solution/ directory before the event.

## structure

```
ctf-nexus/
|-- challenge/
|   |-- app.py              # flask server
|   |-- Dockerfile          # container image
|   +-- requirements.txt    # dependencies (flask)
|-- solution/
|   +-- index.html          # walkthrough (standalone)
|-- deploy.sh               # automatic deploy script
|-- docker-compose.yml      # container orchestration
|-- README.md
|-- LICENSE                 # mit
+-- .gitignore
```

## commands

```
$ podman logs -f ctf-nexus    # tail logs
$ podman stop ctf-nexus       # stop
$ podman restart ctf-nexus    # restart
$ podman rm -f ctf-nexus      # remove
```

## license

MIT
