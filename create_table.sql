CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(250) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    is_active CHAR(1) NOT NULL,
    is_verified_at DATE,
    registered_at DATE,
    updated_at DATE,
    created_at DATE
);
