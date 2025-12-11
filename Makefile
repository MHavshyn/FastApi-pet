DC = docker compose
BACKEND_CONTAINER = backend1

PHONY: up down build

up:
	$(DC) up

down:
	$(DC) down

build:
	$(DC) build

bash:
	$(DC) exec -it $(BACKEND_CONTAINER) bash
