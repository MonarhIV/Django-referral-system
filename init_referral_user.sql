CREATE TABLE IF NOT EXISTS referral_user (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    invite_code VARCHAR(6) UNIQUE NOT NULL,
    activated_invite_code VARCHAR(6),
    invited_by_id BIGINT REFERENCES referral_user(id)
); 