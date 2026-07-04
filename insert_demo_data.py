import sqlite3
import datetime
import random
import os
from database import init_database  

def inject_demo_data():
    db_file = 'mepio_system.db'
    

    if os.path.exists(db_file):
        print(f"🗑️ Found existing database '{db_file}'. Removing it to prevent schema conflicts...")
        try:
            os.remove(db_file)
        except Exception as e:
            print(f"⚠️ Could not remove old DB file (Please close DB Browser or VS Code SQLite extension): {e}")

    print("🚀 Running system database structure initialization...")
    init_database()  
    
    print("🚀 Connecting to database to seed professional mock e-commerce parameters...")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()


    print("📦 Injecting system settings...")
    cursor.execute('''
        INSERT OR REPLACE INTO system_settings (setting_id, shopee_fee, tiktok_fee, lazada_fee, default_view)
        VALUES (1, 5.5, 3.2, 4.0, 'Dashboard')
    ''')


    print("📦 Injecting inventory data...")
    mock_products = [
        ("SKU-COSM-001", "BAR-001", "Glow Serum Vitamin C 30ml", 120, "SHP-001", "TTK-001"),
        ("SKU-COSM-002", "BAR-002", "Hydrating Moisturizer Cream 50g", 15, "SHP-002", "TTK-002"), 
        ("SKU-CARE-003", "BAR-003", "Organic Aloe Vera Soothing Gel", 85, "SHP-003", "TTK-003"),
        ("SKU-WAT-004", "BAR-004", "Minimalist Quartz Watch Rose Gold", 40, "SHP-004", "TTK-004"),
        ("SKU-WAT-005", "BAR-005", "Classic Leather Chronograph Watch", 8, "SHP-005", "TTK-005")   
    ]

    for sku, barcode, name, stock, shopee_id, tiktok_id in mock_products:
        cursor.execute('''
            INSERT INTO inventory (sku, barcode, product_name, local_stock, shopee_item_id, tiktok_item_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sku, barcode, name, stock, shopee_id, tiktok_id))


    print("📦 Injecting linked accounts...")
    mock_channels = [
        ("Shopee", "MY_Beauty_Cosmetics_Official", "Active", "2026-07-04 10:30:12"),
        ("TikTok Shop", "GlowUp_Skincare_Store", "Active", "2026-07-04 11:15:45"),
        ("Lazada", "Mepio_Timepieces_Mall", "Active", "2026-07-04 09:20:00")
    ]
    for platform, shop_id, status, last_sync in mock_channels:
        cursor.execute('''
            INSERT INTO linked_accounts (platform, shop_id, sync_status, last_synced)
            VALUES (?, ?, ?, ?)
        ''', (platform, shop_id, status, last_sync))


    print("📦 Injecting marketplace orders...")
    platforms = ["Shopee", "TikTok Shop", "Lazada"]
    statuses = [
        ("Completed", "#2ecc71"), 
        ("Shipping", "#3498db"), 
        ("Pending", "#f1c40f")
    ]
    
    for i in range(1, 26):
        order_id = f"ORD-2026-{1000 + i}"
        platform = random.choice(platforms)
        status_text, status_color = random.choice(statuses)
        order_val = round(random.uniform(25.5, 289.9), 2)
        
        days_ago = random.randint(0, 10)
        created_at = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
        items_summary = f"Product Pack x{random.randint(1, 3)}"

        cursor.execute('''
            INSERT INTO marketplace_orders (order_id, platform, items, order_value, status, status_color, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (order_id, platform, items_summary, order_val, status_text, status_color, created_at))

    conn.commit()
    conn.close()
    print("✨ Relational databases seeded! 'mepio_system.db' is now stacked with mock data.")

if __name__ == "__main__":
    inject_demo_data()