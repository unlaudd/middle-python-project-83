# =============================================================================
# Page Analyzer - Makefile
# =============================================================================
# This Makefile provides commands for development, testing, building,
# and deploying the Page Analyzer application.
#
# Usage:
#   make <command>
#   make help    - Display available commands
#
# =============================================================================

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# Port for the application server (can be overridden via environment variable)
PORT ?= 8000

# Python package name
PACKAGE = page_analyzer

# =============================================================================
# Default target - show help
# =============================================================================
.DEFAULT_GOAL := help

# =============================================================================
# Help command - display all available commands with descriptions
# =============================================================================
.PHONY: help
help: ## Show this help message
	@echo "Page Analyzer - Available commands:"
	@echo ""
	@echo "  Development:"
	@echo "    make install       Install all dependencies"
	@echo "    make dev           Run application in development mode"
	@echo "    make start         Run application in production mode"
	@echo ""
	@echo "  Code Quality:"
	@echo "    make lint          Run flake8 linter"
	@echo "    make check         Run all checks (lint)"
	@echo ""
	@echo "  Build & Deploy:"
	@echo "    make build         Build application for deployment"
	@echo "    make render-start  Start application on Render.com"
	@echo ""
	@echo "  Utilities:"
	@echo "    make clean         Remove temporary files and cache"
	@echo ""
	@echo "Run 'make <command>' to execute a specific command."

# =============================================================================
# Development commands
# =============================================================================
.PHONY: install
install: ## Install all project dependencies using uv
	uv sync

.PHONY: dev
dev: ## Run the application in development mode with debug enabled
	uv run flask --debug --app $(PACKAGE):app run

.PHONY: start
start: ## Run the application in production mode using gunicorn
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) $(PACKAGE):app

# =============================================================================
# Build and deployment commands
# =============================================================================
.PHONY: build
build: ## Build the application for deployment (used on Render.com)
	./build.sh

.PHONY: render-start
render-start: ## Start the application on Render.com platform
	gunicorn -w 5 -b 0.0.0.0:$(PORT) $(PACKAGE):app

# =============================================================================
# Code quality commands
# =============================================================================
.PHONY: lint
lint: ## Run flake8 linter to check code style
	uv run flake8 $(PACKAGE)

.PHONY: check
check: lint ## Run all code quality checks
	@echo "All checks passed!"

# =============================================================================
# Utility commands
# =============================================================================
.PHONY: clean
clean: ## Remove temporary files, cache, and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete
	find . -type f -name "*$$py.class" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	@echo "Cleaned up temporary files"