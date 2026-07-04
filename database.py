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
        default_view TEXT DEFAULT 'Dashboard'
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
    CREATE TABLE IF NOT EXISTS linked_accounts (\
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        shop_id TEXT NOT NULL,
        sync_status TEXT DEFAULT 'Pending',
        last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Ensure carrier_shipments table exists at startup without dangling SELECT statements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carrier_shipments (
            shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            carrier_name TEXT,
            delivery_days REAL,
            is_on_time INTEGER,
            shipping_cost REAL
        )
    ''')

    conn.commit()
    conn.close()

    print("Database initialization successful! 'mepio_system.db' created.")


# =========================================================================
# NEW INDEPENDENT BACKEND FUNCTION (Call this from main.py)
# =========================================================================
def get_carrier_efficiency_data(carriers):
    """
    Queries the database to aggregate real logistics fulfillment metrics.
    Handles SQL exceptions internally and returns structured analytics safely.
    """
    import sqlite3

    # Default structural fallbacks to return if data is absent or an error occurs
    avg_days = [0.0] * len(carriers)
    on_time_pct = [0.0] * len(carriers)
    cost_per_pkg = [0.0] * len(carriers)

    try:
        conn = sqlite3.connect('mepio_system.db')
        cursor = conn.cursor()
        
        # Aggregate true tracking data via relational grouped selections
        cursor.execute('''
            SELECT carrier_name, 
                   AVG(delivery_days), 
                   (SUM(is_on_time) * 100.0 / COUNT(*)), 
                   AVG(shipping_cost) 
            FROM carrier_shipments 
            GROUP BY carrier_name
        ''')
        analytics_rows = cursor.fetchall()
        conn.close()

        # Map the active rows directly onto the corresponding tracking nodes
        for row in analytics_rows:
            db_name = row[0]
            if db_name in carriers:
                idx = carriers.index(db_name)
                # Neutralize potential NULL values to guard Matplotlib formatting strings
                avg_days[idx] = row[1] or 0.0
                on_time_pct[idx] = row[2] or 0.0
                cost_per_pkg[idx] = row[3] or 0.0

    except sqlite3.OperationalError as db_err:
        print(f"Logistics DB Subsystem Fault: {db_err}")

    return avg_days, on_time_pct, cost_per_pkg

def save_calculator_simulation(platform, selling_price, cost_price, fee, net_profit):
    """
    Saves a clean calculator record to the database if needed.
    [CLEANED] Isolated from standard dashboard telemetry to prevent data pollution.
    """
    import sqlite3
    try:
        conn = sqlite3.connect('mepio_system.db')
        cursor = conn.cursor()
        
        # Ensure the table structure exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profit_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT,
                platform TEXT,
                selling_price REAL,
                cost_price REAL,
                platform_fee REAL,
                net_profit REAL,
                date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert using a clean identifier "CALC_ESTIMATE" instead of polluting general stock metrics
        cursor.execute("""
            INSERT INTO profit_records (sku, platform, selling_price, cost_price, platform_fee, net_profit)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("CALC_ESTIMATE", platform, selling_price, cost_price, fee, net_profit))
        
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as db_err:
        print(f"Calculator DB Storage Fault: {db_err}")

if __name__ == "__main__":
    init_database()