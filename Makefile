# Makefile for CompositionAssistant
# ==================================

.PHONY: help info build build-api build-ui up down restart logs logs-api logs-ui \
        clean clean-all shell-api shell-ui status health test lint \
        install-deps dev setup setup-env setup-personal check-ollama check-soundfont

# Default target
.DEFAULT_GOAL := help

# Project info
APP_NAME := Composition Assistant
VERSION := 1.0.0
IMAGE_NAME := composition-assistant-api
UI_IMAGE_NAME := composition-assistant-ui
CONTAINER_NAME := composition-assistant-api
UI_CONTAINER_NAME := composition-assistant-ui
API_PORT := 8000
UI_PORT := 3000

# Detect docker compose command (v2 uses 'docker compose', v1 uses 'docker-compose')
DOCKER_COMPOSE := $(shell docker compose version > /dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
CYAN := \033[0;36m
BOLD := \033[1m
NC := \033[0m # No Color

# =============================================================================
# HELP & INFO
# =============================================================================

help: ## Show this help message
	@echo "$(BLUE)$(APP_NAME) - Available Commands$(NC)"
	@echo "============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

info: ## Show project information and endpoints
	@echo ""
	@echo "$(BOLD)$(CYAN)╔══════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BOLD)$(CYAN)║              🎵 COMPOSITION ASSISTANT                            ║$(NC)"
	@echo "$(BOLD)$(CYAN)╚══════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(BOLD)Project Information$(NC)"
	@echo "────────────────────────────────────────────────────────────────────"
	@echo "  $(GREEN)Name:$(NC)        $(APP_NAME)"
	@echo "  $(GREEN)Version:$(NC)     $(VERSION)"
	@echo "  $(GREEN)Description:$(NC) AI-powered music transformation and composition"
	@echo ""
	@echo "$(BOLD)Services$(NC)"
	@echo "────────────────────────────────────────────────────────────────────"
	@echo "  $(GREEN)API:$(NC)         $(CONTAINER_NAME) (Port $(API_PORT))"
	@echo "  $(GREEN)UI:$(NC)          $(UI_CONTAINER_NAME) (Port $(UI_PORT))"
	@echo ""
	@echo "$(BOLD)API Endpoints$(NC)"
	@echo "────────────────────────────────────────────────────────────────────"
	@echo "  $(CYAN)POST$(NC)  /process-wav/       Process audio with AI transformation"
	@echo "  $(CYAN)GET$(NC)   /download/{file}    Download processed audio file"
	@echo "  $(CYAN)GET$(NC)   /health             Health check endpoint"
	@echo "  $(CYAN)GET$(NC)   /status             Detailed status check"
	@echo "  $(CYAN)GET$(NC)   /metrics            Prometheus metrics"
	@echo "  $(CYAN)GET$(NC)   /workflow-diagram   Interactive workflow diagram"
	@echo "  $(CYAN)GET$(NC)   /config             System configuration"
	@echo "  $(CYAN)GET$(NC)   /ollama/status      Ollama connection status"
	@echo "  $(CYAN)GET$(NC)   /docs               Swagger API documentation"
	@echo "  $(CYAN)GET$(NC)   /redoc              ReDoc API documentation"
	@echo ""
	@echo "$(BOLD)URLs (when running)$(NC)"
	@echo "────────────────────────────────────────────────────────────────────"
	@echo "  $(GREEN)API:$(NC)              http://localhost:$(API_PORT)"
	@echo "  $(GREEN)API Docs:$(NC)         http://localhost:$(API_PORT)/docs"
	@echo "  $(GREEN)Metrics:$(NC)          http://localhost:$(API_PORT)/metrics"
	@echo "  $(GREEN)Workflow Diagram:$(NC) http://localhost:$(API_PORT)/workflow-diagram"
	@echo "  $(GREEN)UI:$(NC)               http://localhost:$(UI_PORT)"
	@echo ""
	@echo "$(BOLD)Supported Transformations$(NC)"
	@echo "────────────────────────────────────────────────────────────────────"
	@echo "  • Interval changes (transpose notes up/down)"
	@echo "  • Modal shifts (change musical scale/mode)"
	@echo "  • Rhythmic alterations (adjust timing/tempo)"
	@echo "  • Register changes (move octaves)"
	@echo ""
	@echo "$(BOLD)Tech Stack$(NC)"
	@echo "────────────────────────────────────────────────────────────────────"
	@echo "  $(GREEN)Backend:$(NC)     FastAPI, Python 3.11"
	@echo "  $(GREEN)LLM:$(NC)         Ollama (configurable model)"
	@echo "  $(GREEN)Audio:$(NC)       basic-pitch, FluidSynth, pretty_midi"
	@echo "  $(GREEN)Metrics:$(NC)     Prometheus"
	@echo ""
	@echo "$(BOLD)Quick Start$(NC)"
	@echo "────────────────────────────────────────────────────────────────────"
	@echo "  $(YELLOW)make setup$(NC)   - Initial setup (create .env)"
	@echo "  $(YELLOW)make start$(NC)   - Build and run all services"
	@echo "  $(YELLOW)make stop$(NC)    - Stop all services"
	@echo "  $(YELLOW)make logs$(NC)    - View logs"
	@echo "  $(YELLOW)make health$(NC)  - Check service health"
	@echo ""

# =============================================================================
# SETUP COMMANDS
# =============================================================================

setup: setup-env-copy check-env ## Quick setup (copy .env.example)
	@echo ""
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)Setup completed!$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Edit .env file with your configuration"
	@echo "  2. make check-soundfont (verify SoundFont exists)"
	@echo "  3. make check-ollama    (verify Ollama is running)"
	@echo "  4. make start           (build and run)"
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"

setup-full: setup-env check-soundfont check-ollama ## Full interactive setup
	@echo ""
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)Full setup completed!$(NC)"
	@echo "$(YELLOW)Next: make start$(NC)"
	@echo "$(GREEN)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"

setup-env: ## Configure .env interactively
	@chmod +x scripts/setup-env.sh 2>/dev/null || true
	@bash scripts/setup-env.sh

setup-env-copy: ## Copy .env.example to .env (if not exists)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✓ .env created from .env.example$(NC)"; \
		echo "$(YELLOW)  Edit .env to customize your configuration$(NC)"; \
	else \
		echo "$(YELLOW)⚠ .env already exists$(NC)"; \
	fi

setup-personal: ## Load saved personal configuration
	@if [ -f scripts/setup-personal.sh ]; then \
		chmod +x scripts/setup-personal.sh; \
		bash scripts/setup-personal.sh; \
	else \
		echo "$(RED)Error: scripts/setup-personal.sh not found$(NC)"; \
		echo "$(YELLOW)Copy from template: cp scripts/setup-personal.sh.template scripts/setup-personal.sh$(NC)"; \
		exit 1; \
	fi

check-env: ## Check environment configuration
	@echo "$(BLUE)Checking environment...$(NC)"
	@if [ -f .env ]; then \
		echo "$(GREEN)✓ .env file exists$(NC)"; \
	else \
		echo "$(RED)✗ .env file not found$(NC)"; \
		echo "$(YELLOW)  Run: make setup$(NC)"; \
	fi

check-ollama: ## Check if Ollama is running
	@chmod +x scripts/check-ollama.sh 2>/dev/null || true
	@bash scripts/check-ollama.sh

check-soundfont: ## Check if SoundFont file exists
	@chmod +x scripts/check-soundfont.sh 2>/dev/null || true
	@bash scripts/check-soundfont.sh

# =============================================================================
# BUILD COMMANDS
# =============================================================================

build: ## Build all Docker images
	@echo "$(BLUE)Building all services...$(NC)"
	$(DOCKER_COMPOSE) build

build-api: ## Build only the API image
	@echo "$(BLUE)Building API service...$(NC)"
	$(DOCKER_COMPOSE) build $(CONTAINER_NAME)

build-ui: ## Build only the UI image
	@echo "$(BLUE)Building UI service...$(NC)"
	$(DOCKER_COMPOSE) build $(UI_CONTAINER_NAME)

build-no-cache: ## Build all images without cache
	@echo "$(BLUE)Building all services (no cache)...$(NC)"
	$(DOCKER_COMPOSE) build --no-cache

# =============================================================================
# RUN COMMANDS
# =============================================================================

up: ## Start all services in detached mode
	@echo "$(GREEN)Starting all services...$(NC)"
	$(DOCKER_COMPOSE) up -d

up-attached: ## Start all services with logs attached
	@echo "$(GREEN)Starting all services (attached)...$(NC)"
	$(DOCKER_COMPOSE) up

up-api: ## Start only the API service
	@echo "$(GREEN)Starting API service...$(NC)"
	$(DOCKER_COMPOSE) up -d $(CONTAINER_NAME)

up-ui: ## Start only the UI service
	@echo "$(GREEN)Starting UI service...$(NC)"
	$(DOCKER_COMPOSE) up -d $(UI_CONTAINER_NAME)

down: ## Stop all services
	@echo "$(YELLOW)Stopping all services...$(NC)"
	$(DOCKER_COMPOSE) down

restart: down up ## Restart all services

restart-api: ## Restart only the API service
	@echo "$(YELLOW)Restarting API service...$(NC)"
	$(DOCKER_COMPOSE) restart $(CONTAINER_NAME)

restart-ui: ## Restart only the UI service
	@echo "$(YELLOW)Restarting UI service...$(NC)"
	$(DOCKER_COMPOSE) restart $(UI_CONTAINER_NAME)

# =============================================================================
# LOGGING COMMANDS
# =============================================================================

logs: ## View logs for all services (follow)
	$(DOCKER_COMPOSE) logs -f

logs-api: ## View logs for API service (follow)
	$(DOCKER_COMPOSE) logs -f $(CONTAINER_NAME)

logs-ui: ## View logs for UI service (follow)
	$(DOCKER_COMPOSE) logs -f $(UI_CONTAINER_NAME)

logs-tail: ## View last 100 lines of all logs
	$(DOCKER_COMPOSE) logs --tail=100

# =============================================================================
# SHELL ACCESS
# =============================================================================

shell-api: ## Open a shell in the API container
	@echo "$(BLUE)Opening shell in API container...$(NC)"
	docker exec -it $(CONTAINER_NAME) /bin/bash

shell-ui: ## Open a shell in the UI container
	@echo "$(BLUE)Opening shell in UI container...$(NC)"
	docker exec -it $(UI_CONTAINER_NAME) /bin/sh

# =============================================================================
# STATUS & HEALTH
# =============================================================================

status: ## Show status of all services
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(BLUE)$(APP_NAME) Status$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo ""
	@echo "$(YELLOW)Configuration:$(NC)"
	@if [ -f .env ]; then \
		echo "  $(GREEN)✓$(NC) .env"; \
	else \
		echo "  $(RED)✗$(NC) .env (run: make setup)"; \
	fi
	@if [ -f ./transcriptionLibs/FluidR3_GM/FluidR3_GM.sf2 ] || [ -f ./FluidR3_GM/FluidR3_GM.sf2 ]; then \
		echo "  $(GREEN)✓$(NC) SoundFont"; \
	else \
		echo "  $(RED)✗$(NC) SoundFont (run: make check-soundfont)"; \
	fi
	@echo ""
	@echo "$(YELLOW)Docker Images:$(NC)"
	@docker images $(IMAGE_NAME):latest --format "  $(GREEN)✓$(NC) $(IMAGE_NAME):latest" 2>/dev/null || echo "  $(RED)✗$(NC) $(IMAGE_NAME) (run: make build)"
	@docker images $(UI_IMAGE_NAME):latest --format "  $(GREEN)✓$(NC) $(UI_IMAGE_NAME):latest" 2>/dev/null || echo "  $(RED)✗$(NC) $(UI_IMAGE_NAME) (run: make build)"
	@echo ""
	@echo "$(YELLOW)Containers:$(NC)"
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(YELLOW)Services:$(NC)"
	@curl -sf http://localhost:$(API_PORT)/health > /dev/null 2>&1 \
		&& echo "  $(GREEN)✓$(NC) API running at http://localhost:$(API_PORT)" \
		|| echo "  $(RED)✗$(NC) API not running"
	@curl -sf http://localhost:$(UI_PORT)/ > /dev/null 2>&1 \
		&& echo "  $(GREEN)✓$(NC) UI running at http://localhost:$(UI_PORT)" \
		|| echo "  $(RED)✗$(NC) UI not running"

health: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(NC)"
	@echo ""
	@echo "$(GREEN)API Health:$(NC)"
	@curl -s http://localhost:$(API_PORT)/health | python3 -m json.tool 2>/dev/null || echo "$(RED)API not responding$(NC)"
	@echo ""
	@echo "$(GREEN)Ollama Status:$(NC)"
	@curl -s http://localhost:$(API_PORT)/ollama/status | python3 -m json.tool 2>/dev/null || echo "$(RED)Cannot check Ollama status$(NC)"
	@echo ""
	@echo "$(GREEN)API Metrics (first 20 lines):$(NC)"
	@curl -s http://localhost:$(API_PORT)/metrics | head -20 2>/dev/null || echo "$(RED)Metrics not available$(NC)"

# =============================================================================
# CLEANUP COMMANDS
# =============================================================================

clean: ## Stop and remove containers
	@echo "$(YELLOW)Cleaning up containers...$(NC)"
	$(DOCKER_COMPOSE) down -v

clean-all: ## Remove all containers, images, and volumes
	@echo "$(RED)Removing all containers, images, and volumes...$(NC)"
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans

clean-tmp: ## Clean temporary files
	@echo "$(YELLOW)Cleaning temporary files...$(NC)"
	rm -rf ./tmp/input/* ./tmp/output/*

clean-images: ## Remove dangling images
	@echo "$(YELLOW)Removing dangling images...$(NC)"
	docker image prune -f

# =============================================================================
# DEVELOPMENT COMMANDS
# =============================================================================

dev: ## Run API in development mode (with hot reload)
	@echo "$(GREEN)Starting API in development mode...$(NC)"
	uvicorn src.main:app --reload --host 0.0.0.0 --port $(API_PORT)

install-deps: ## Install Python dependencies locally
	@echo "$(BLUE)Installing dependencies...$(NC)"
	pip install -r requirements.txt

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ -v

lint: ## Run linter
	@echo "$(BLUE)Running linter...$(NC)"
	flake8 src/ --max-line-length=120

# =============================================================================
# UTILITY COMMANDS
# =============================================================================

open-api: ## Open API docs in browser
	@echo "$(BLUE)Opening API docs...$(NC)"
	@which xdg-open > /dev/null 2>&1 && xdg-open http://localhost:$(API_PORT)/docs || \
	which open > /dev/null 2>&1 && open http://localhost:$(API_PORT)/docs || \
	echo "$(YELLOW)Open http://localhost:$(API_PORT)/docs in your browser$(NC)"

open-ui: ## Open UI in browser
	@echo "$(BLUE)Opening UI...$(NC)"
	@which xdg-open > /dev/null 2>&1 && xdg-open http://localhost:$(UI_PORT) || \
	which open > /dev/null 2>&1 && open http://localhost:$(UI_PORT) || \
	echo "$(YELLOW)Open http://localhost:$(UI_PORT) in your browser$(NC)"

open-diagram: ## Open workflow diagram in browser
	@echo "$(BLUE)Opening workflow diagram...$(NC)"
	@which xdg-open > /dev/null 2>&1 && xdg-open http://localhost:$(API_PORT)/workflow-diagram || \
	which open > /dev/null 2>&1 && open http://localhost:$(API_PORT)/workflow-diagram || \
	echo "$(YELLOW)Open http://localhost:$(API_PORT)/workflow-diagram in your browser$(NC)"

open-metrics: ## Open metrics endpoint in browser
	@echo "$(BLUE)Opening metrics...$(NC)"
	@which xdg-open > /dev/null 2>&1 && xdg-open http://localhost:$(API_PORT)/metrics || \
	which open > /dev/null 2>&1 && open http://localhost:$(API_PORT)/metrics || \
	echo "$(YELLOW)Open http://localhost:$(API_PORT)/metrics in your browser$(NC)"

# =============================================================================
# QUICK START
# =============================================================================

start: build up status ## Build and start all services (quick start)
	@echo ""
	@echo "$(GREEN)✓ $(APP_NAME) is running!$(NC)"
	@echo ""
	@echo "  $(CYAN)API:$(NC)              http://localhost:$(API_PORT)"
	@echo "  $(CYAN)API Docs:$(NC)         http://localhost:$(API_PORT)/docs"
	@echo "  $(CYAN)Metrics:$(NC)          http://localhost:$(API_PORT)/metrics"
	@echo "  $(CYAN)Workflow Diagram:$(NC) http://localhost:$(API_PORT)/workflow-diagram"
	@echo "  $(CYAN)UI:$(NC)               http://localhost:$(UI_PORT)"
	@echo ""
	@echo "  Run $(YELLOW)make info$(NC) for more details"
	@echo ""

stop: down ## Alias for down

# =============================================================================
# COMBINED COMMANDS
# =============================================================================

docker-start: setup-env-copy check-soundfont build up status ## Setup + build + start (first time)

docker-rebuild: down build up ## Rebuild and restart all

docker-personal: setup-personal check-soundfont build up status ## Load personal config + build + start
