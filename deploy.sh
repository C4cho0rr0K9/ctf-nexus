#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()  { echo -e "${CYAN}[*]${NC}  $*"; }
ok()    { echo -e "${GREEN}[+]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[!]${NC}  $*"; }
fail()  { echo -e "${RED}[-]${NC}  $*"; exit 1; }
sep()   { echo; echo -e "${CYAN}--- $* ---${NC}"; }

CONTAINER_NAME="ctf-nexus"
IMAGE_NAME="ctf-nexus"
PORT="9090"

cleanup() {
  sep "cleaning up previous containers"
  if podman ps -a --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    podman rm -f "$CONTAINER_NAME" 2>/dev/null
    ok "removed container '$CONTAINER_NAME'"
  else
    info "no previous container found"
  fi
}

build() {
  sep "building image"
  podman build --dns 8.8.8.8 -t "$IMAGE_NAME" ./challenge
  ok "image '$IMAGE_NAME' built"
}

run() {
  sep "starting container"
  if podman run -d --name "$CONTAINER_NAME" --network host "$IMAGE_NAME" 2>/dev/null; then
    ok "container started on port $PORT (host networking)"
  else
    podman run -d --name "$CONTAINER_NAME" -p "$PORT:$PORT" "$IMAGE_NAME" 2>/dev/null || fail "could not start container"
    ok "container started on port $PORT (port mapping)"
  fi
}

test_health() {
  sep "checking server health"
  sleep 2
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/" 2>/dev/null || echo "000")
  if [ "$status" = "200" ]; then
    ok "server responded HTTP $status at http://localhost:$PORT/"
  else
    warn "server responded HTTP $status -- retry in a few seconds"
  fi
}

show_info() {
  local ip
  ip=$(ip addr show | grep -E "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}' | cut -d/ -f1)
  echo
  echo -e "  ${GREEN}deploy complete${NC}"
  echo
  echo -e "    local:   ${YELLOW}http://localhost:$PORT/${NC}"
  echo -e "    network: ${YELLOW}http://$ip:$PORT/${NC}"
  echo -e "    solution: ${YELLOW}./solution/index.html${NC}"
  echo
  echo -e "    logs:    ${GREEN}podman logs -f $CONTAINER_NAME${NC}"
  echo -e "    stop:    ${GREEN}podman stop $CONTAINER_NAME${NC}"
  echo -e "    restart: ${GREEN}podman restart $CONTAINER_NAME${NC}"
  echo
}

main() {
  echo
  echo -e "${CYAN}nexus ctf -- deploy${NC}"
  echo -e "${CYAN}container: $CONTAINER_NAME | port: $PORT${NC}"
  echo -e "${CYAN}$(date '+%Y-%m-%d %H:%M')${NC}"
  echo

  cleanup
  build
  run
  test_health
  show_info
}

main "$@"
