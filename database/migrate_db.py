
"""
Database migration script to add missing columns
Run this once to update your existing database
"""

from sqlalchemy import text, inspect
from database.database import db
from utils.error_handler import logger


def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def migrate_projects_table():
    """Add missing columns to projects table"""
    print("\n" + "="*60)
    print("🔧 Migrating Projects Table")
    print("="*60)
    
    with db.get_session() as session:
        # Check and add updated_at column
        if not check_column_exists('projects', 'updated_at'):
            print("➕ Adding 'updated_at' column...")
            try:
                session.execute(text("""
                    ALTER TABLE projects 
                    ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                """))
                print("   ✅ Added 'updated_at' column")
            except Exception as e:
                print(f"   ⚠️  Warning: {str(e)}")
        else:
            print("   ✓ 'updated_at' column already exists")
        
        # Check and add tags column
        if not check_column_exists('projects', 'tags'):
            print("➕ Adding 'tags' column...")
            try:
                # SQLite uses JSON type differently
                if db.engine.url.drivername == 'sqlite':
                    session.execute(text("""
                        ALTER TABLE projects 
                        ADD COLUMN tags TEXT
                    """))
                else:
                    session.execute(text("""
                        ALTER TABLE projects 
                        ADD COLUMN tags JSON
                    """))
                print("   ✅ Added 'tags' column")
            except Exception as e:
                print(f"   ⚠️  Warning: {str(e)}")
        else:
            print("   ✓ 'tags' column already exists")
        
        # Update existing rows to have default values
        try:
            session.execute(text("""
                UPDATE projects 
                SET updated_at = created_at 
                WHERE updated_at IS NULL
            """))
            print("   ✅ Set default updated_at values")
        except:
            pass


def migrate_papers_table():
    """Add missing columns to papers table"""
    print("\n" + "="*60)
    print("🔧 Migrating Papers Table")
    print("="*60)
    
    with db.get_session() as session:
        # Check and add missing columns
        missing_columns = {
            'doi': 'VARCHAR(255)',
            'arxiv_id': 'VARCHAR(50)',
            'semantic_scholar_id': 'VARCHAR(100)',
            'source': 'VARCHAR(50)',
            'processing_status': 'TEXT' if db.engine.url.drivername == 'sqlite' else 'JSON',
            'updated_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        }
        
        for column, column_type in missing_columns.items():
            if not check_column_exists('papers', column):
                print(f"➕ Adding '{column}' column...")
                try:
                    session.execute(text(f"""
                        ALTER TABLE papers 
                        ADD COLUMN {column} {column_type}
                    """))
                    print(f"   ✅ Added '{column}' column")
                except Exception as e:
                    print(f"   ⚠️  Warning: {str(e)}")
            else:
                print(f"   ✓ '{column}' column already exists")


def verify_migration():
    """Verify that all columns exist"""
    print("\n" + "="*60)
    print("✅ Verifying Migration")
    print("="*60)
    
    inspector = inspect(db.engine)
    
    # Check projects table
    project_columns = [col['name'] for col in inspector.get_columns('projects')]
    print("\nProjects table columns:")
    for col in project_columns:
        print(f"   ✓ {col}")
    
    required_project_cols = ['id', 'name', 'description', 'tags', 'created_at', 'updated_at']
    missing_project_cols = [col for col in required_project_cols if col not in project_columns]
    
    if missing_project_cols:
        print(f"\n⚠️  Missing columns in projects: {missing_project_cols}")
    else:
        print("\n✅ All required columns present in projects table")
    
    # Check papers table
    paper_columns = [col['name'] for col in inspector.get_columns('papers')]
    print("\nPapers table columns:")
    for col in paper_columns[:10]:  # Show first 10
        print(f"   ✓ {col}")
    if len(paper_columns) > 10:
        print(f"   ... and {len(paper_columns) - 10} more")
    
    print("\n✅ Migration verification complete!")


def main():
    """Run all migrations"""
    print("\n" + "="*60)
    print("🚀 DATABASE MIGRATION SCRIPT")
    print("="*60)
    print("\nThis script will update your database schema to match")
    print("the latest models without losing existing data.")
    print("\nPress Ctrl+C to cancel, or Enter to continue...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
        return
    
    try:
        # Run migrations
        migrate_projects_table()
        migrate_papers_table()
        verify_migration()
        
        print("\n" + "="*60)
        print("🎉 MIGRATION COMPLETE!")
        print("="*60)
        print("\nYou can now run the application without errors.")
        print("Run: streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        logger.error(f"Migration error: {str(e)}")
        print("\nIf you continue to have issues, you may need to:")
        print("1. Backup your database")
        print("2. Delete the database file")
        print("3. Run: python -c 'from database.database import db; db.create_tables()'")


if __name__ == "__main__":
    main()