from google.cloud import bigquery
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize BigQuery client
    client = bigquery.Client()
    
    # Example 1: Create a simple table
    project_id = os.getenv('GCP_PROJECT_ID')
    dataset_id = os.getenv('GCP_DATASET_ID')
    table_id = f"{project_id}.{dataset_id}.user_data"
    
    # Define schema
    schema = [
        bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("email", "STRING"),
        bigquery.SchemaField("created_at", "TIMESTAMP")
    ]
    
    # Create table
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table, exists_ok=True)
    print(f"Created table {table_id}")
    
    # Example 2: Insert data
    rows_to_insert = [
        {
            "user_id": "user1",
            "name": "John Doe",
            "email": "john@example.com",
            "created_at": "2024-01-01 12:00:00"
        },
        {
            "user_id": "user2",
            "name": "Jane Smith",
            "email": "jane@example.com",
            "created_at": "2024-01-02 13:00:00"
        }
    ]
    
    errors = client.insert_rows_json(table, rows_to_insert)
    if not errors:
        print("Data inserted successfully")
    else:
        print(f"Errors: {errors}")
    
    # Example 3: Query data
    query = f"""
        SELECT name, email
        FROM `{table_id}`
        WHERE created_at > TIMESTAMP('2024-01-01')
        ORDER BY created_at DESC
    """
    
    query_job = client.query(query)
    results = query_job.result()
    
    print("\nQuery Results:")
    for row in results:
        print(f"Name: {row.name}, Email: {row.email}")

if __name__ == "__main__":
    main() 