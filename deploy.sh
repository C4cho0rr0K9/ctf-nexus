#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }
step()  { echo; echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; echo -e "  ${GREEN}$1${NC}"; echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"; }

CONTAINER_NAME="ctf-nexus"
IMAGE_NAME="ctf-nexus"
PORT="9090"

cleanup() {
  step "Limpiando contenedores anteriores..."
  if podman ps -a --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    podman rm -f "$CONTAINER_NAME" 2>/dev/null
    ok "Contenedor '$CONTAINER_NAME' eliminado."
  else
    info "No hay contenedor previo."
  fi
}

build() {
  step "Construyendo imagen Docker..."
  podman build --dns 8.8.8.8 -t "$IMAGE_NAME" ./challenge
  ok "Imagen '$IMAGE_NAME' construida."
}

run() {
  step "Ejecutando contenedor..."
  local have_host=$(podman info 2>/dev/null | grep -c "hostContainersStorage" || true)
  if podman run -d --name "$CONTAINER_NAME" --network host "$IMAGE_NAME" 2>/dev/null; then
    ok "Contenedor iniciado en puerto $PORT."
  else
    podman run -d --name "$CONTAINER_NAME" -p "$PORT:$PORT" "$IMAGE_NAME" 2>/dev/null || fail "No se pudo iniciar el contenedor."
    ok "Contenedor iniciado con port mapping en puerto $PORT."
  fi
}

test_health() {
  step "Verificando que el servidor responda..."
  sleep 2
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/" 2>/dev/null || echo "000")
  if [ "$status" = "200" ]; then
    ok "Servidor responde OK (HTTP $status) en http://localhost:$PORT/"
  else
    warn "Servidor respondió HTTP $status. Espera unos segundos y reintenta."
  fi
}

show_info() {
  local ip
  ip=$(ip addr show | grep -E "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}' | cut -d/ -f1)
  echo
  echo -e "${CYAN}╔════════════════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║${NC}  ${GREEN}CTF NEXUS desplegado exitosamente${NC}              ${CYAN}║${NC}"
  echo -e "${CYAN}╠════════════════════════════════════════════════════╣${NC}"
  echo -e "${CYAN}║${NC}  Local:  ${YELLOW}http://localhost:$PORT/${NC}                   ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC}  Red:    ${YELLOW}http://$ip:$PORT/${NC}        ${CYAN}║${NC}"
  echo -e "${CYAN}║${NC}  Solución: ${YELLOW}./solution/index.html${NC}               ${CYAN}║${NC}"
  echo -e "${CYAN}╚════════════════════════════════════════════════════╝${NC}"
  echo
  echo -e "  Para ver logs:       ${GREEN}podman logs -f $CONTAINER_NAME${NC}"
  echo -e "  Para detener:        ${GREEN}podman stop $CONTAINER_NAME${NC}"
  echo -e "  Para reiniciar:      ${GREEN}podman restart $CONTAINER_NAME${NC}"
  echo
}

main() {
  echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
  echo -e "${CYAN}║${NC}    ${GREEN}NEXUS CTF — Deploy Automático${NC}     ${CYAN}║${NC}"
  echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
  echo "  Container: $CONTAINER_NAME"
  echo "  Puerto:    $PORT"
  echo "  Fecha:     $(date '+%Y-%m-%d %H:%M')"
  echo

  cleanup
  build
  run
  test_health
  show_info
}

main "$@"
