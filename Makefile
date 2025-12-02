DC = docker compose

PHONY: up, down
up:
	$(DC) up -d
down:
	$(DC) down
