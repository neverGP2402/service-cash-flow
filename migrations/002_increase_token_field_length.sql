-- =====================================================
-- Migration: Increase token field length for JWT tokens
-- Reason: JWT tokens are typically 300-400 characters long
-- =====================================================

-- Increase session_token and refresh_token field length
ALTER TABLE auth_sessions 
ALTER COLUMN session_token TYPE VARCHAR(500),
ALTER COLUMN refresh_token TYPE VARCHAR(500);

-- Update indexes if needed (PostgreSQL automatically updates indexes for VARCHAR changes)

-- =====================================================
-- Verification
-- =====================================================

-- Check the updated column types
SELECT 
    column_name, 
    data_type, 
    character_maximum_length
FROM information_schema.columns 
WHERE table_name = 'auth_sessions' 
    AND column_name IN ('session_token', 'refresh_token')
    AND table_schema = 'public';

-- =====================================================
-- Migration completed successfully
-- =====================================================
