#!/usr/bin/env python3
"""
Script to generate fake user data and insert into MySQL database using Faker library.
"""

import mysql.connector
from faker import Faker
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gcp_demo'
}

def generate_fake_users(count=50):
    """Generate fake user data using Faker library."""
    fake = Faker()
    users = []
    
    print(f"\n{'='*60}")
    print(f"Generating {count} fake users...")
    print(f"{'='*60}\n")
    
    for i in range(count):
        user = {
            'name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.address().replace('\n', ', '),
            'city': fake.city(),
            'country': fake.country()
        }
        users.append(user)
        
        if (i + 1) % 10 == 0:
            print(f"✓ Generated {i + 1}/{count} users")
    
    return users

def insert_users_to_db(users):
    """Insert generated users into MySQL database."""
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print(f"\n{'='*60}")
        print("Inserting data into database...")
        print(f"{'='*60}\n")
        
        insert_query = """
        INSERT INTO users (name, email, phone, address, city, country)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Insert all users
        for i, user in enumerate(users):
            cursor.execute(insert_query, (
                user['name'],
                user['email'],
                user['phone'],
                user['address'],
                user['city'],
                user['country']
            ))
            
            if (i + 1) % 10 == 0:
                print(f"✓ Inserted {i + 1}/{len(users)} users")
        
        conn.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ Successfully inserted {len(users)} users!")
        print(f"{'='*60}\n")
        
        # Display inserted data
        cursor.execute("SELECT * FROM users LIMIT 5;")
        rows = cursor.fetchall()
        
        print("Sample inserted records:\n")
        print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'City':<15}")
        print("-" * 70)
        
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<30} {row[5]:<15}")
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM users;")
        total_count = cursor.fetchone()[0]
        print(f"\nTotal users in database: {total_count}\n")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")
        sys.exit(1)

def main():
    """Main function."""
    try:
        # Generate fake data
        fake_users = generate_fake_users(count=50)
        
        # Insert into database
        insert_users_to_db(fake_users)
        
        print("✅ Task completed successfully!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
