-- =====================================================
-- Cash Flow Management System Database Schema
-- PostgreSQL Production Ready
-- Created: 2025-05-08
-- =====================================================

-- Set database encoding and timezone
SET client_encoding = 'UTF8';
SET timezone = 'UTC';

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- System Tables (sys)
-- =====================================================

-- sys_application: Thông tin ứng dụng
CREATE TABLE IF NOT EXISTS sys_application (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    version_mobile VARCHAR(100),
    version_web VARCHAR(100),
    author VARCHAR(255),
    process_flag VARCHAR(20),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- sys_history: Lịch sử thao tác
CREATE TABLE IF NOT EXISTS sys_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    process_id BIGINT,
    session_id BIGINT,
    description VARCHAR(255),
    method VARCHAR(10),
    api_path VARCHAR(255),
    param JSON,
    status VARCHAR(10),
    start_request_time TIMESTAMP,
    finish_request_time TIMESTAMP,
    message_response TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- =====================================================
-- Authentication Tables (auth)
-- =====================================================

-- auth_users: Quản lý user của hệ thống
CREATE TABLE IF NOT EXISTS auth_users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    avatar VARCHAR(255),
    birthday TIMESTAMP,
    age INTEGER,
    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    gender VARCHAR(10),
    province_id BIGINT,
    ward_id BIGINT,
    address VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    role_permission_id BIGINT,
    last_login_time TIMESTAMP,
    last_request_time TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- auth_sessions: Quản lý session của user
CREATE TABLE IF NOT EXISTS auth_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    refresh_token VARCHAR(255) UNIQUE,
    refresh_token_expires_at TIMESTAMP,
    refresh_token_used VARCHAR(255),
    last_request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_info VARCHAR(255),
    ip_address VARCHAR(255),
    status VARCHAR(50) DEFAULT 'ACTIVE',
    type VARCHAR(10),
    platform VARCHAR(50),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- auth_permission
CREATE TABLE IF NOT EXISTS auth_permission (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- auth_permission_screen
CREATE TABLE IF NOT EXISTS auth_permission_screen (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(10),
    navigate VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- auth_permission_screen_role
CREATE TABLE IF NOT EXISTS auth_permission_screen_role (
    id BIGSERIAL PRIMARY KEY,
    permission_screen_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- =====================================================
-- Transaction Tables (tran)
-- =====================================================

-- tran_transactions: Quản lý giao dịch hằng ngày
CREATE TABLE IF NOT EXISTS tran_transactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    type VARCHAR(50) NOT NULL,
    category_id BIGINT,
    bill_image VARCHAR(255),
    amount DOUBLE PRECISION NOT NULL,
    date TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'COMPLETED',
    formality_transaction VARCHAR(50),
    wallet_id BIGINT,
    origin_transaction_id BIGINT,
    description VARCHAR(255),
    reference VARCHAR(255),
    metadata VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- tran_transactions_detail: Quản lý chi tiết giao dịch
CREATE TABLE IF NOT EXISTS tran_transactions_detail (
    id BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    product_name VARCHAR(255),
    amount DOUBLE PRECISION,
    price DOUBLE PRECISION,
    into_money DOUBLE PRECISION,
    date TIMESTAMP,
    description VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- tran_notification: Thông báo
CREATE TABLE IF NOT EXISTS tran_notification (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    transaction_id BIGINT,
    title VARCHAR(255),
    content VARCHAR(255),
    type VARCHAR(20),
    status VARCHAR(20),
    sent_at TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- tran_accumulated_assets_time_line: Tài sản tích lũy theo timeline
CREATE TABLE IF NOT EXISTS tran_accumulated_assets_time_line (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    transaction_id BIGINT,
    asset_id BIGINT,
    unit_id BIGINT,
    value_remaining DOUBLE PRECISION,
    description VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- tran_accumulated_assets_by_date: Tài sản tích lũy theo ngày
CREATE TABLE IF NOT EXISTS tran_accumulated_assets_by_date (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    asset_id BIGINT,
    unit_id BIGINT,
    value_remaining DOUBLE PRECISION,
    description VARCHAR(255),
    date TIMESTAMP NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- tran_result_by_month: Thống kê giao dịch theo tháng
CREATE TABLE IF NOT EXISTS tran_result_by_month (
    id BIGSERIAL PRIMARY KEY,
    unit_id BIGINT,
    income DOUBLE PRECISION DEFAULT 0,
    expense DOUBLE PRECISION DEFAULT 0,
    accumulated_income DOUBLE PRECISION DEFAULT 0,
    accumulated_expense DOUBLE PRECISION DEFAULT 0,
    change_income_month_one_before DOUBLE PRECISION DEFAULT 0,
    change_expense_month_one_before DOUBLE PRECISION DEFAULT 0,
    type VARCHAR(20),
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month_before INTEGER,
    year_before INTEGER,
    description VARCHAR(255),
    date TIMESTAMP NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- =====================================================
-- Personal Finance Tables (my_)
-- =====================================================

-- my_info_asset: Thông tin tài sản cố định
CREATE TABLE IF NOT EXISTS my_info_asset (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    asset_id BIGINT,
    wallet_id BIGINT,
    amount DOUBLE PRECISION,
    price DOUBLE PRECISION,
    origin VARCHAR(255),
    status VARCHAR(20),
    description VARCHAR(255),
    unit_id BIGINT,
    transaction_date TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- my_target: Mục tiêu tài chính
CREATE TABLE IF NOT EXISTS my_target (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    income DOUBLE PRECISION,
    expense DOUBLE PRECISION,
    description VARCHAR(255),
    time_cycle DOUBLE PRECISION,
    type VARCHAR(20),
    progress DOUBLE PRECISION DEFAULT 0,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    setting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_date TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- my_target_plan: Kế hoạch mục tiêu tài chính
CREATE TABLE IF NOT EXISTS my_target_plan (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    target_id BIGINT NOT NULL,
    income DOUBLE PRECISION,
    expense DOUBLE PRECISION,
    into_money_actual DOUBLE PRECISION,
    date TIMESTAMP,
    status VARCHAR(20),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- my_expense: Thông tin chi tiêu cố định
CREATE TABLE IF NOT EXISTS my_expense (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    expense_id BIGINT,
    type VARCHAR(20),
    frequency VARCHAR(20),
    amount DOUBLE PRECISION,
    price DOUBLE PRECISION,
    into_money DOUBLE PRECISION,
    effective_date TIMESTAMP,
    exp_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    description VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- my_debt: Thông tin khoản vay/nợ
CREATE TABLE IF NOT EXISTS my_debt (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    contract_no VARCHAR(50),
    contract_date TIMESTAMP,
    counterparty_id BIGINT,
    debt_type VARCHAR(20),
    type VARCHAR(20),
    file_path_json JSON,
    frequency VARCHAR(20),
    principal_debt DOUBLE PRECISION,
    interest DOUBLE PRECISION,
    interest_rate DOUBLE PRECISION,
    insurance_fee DOUBLE PRECISION,
    into_money DOUBLE PRECISION,
    paid_amount DOUBLE PRECISION DEFAULT 0,
    remaining_amount DOUBLE PRECISION,
    cycle INTEGER,
    paymented_times INTEGER DEFAULT 0,
    start_date TIMESTAMP,
    exp_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    description VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- my_debt_detail: Thông tin chi tiết khoản vay/nợ
CREATE TABLE IF NOT EXISTS my_debt_detail (
    id BIGSERIAL PRIMARY KEY,
    my_debt_id BIGINT NOT NULL,
    principal_debt DOUBLE PRECISION,
    interest DOUBLE PRECISION,
    insurance_fee DOUBLE PRECISION,
    into_money DOUBLE PRECISION,
    paid_amount DOUBLE PRECISION,
    remaining_amount DOUBLE PRECISION,
    payment_times INTEGER,
    payment_date TIMESTAMP,
    payment_method VARCHAR(50),
    transaction_id BIGINT,
    wallet_id BIGINT,
    bill_id BIGINT,
    status VARCHAR(20),
    description VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- =====================================================
-- Configuration Tables (com)
-- =====================================================

-- com_wallets: Ví thanh toán, ngân hàng, app tài chính
CREATE TABLE IF NOT EXISTS com_wallets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(10),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- com_asset: Loại tài sản
CREATE TABLE IF NOT EXISTS com_asset (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(10),
    unit_id BIGINT,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- com_origin_transaction: Nguồn tiền giao dịch
CREATE TABLE IF NOT EXISTS com_origin_transaction (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- com_exchange_rate: Tỉ giá hiện tại
CREATE TABLE IF NOT EXISTS com_exchange_rate (
    id BIGSERIAL PRIMARY KEY,
    exchange_rate_purchase DOUBLE PRECISION,
    exchange_rate_sell DOUBLE PRECISION,
    asset_id BIGINT NOT NULL,
    description VARCHAR(255),
    origin_info VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- com_unit: Đơn vị tính
CREATE TABLE IF NOT EXISTS com_unit (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- com_categories: Danh mục giao dịch
CREATE TABLE IF NOT EXISTS com_categories (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(10),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- com_counterparty: Đối tác
CREATE TABLE IF NOT EXISTS com_counterparty (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    avatar VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id BIGINT
);

-- =====================================================
-- Indexes for Performance Optimization
-- =====================================================

-- Indexes for auth_users
CREATE INDEX IF NOT EXISTS idx_auth_users_email ON auth_users(email) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_auth_users_username ON auth_users(username) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_auth_users_status ON auth_users(status) WHERE is_deleted = FALSE;

-- Indexes for auth_sessions
CREATE INDEX IF NOT EXISTS idx_auth_sessions_user_id ON auth_sessions(user_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_auth_sessions_session_token ON auth_sessions(session_token) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_auth_sessions_expires_at ON auth_sessions(expires_at) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_auth_sessions_refresh_token ON auth_sessions(refresh_token) WHERE is_deleted = FALSE;

-- Indexes for tran_transactions
CREATE INDEX IF NOT EXISTS idx_tran_transactions_user_id ON tran_transactions(user_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_tran_transactions_date ON tran_transactions(date) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_tran_transactions_type ON tran_transactions(type) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_tran_transactions_category_id ON tran_transactions(category_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_tran_transactions_wallet_id ON tran_transactions(wallet_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_tran_transactions_status ON tran_transactions(status) WHERE is_deleted = FALSE;

-- Indexes for tran_transactions_detail
CREATE INDEX IF NOT EXISTS idx_tran_transactions_detail_transaction_id ON tran_transactions_detail(transaction_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_tran_transactions_detail_user_id ON tran_transactions_detail(user_id) WHERE is_deleted = FALSE;

-- Indexes for my_info_asset
CREATE INDEX IF NOT EXISTS idx_my_info_asset_user_id ON my_info_asset(user_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_my_info_asset_asset_id ON my_info_asset(asset_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_my_info_asset_wallet_id ON my_info_asset(wallet_id) WHERE is_deleted = FALSE;

-- Indexes for my_debt
CREATE INDEX IF NOT EXISTS idx_my_debt_user_id ON my_debt(user_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_my_debt_counterparty_id ON my_debt(counterparty_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_my_debt_status ON my_debt(status) WHERE is_deleted = FALSE;

-- Indexes for my_debt_detail
CREATE INDEX IF NOT EXISTS idx_my_debt_detail_my_debt_id ON my_debt_detail(my_debt_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_my_debt_detail_payment_date ON my_debt_detail(payment_date) WHERE is_deleted = FALSE;

-- Indexes for com_categories
CREATE INDEX IF NOT EXISTS idx_com_categories_type ON com_categories(type) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_com_categories_code ON com_categories(code) WHERE is_deleted = FALSE;

-- Indexes for sys_history
CREATE INDEX IF NOT EXISTS idx_sys_history_user_id ON sys_history(user_id) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_sys_history_start_request_time ON sys_history(start_request_time) WHERE is_deleted = FALSE;
CREATE INDEX IF NOT EXISTS idx_sys_history_api_path ON sys_history(api_path) WHERE is_deleted = FALSE;

-- =====================================================
-- Update timestamp function
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for all tables with updated_at column
CREATE TRIGGER update_sys_application_updated_at BEFORE UPDATE ON sys_application FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_sys_history_updated_at BEFORE UPDATE ON sys_history FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_auth_users_updated_at BEFORE UPDATE ON auth_users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_auth_sessions_updated_at BEFORE UPDATE ON auth_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_auth_permission_updated_at BEFORE UPDATE ON auth_permission FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_auth_permission_screen_updated_at BEFORE UPDATE ON auth_permission_screen FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_auth_permission_screen_role_updated_at BEFORE UPDATE ON auth_permission_screen_role FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tran_transactions_updated_at BEFORE UPDATE ON tran_transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tran_transactions_detail_updated_at BEFORE UPDATE ON tran_transactions_detail FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tran_notification_updated_at BEFORE UPDATE ON tran_notification FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tran_accumulated_assets_time_line_updated_at BEFORE UPDATE ON tran_accumulated_assets_time_line FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tran_accumulated_assets_by_date_updated_at BEFORE UPDATE ON tran_accumulated_assets_by_date FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_tran_result_by_month_updated_at BEFORE UPDATE ON tran_result_by_month FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_my_info_asset_updated_at BEFORE UPDATE ON my_info_asset FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_my_target_updated_at BEFORE UPDATE ON my_target FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_my_target_plan_updated_at BEFORE UPDATE ON my_target_plan FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_my_expense_updated_at BEFORE UPDATE ON my_expense FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_my_debt_updated_at BEFORE UPDATE ON my_debt FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_my_debt_detail_updated_at BEFORE UPDATE ON my_debt_detail FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_com_wallets_updated_at BEFORE UPDATE ON com_wallets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_com_asset_updated_at BEFORE UPDATE ON com_asset FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_com_origin_transaction_updated_at BEFORE UPDATE ON com_origin_transaction FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_com_exchange_rate_updated_at BEFORE UPDATE ON com_exchange_rate FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_com_unit_updated_at BEFORE UPDATE ON com_unit FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_com_categories_updated_at BEFORE UPDATE ON com_categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_com_counterparty_updated_at BEFORE UPDATE ON com_counterparty FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Insert initial data
-- =====================================================

-- Insert default application info
INSERT INTO sys_application (name, description, version_mobile, version_web, author, process_flag) 
VALUES ('Cash Flow Management', 'Personal Finance Management System', '1.0.0', '1.0.0', 'Development Team', 'READY')
ON CONFLICT DO NOTHING;

-- Insert default units
INSERT INTO com_unit (code, name) VALUES 
('VND', 'Vietnam Dong'),
('USD', 'US Dollar'),
('GOLD', 'Gold (Chỉ)'),
('SILVER', 'Silver (Lượng)'),
('BTC', 'Bitcoin'),
('ETH', 'Ethereum')
ON CONFLICT DO NOTHING;

-- Insert default asset types
INSERT INTO com_asset (code, name, type, unit_id) VALUES 
('CASH', 'Tiền mặt', 'PHYSICAL', 1),
('BANK', 'Tiền ngân hàng', 'PHYSICAL', 1),
('GOLD', 'Vàng', 'PHYSICAL', 3),
('SILVER', 'Bạc', 'PHYSICAL', 4),
('BTC', 'Bitcoin', 'DIGITAL', 5),
('ETH', 'Ethereum', 'DIGITAL', 6)
ON CONFLICT DO NOTHING;

-- Insert default transaction categories
INSERT INTO com_categories (code, name, type) VALUES 
('SALARY', 'Lương', 'INCOME'),
('BONUS', 'Thưởng', 'INCOME'),
('INVESTMENT', 'Đầu tư', 'INCOME'),
('OTHER_INCOME', 'Thu nhập khác', 'INCOME'),
('FOOD', 'Ăn uống', 'EXPENSE'),
('SHOPPING', 'Mua sắm', 'EXPENSE'),
('TRANSPORT', 'Di chuyển', 'EXPENSE'),
('ENTERTAINMENT', 'Giải trí', 'EXPENSE'),
('HEALTH', 'Sức khỏe', 'EXPENSE'),
('EDUCATION', 'Học tập', 'EXPENSE'),
('HOUSING', 'Nhà ở', 'EXPENSE'),
('UTILITIES', 'Dịch vụ', 'EXPENSE'),
('OTHER_EXPENSE', 'Chi tiêu khác', 'EXPENSE')
ON CONFLICT DO NOTHING;

-- Insert default transaction origins
INSERT INTO com_origin_transaction (code, name) VALUES 
('SALARY_1', 'Lương đợt 1'),
('SALARY_2', 'Lương đợt 2'),
('BONUS_Q1', 'Thưởng quý 1'),
('BONUS_Q2', 'Thưởng quý 2'),
('BONUS_Q3', 'Thưởng quý 3'),
('BONUS_Q4', 'Thưởng quý 4'),
('BONUS_YEAR', 'Thưởng cuối năm'),
('INVESTMENT_PROFIT', 'Lợi nhuận đầu tư'),
('LOAN', 'Vay nợ'),
('GIFT', 'Quà tặng'),
('OTHER', 'Khác')
ON CONFLICT DO NOTHING;

-- Insert default wallet types
INSERT INTO com_wallets (user_id, code, name, type) VALUES 
(0, 'CASH', 'Tiền mặt', 'CASH'),
(0, 'BANK_DEFAULT', 'Ngân hàng mặc định', 'BANK'),
(0, 'MOMO', 'Ví MoMo', 'E_WALLET'),
(0, 'ZALOPAY', 'Ví ZaloPay', 'E_WALLET'),
(0, 'VNPAY', 'Ví VNPay', 'E_WALLET')
ON CONFLICT DO NOTHING;

-- Insert default permissions
INSERT INTO auth_permission (code, name, description) VALUES 
('ADMIN', 'Administrator', 'Full system access'),
('USER', 'User', 'Basic user access'),
('VIEW_REPORTS', 'View Reports', 'Can view financial reports'),
('MANAGE_TRANSACTIONS', 'Manage Transactions', 'Can add/edit/delete transactions'),
('MANAGE_ASSETS', 'Manage Assets', 'Can manage personal assets'),
('MANAGE_DEBTS', 'Manage Debts', 'Can manage debts and loans'),
('MANAGE_TARGETS', 'Manage Targets', 'Can set and manage financial targets')
ON CONFLICT DO NOTHING;

-- Insert default permission screens
INSERT INTO auth_permission_screen (code, name, type, navigate) VALUES 
('DASHBOARD', 'Dashboard', 'WEB', '/dashboard'),
('TRANSACTIONS', 'Transactions', 'WEB', '/transactions'),
('ASSETS', 'Assets', 'WEB', '/assets'),
('DEBTS', 'Debts', 'WEB', '/debts'),
('REPORTS', 'Reports', 'WEB', '/reports'),
('SETTINGS', 'Settings', 'WEB', '/settings'),
('MOBILE_HOME', 'Mobile Home', 'MOBILE', '/mobile/home'),
('MOBILE_TRANSACTIONS', 'Mobile Transactions', 'MOBILE', '/mobile/transactions'),
('MOBILE_ASSETS', 'Mobile Assets', 'MOBILE', '/mobile/assets')
ON CONFLICT DO NOTHING;

-- =====================================================
-- Database schema created successfully
-- =====================================================
