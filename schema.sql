CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(150) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE currencies (
    currency_id INT AUTO_INCREMENT PRIMARY KEY,
    currency_code VARCHAR(10) NOT NULL UNIQUE, -- Ej: USD, ARS
    currency_name VARCHAR(50) NOT NULL
);

CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50),
    currency_id INT NOT NULL,
    initial_balance DECIMAL(15, 2) DEFAULT 0,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (currency_id) REFERENCES currencies(currency_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    supplier_description VARCHAR(255)
);

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    category_type ENUM('income', 'expense', 'transfer') NOT NULL
);

CREATE TABLE subcategories (
    subcategory_id INT AUTO_INCREMENT PRIMARY KEY,
    subcategory_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE currency_exchange (
    exchange_id INT AUTO_INCREMENT PRIMARY KEY,
    from_currency_id INT NOT NULL,
    to_currency_id INT NOT NULL,
    exchange_rate DECIMAL(15, 6) NOT NULL,
    exchange_date DATETIME NOT NULL,
    FOREIGN KEY (from_currency_id) REFERENCES currencies(currency_id),
    FOREIGN KEY (to_currency_id) REFERENCES currencies(currency_id),
    INDEX idx_exchange_date (exchange_date)
);

CREATE TABLE transfers (
    transfer_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id_from INT NOT NULL,
    account_id_to INT NOT NULL,
    transfer_amount DECIMAL(15, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id_from) REFERENCES accounts(account_id),
    FOREIGN KEY (account_id_to) REFERENCES accounts(account_id)
);

CREATE TABLE records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    subcategory_id INT NOT NULL,
    record_amount DECIMAL(15, 2) NOT NULL,
    record_type ENUM('income', 'expense', 'transfer') NOT NULL,
    record_description VARCHAR(255),
    record_date DATETIME NOT NULL,
    supplier_id INT,
    exchange_id INT,
    transfer_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(subcategory_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (exchange_id) REFERENCES currency_exchange(exchange_id),
    FOREIGN KEY (transfer_id) REFERENCES transfers(transfer_id),
    INDEX idx_record_date (record_date)
);

