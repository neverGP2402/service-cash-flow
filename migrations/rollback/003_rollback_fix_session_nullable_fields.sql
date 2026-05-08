-- =====================================================
-- Rollback: Make session fields NOT NULL again
-- =====================================================

-- First, update any NULL values to defaults
UPDATE auth_sessions SET 
    expires_at = CURRENT_TIMESTAMP + INTERVAL '1 hour' WHERE expires_at IS NULL,
    refresh_token_expires_at = CURRENT_TIMESTAMP + INTERVAL '7 days' WHERE refresh_token_expires_at IS NULL,
    refresh_token_used = '' WHERE refresh_token_used IS NULL,
    last_request_time = CURRENT_TIMESTAMP WHERE last_request_time IS NULL,
    created_by_user_id = 0 WHERE created_by_user_id IS NULL,
    updated_by_user_id = 0 WHERE updated_by_user_id IS NULL;

-- Make fields NOT NULL again
ALTER TABLE auth_sessions 
ALTER COLUMN expires_at SET NOT NULL,
ALTER COLUMN refresh_token_expires_at SET NOT NULL,
ALTER COLUMN refresh_token_used SET NOT NULL,
ALTER COLUMN last_request_time SET NOT NULL,
ALTER COLUMN created_by_user_id SET NOT NULL,
ALTER COLUMN updated_by_user_id SET NOT NULL;

-- =====================================================
-- Rollback completed successfully
-- =====================================================
