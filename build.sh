#!/usr/bin/env bash
# =============================================================================
# Page Analyzer - Build Script for Render.com
# =============================================================================
# This script is executed during the build process on Render.com.
# It installs the uv package manager, sets up Python dependencies,
# and runs database migrations.
#
# Required Environment Variables:
#   DATABASE_URL - PostgreSQL connection string for schema initialization
#
# Usage:
#   ./build.sh
#
# Note: This script is called by 'make build' command.
# =============================================================================

set -e  # Exit immediately if a command exits with a non-zero status

# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Source uv environment to make it available in PATH
source $HOME/.local/bin/env

# Install Python dependencies and run database migrations
# make install - installs all dependencies from pyproject.toml
# psql - executes database.sql to create/verify tables
make install && psql -a -d $DATABASE_URL -f database.sql