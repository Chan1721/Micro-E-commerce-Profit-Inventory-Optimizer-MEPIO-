import sqlite3
import os

def clear_all_data():
    db_file = 'mepio_system.db'
    
    if os.path.exists(db_file):
        print(f"🗑️ Found database '{db_file}'. Removing file to wipe all data...")
        try:

            os.remove(db_file)
            print("✨ Database file deleted successfully! Your system is now perfectly clean.")
        except Exception as e:
            print(f"⚠️ Could not delete file (it might be locked): {e}")
            print("🔄 Attempting to clear tables manually instead...")
            

            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                

                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
                
    
                for table in tables:
                    cursor.execute(f"DELETE FROM {table};")
                    print(f"🧹 Cleared table: {table}")
                    
                conn.commit()
                conn.close()
                print("✨ All data records have been wiped from the tables!")
            except Exception as db_err:
                print(f"❌ Failed to clear database: {db_err}")
    else:
        print("ℹ️ No database file found. It's already empty!")

if __name__ == "__main__":
    clear_all_data()