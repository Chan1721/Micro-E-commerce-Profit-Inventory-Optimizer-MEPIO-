import sqlite3

def init_database():
    """
    Initializes the local SQLite database for the MEPIO system.
    This function creates all necessary relational tables if they do not exist.
    It ensures seamless local data persistence for users, inventory, profit tracking, and stock logs.
    """
    
    # Connect to the local SQLite database file. 
    # If 'mepio_system.db' does not exist in the project directory, SQLite will automatically create it.
    conn = sqlite3.connect('mepio_system.db')
    
    # Create a cursor object to execute SQL statements and interact with the database.
    cursor = conn.cursor()

    # =========================================================================
    # 1. USER ACCOUNTS TABLE (Multi-Store Credential Management)
    # =========================================================================
    # This table stores seller profile details, encrypted passwords, and integration API tokens.
    # It serves as the data foundation for centralized multi-platform management.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Automatically increments unique ID for each user
        username TEXT NOT NULL UNIQUE,              -- Store account name (must be unique to prevent duplicates)
        password_hash TEXT NOT NULL,                -- Encrypted password string for security compliance
        shopee_api_key TEXT,                        -- API integration key for Shopee Open Platform connection
        tiktok_api_key TEXT,                        -- API integration token for TikTok Shop Seller Center connection
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Automatically logs the timestamp of registration
    )''')

    # =========================================================================
    # 2. CENTRALIZED INVENTORY TABLE (Stocking System)
    # =========================================================================
    # This table holds the master records of products. It cross-references internal SKUs, 
    # manufacturer barcodes, and distinct platform listing IDs to prevent overselling.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique internal reference ID for each product entry
        sku TEXT NOT NULL UNIQUE,                     -- Stock Keeping Unit (e.g., 'COS-MY-LIP-001') used as main identifier
        barcode TEXT UNIQUE,                          -- Commercial barcode string (EAN/UPC) captured via scanner hardware
        product_name TEXT NOT NULL,                   -- Description or title of the product item
        local_stock INTEGER DEFAULT 0,                -- Physical inventory count remaining in the local warehouse
        shopee_item_id TEXT,                          -- Unique listing identifier mapped from Shopee's server database
        tiktok_item_id TEXT,                          -- Unique product identifier mapped from TikTok's server database
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Records the last time stock or info was altered
    )''')

    # =========================================================================
    # 3. GRANULAR PROFIT RECORDS TABLE (Calculation Engine Output)
    # =========================================================================
    # This table captures detailed financial data from every calculation or simulated sale.
    # It breaks down hidden operational expenses so Teammate B can extract it for benchmarking.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profit_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique transactional receipt ID
        sku TEXT NOT NULL,                             -- Linked to the inventory SKU via Foreign Key relationship
        platform TEXT NOT NULL,                        -- Sales source channel identifier (e.g., 'Shopee', 'TikTok', 'Lazada')
        selling_price REAL NOT NULL,                   -- Product retail price listed on the respective platform (RM)
        cost_price REAL NOT NULL,                      -- Base wholesale/sourcing cost paid to suppliers (RM)
        platform_fee REAL NOT NULL,                    -- Commission and transaction fees charged by the platform ecosystem (RM)
        base_package_cost REAL DEFAULT 0,              -- Material expenditure for boxes, flyers, or bubble wraps (RM)
        labor_cost REAL DEFAULT 0,                     -- Calculated operational labor cost spent on packing per item (RM)
        buffer_cost REAL DEFAULT 0,                    -- Emergency financial buffer allocated for return/damage risks (RM)
        shipping_by_seller REAL DEFAULT 0,              -- Promotional shipping subsidies covered by the merchant (RM)
        net_profit REAL NOT NULL,                      -- Absolute pure profit calculated: Selling - (All Costs + Fees) (RM)
        sale_date DATE DEFAULT CURRENT_DATE,           -- Automatically archives the exact date of the entry record
        FOREIGN KEY (sku) REFERENCES inventory(sku)    -- Ensures data integrity by linking directly to existing inventory
    )''')

    # =========================================================================
    # 4. INVENTORY LOGS TABLE (Operational Audit Trail)
    # =========================================================================
    # Tracks the history of stock movements. Every inbound scan or outbound sale 
    # creates an entry here, proving transaction history to your supervisor.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,      -- Unique identifier for the transaction log entry
        sku TEXT NOT NULL,                             -- Affected product SKU code
        change_quantity INTEGER NOT NULL,              -- Positive values indicate restocking (+); Negative indicate sales (-)
        reason TEXT,                                   -- Description tag (e.g., 'Barcode Inbound Scan', 'Shopee Order #342')
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Exact time the inventory movement took place
    )''')

    # Commit all table schemas to save changes permanently inside the .db file
    conn.commit()
    
    # Close the connection safely to prevent file locks or memory leaks
    conn.close()
    
    print("Database initialization successful! 'mepio_system.db' created.")

# This conditional block ensures that the database initialization script runs 
# only if this specific file is executed directly (not when imported as a module).
if __name__ == "__main__":
    init_database()