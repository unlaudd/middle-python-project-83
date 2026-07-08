-- =============================================================================
-- Page Analyzer - Database Schema
-- =============================================================================
-- This file contains the database schema for the Page Analyzer application.
-- It is executed during the build process on Render.com to initialize
-- the PostgreSQL database structure.
--
-- Tables:
--   urls         - Stores analyzed URLs with their creation dates
--   url_checks   - Stores check results including HTTP status codes and SEO metadata
--
-- Usage:
--   psql -d $DATABASE_URL -f database.sql
--
-- Note: This script uses CREATE TABLE IF NOT EXISTS to ensure idempotency.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Table: urls
-- -----------------------------------------------------------------------------
-- Stores unique URLs that have been submitted for analysis.
-- Each URL can have multiple associated checks over time.
CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

-- -----------------------------------------------------------------------------
-- Table: url_checks
-- -----------------------------------------------------------------------------
-- Stores individual check results for each URL.
-- Contains HTTP response data and extracted SEO metadata.
-- A URL can have multiple checks, creating a history of analysis results.
CREATE TABLE IF NOT EXISTS url_checks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER REFERENCES urls(id),
    status_code INTEGER,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at DATE DEFAULT CURRENT_DATE
);