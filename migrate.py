from database import engine, Base

# Jalankan migrasi
if __name__ == "__main__":
    print("Migrating database...")
    Base.metadata.create_all(bind=engine)
    print("Migration completed!")
