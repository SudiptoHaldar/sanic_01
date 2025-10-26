"""
Create Basic Info Data Script

This script connects to the PostgreSQL database and inserts
placeholder company basic information into the org_basic_info table.
"""

import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from parent directory .env file
load_dotenv()

# Placeholder data from basic.py
PLACEHOLDER_DATA = [
    {
        'symbol': 'JPM',
        'company_name': 'JP Morgan Chase & Co.',
        'currency': 'USD',
        'annual_revenue': '78900000000',
        'annual_profit': '177556000000'
    },
    {
        'symbol': 'AAPL',
        'company_name': 'Apple Inc.',
        'currency': 'USD',
        'annual_revenue': '394300000000',
        'annual_profit': '995800000000'
    },
    {
        'symbol': 'GOOGL',
        'company_name': 'Alphabet Inc.',
        'currency': 'USD',
        'annual_revenue': '307400000000',
        'annual_profit': '738000000000'
    }
]


def get_db_connection():
    """
    Create and return a PostgreSQL database connection using .env credentials.

    Returns:
    --------
    psycopg2.connection
        Database connection object
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv('postgres_host'),
            port=os.getenv('postgres_port', 5432),
            database=os.getenv('postgres_database', 'ResearchAssistant'),
            user=os.getenv('postgres_user'),
            password=os.getenv('postgres_password')
        )
        print(f"✓ Successfully connected to database: {os.getenv('postgres_database', '--unknown--')}")
        return conn
    except psycopg2.Error as e:
        print(f"✗ Error connecting to database: {e}")
        raise


def create_table_if_not_exists(cursor):
    """
    Create the org_basic_info table if it doesn't exist.

    Parameters:
    -----------
    cursor : psycopg2.cursor
        Database cursor object
    """
    create_table_query = """
CREATE TABLE IF NOT EXISTS public.org_basic_info
(
    symbol text COLLATE pg_catalog."default" NOT NULL,
    company_name text COLLATE pg_catalog."default",
    currency text COLLATE pg_catalog."default",
    annual_revenue bigint,
    annual_profit bigint,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT org_basic_info_pkey PRIMARY KEY (symbol)
);
    """

    try:
        cursor.execute(create_table_query)
        print("✓ Table org_basic_info ready")
    except psycopg2.Error as e:
        print(f"✗ Error creating table: {e}")
        raise


def insert_basic_info(cursor, data):
    """
    Insert company basic information into org_basic_info table.
    Uses ON CONFLICT to update existing records.

    Parameters:
    -----------
    cursor : psycopg2.cursor
        Database cursor object
    data : list[dict]
        List of company data dictionaries
    """
    insert_query = """
    INSERT INTO org_basic_info (symbol, company_name, currency, annual_revenue, annual_profit)
    VALUES (%(symbol)s, %(company_name)s, %(currency)s, %(annual_revenue)s, %(annual_profit)s)
    ON CONFLICT (symbol)
    DO UPDATE SET
        company_name = EXCLUDED.company_name,
        currency = EXCLUDED.currency,
        annual_revenue = EXCLUDED.annual_revenue,
        annual_profit = EXCLUDED.annual_profit,
        updated_at = CURRENT_TIMESTAMP;
    """

    inserted_count = 0
    updated_count = 0

    for record in data:
        try:
            # Check if record exists
            cursor.execute("SELECT symbol FROM org_basic_info WHERE symbol = %s", (record['symbol'],))
            exists = cursor.fetchone() is not None

            # Insert or update
            cursor.execute(insert_query, record)

            if exists:
                updated_count += 1
                print(f"  ↻ Updated: {record['symbol']} - {record['company_name']}")
            else:
                inserted_count += 1
                print(f"  ✓ Inserted: {record['symbol']} - {record['company_name']}")

        except psycopg2.Error as e:
            print(f"  ✗ Error processing {record['symbol']}: {e}")
            raise

    return inserted_count, updated_count


def verify_data(cursor):
    """
    Verify the inserted data by querying the table.

    Parameters:
    -----------
    cursor : psycopg2.cursor
        Database cursor object
    """
    cursor.execute("SELECT symbol, company_name, currency, annual_revenue, annual_profit FROM org_basic_info ORDER BY symbol")
    rows = cursor.fetchall()

    print("\n" + "="*70)
    print("Verification - Data in org_basic_info table:")
    print("="*70)

    for row in rows:
        print(f"Symbol: {row[0]}")
        print(f"  Company: {row[1]}")
        print(f"  Currency: {row[2]}")
        print(f"  Revenue: {row[3]}")
        print(f"  Profit:  {row[4]}")
        print("-" * 70)


def main():
    """
    Main function to orchestrate database operations.
    """
    print("\n" + "="*70)
    print("Creating Basic Company Information Data")
    print("="*70 + "\n")

    conn = None
    cursor = None

    try:
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create table
        print("\nCreating table...")
        create_table_if_not_exists(cursor)

        # Insert data
        print(f"\nInserting {len(PLACEHOLDER_DATA)} records...")
        inserted, updated = insert_basic_info(cursor, PLACEHOLDER_DATA)

        # Commit transaction
        conn.commit()
        print(f"\n✓ Transaction committed successfully")
        print(f"  - {inserted} new records inserted")
        print(f"  - {updated} existing records updated")

        # Verify data
        verify_data(cursor)

        print("\n" + "="*70)
        print("✓ Script completed successfully!")
        print("="*70 + "\n")

    except Exception as e:
        if conn:
            conn.rollback()
            print(f"\n✗ Transaction rolled back due to error: {e}")
        raise

    finally:
        # Close connections
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
