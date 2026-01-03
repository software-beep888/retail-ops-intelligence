-- Initialize retail database
-- Simple schema setup demonstrating data modeling thinking

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create schemas for organization
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;

-- Set search path for convenience
SET search_path TO public, staging, marts;

-- Create tables will be done by ingestion pipeline and dbt
-- This file exists to show database initialization thinking

COMMENT ON SCHEMA staging IS 'Raw ingested data before transformation';
COMMENT ON SCHEMA marts IS 'Business-ready data models for consumption';

-- Grant permissions (simplified for demo)
GRANT ALL PRIVILEGES ON SCHEMA public TO retail_user;
GRANT ALL PRIVILEGES ON SCHEMA staging TO retail_user;
GRANT ALL PRIVILEGES ON SCHEMA marts TO retail_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO retail_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging TO retail_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA marts TO retail_user;

-- Set statement timeout for safety
ALTER DATABASE retail_db SET statement_timeout = '30000';