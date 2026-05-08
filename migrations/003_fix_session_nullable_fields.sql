-- =====================================================
-- Migration: Fix nullable fields in auth_sessions table
-- Reason: JWT tokens may not always have explicit expiration times
-- =====================================================

-- Make timestamp fields nullable to match JWT token behavior
ALTER TABLE auth_sessions 
ALTER COLUMN expires_at DROP NOT NULL,
ALTER COLUMN refresh_token_expires_at DROP NOT NULL,
ALTER COLUMN refresh_token_used DROP NOT NULL,
ALTER COLUMN last_request_time DROP NOT NULL;

-- Also make user tracking fields nullable since they might not always be available
ALTER TABLE auth_sessions 
ALTER COLUMN created_by_user_id DROP NOT NULL,
ALTER COLUMN updated_by_user_id DROP NOT NULL;

-- =====================================================
-- Verification
-- =====================================================

-- Check the updated column constraints
SELECT 
    column_name, 
    is_nullable,
    data_type,
    character_maximum_length
FROM information_schema.columns 
WHERE table_name = 'auth_sessions' 
    AND table_schema = 'public'
ORDER BY ordinal_position;

-- =====================================================
-- Migration completed successfully
-- =====================================================
