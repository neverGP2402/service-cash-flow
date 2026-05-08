-- =====================================================
-- Rollback: Decrease token field length back to VARCHAR(255)
-- =====================================================

-- First, delete any existing sessions that might have long tokens
DELETE FROM auth_sessions WHERE 
    LENGTH(session_token) > 255 OR 
    LENGTH(refresh_token) > 255;

-- Decrease session_token and refresh_token field length
ALTER TABLE auth_sessions 
ALTER COLUMN session_token TYPE VARCHAR(255),
ALTER COLUMN refresh_token TYPE VARCHAR(255);

-- =====================================================
-- Rollback completed successfully
-- =====================================================
