import sqlite3

def init_database():
    """
    Initializes the local SQLite database for the MEPIO system.
    This function creates all necessary relational tables if they do not exist.
    It ensures seamless local data persistence for users, inventory, profit tracking, and stock logs.
    """

    conn = sqlite3.connect('mepio_system.db')
    cursor = conn.cursor()

    # =========================================================================
    # 1. USER ACCOUNTS TABLE (Multi-Store Credential Management)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        security_answer TEXT,
        shopee_api_key TEXT,
        tiktok_api_key TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # =========================================================================
    # 2. CENTRALIZED INVENTORY TABLE (Stocking System)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL UNIQUE,
        barcode TEXT UNIQUE,
        product_name TEXT NOT NULL,
        local_stock INTEGER DEFAULT 0,
        shopee_item_id TEXT,
        tiktok_item_id TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # =========================================================================
    # 3. GRANULAR PROFIT RECORDS TABLE (Calculation Engine Output)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profit_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        platform TEXT NOT NULL,
        selling_price REAL NOT NULL,
        cost_price REAL NOT NULL,
        platform_fee REAL NOT NULL,
        base_package_cost REAL DEFAULT 0,
        labor_cost REAL DEFAULT 0,
        buffer_cost REAL DEFAULT 0,
        shipping_by_seller REAL DEFAULT 0,
        net_profit REAL NOT NULL,
        sale_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (sku) REFERENCES inventory(sku)
    )''')

    # =========================================================================
    # 4. INVENTORY LOGS TABLE (Operational Audit Trail)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        change_quantity INTEGER NOT NULL,
        reason TEXT,
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # =========================================================================
    # 5. SYSTEM SETTINGS TABLE (Global Configuration & View Persistence)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_settings (
        setting_id INTEGER PRIMARY KEY CHECK (setting_id = 1),
        shopee_fee REAL DEFAULT 5.5,
        tiktok_fee REAL DEFAULT 3.2,
        lazada_fee REAL DEFAULT 4.0,
        default_view TEXT DEFAULT 'Dashboard',
        app_geometry TEXT                      
    )''')

    # --- Migration safety check: add default_view column if it doesn't exist yet ---
    # (This handles the case where an older version of mepio_system.db already exists
    # on disk without this column, since CREATE TABLE IF NOT EXISTS won't alter it.)
    cursor.execute("PRAGMA table_info(system_settings)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    if 'default_view' not in existing_columns:
        cursor.execute('''
            ALTER TABLE system_settings ADD COLUMN default_view TEXT DEFAULT 'Dashboard'
        ''')

    if 'app_geometry' not in existing_columns:
        cursor.execute("ALTER TABLE system_settings ADD COLUMN app_geometry TEXT")
        
    # Migration: add default_view column if it doesn't exist yet (for existing databases)
    cursor.execute("PRAGMA table_info(system_settings)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    if 'default_view' not in existing_columns:
        cursor.execute("ALTER TABLE system_settings ADD COLUMN default_view TEXT DEFAULT 'Dashboard'")

    cursor.execute('''
    INSERT OR IGNORE INTO system_settings (setting_id, shopee_fee, tiktok_fee, lazada_fee, default_view)
    VALUES (1, 5.5, 3.2, 4.0, 'Dashboard')
    ''')

    # =========================================================================
    # 6. RECENT TRACKING TABLE (Logistics History)
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recent_tracking (
        tracking_no TEXT PRIMARY KEY,
        courier TEXT,
        track_type TEXT,
        last_tracked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # =========================================================================
    # 7. MARKETPLACE ORDERS TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS marketplace_orders (
        order_id TEXT PRIMARY KEY,
        platform TEXT NOT NULL,
        items TEXT,
        order_value REAL DEFAULT 0.0,
        status TEXT,
        status_color TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # =========================================================================
    # 8. LINKED ACCOUNTS TABLE
    # =========================================================================
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS linked_accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        shop_id TEXT NOT NULL,
        sync_status TEXT DEFAULT 'Pending',
        last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()

    print("Database initialization successful! 'mepio_system.db' created.")

if __name__ == "__main__":
    init_database()