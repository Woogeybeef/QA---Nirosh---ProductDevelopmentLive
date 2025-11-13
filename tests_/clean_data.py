import pandas as pd
import argparse
import os
import glob
import time
from sqlalchemy import create_engine, text

# Function to cleanse data and track metrics
def cleanse_data(input_file, engine):
    metrics = {
        'rows_processed': 0,  # Total rows processed
        'rows_removed': 0,    # Rows removed due to null or duplicates
        'rows_modified': 0,   # Rows modified (e.g., lowercased, date converted)
        'processing_time': 0  # Time taken for processing (in seconds)
    }

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = 'Cleaned_Data'  # Directory to save cleaned files
    
    # Ensure the directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, f"{base_name}_cleaned.csv")

    # Track the start time for processing
    start_time = time.time()

    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)
    metrics['rows_processed'] = len(df)  # Track the total rows processed
    
    # Clean column names (stripping spaces and lowercasing)
    df.columns = df.columns.str.strip().str.lower()

    # Track rows before null removal
    original_row_count = len(df)
    
    # Step 1: Check for null values and remove rows
    null_rows = df.isnull().sum()
    df = df.dropna()
    rows_removed = original_row_count - len(df)
    metrics['rows_removed'] += rows_removed  # Track rows removed due to null values

    # Step 2: Check for duplicates and remove them
    original_row_count = len(df)
    df = df.drop_duplicates()
    rows_removed = original_row_count - len(df)
    metrics['rows_removed'] += rows_removed  # Track rows removed due to duplicates

    # Step 3: Modify columns (e.g., lowercase strings, convert dates)
    rows_modified = 0  # Count rows that are modified (e.g., converted to lowercase, etc.)
    
    # Convert 'book checkout' to datetime if present
    if 'book checkout' in df.columns:
        df['book checkout'] = df['book checkout'].str.replace('"', "", regex=True)
        df['book checkout'] = pd.to_datetime(df['book checkout'], errors='coerce')
        rows_modified += df['book checkout'].notna().sum()  # Count rows modified (non-NaT entries)

    # Convert 'book returned' to datetime if present
    if 'book returned' in df.columns:
        df['book returned'] = pd.to_datetime(df['book returned'], errors='coerce')
        rows_modified += df['book returned'].notna().sum()  # Count rows modified (non-NaT entries)
    
    # Example: Convert string columns to lowercase (if applicable)
    if 'string_column' in df.columns:
        df['string_column'] = df['string_column'].str.lower()
        rows_modified += df['string_column'].notna().sum()  # Track rows modified

    metrics['rows_modified'] = rows_modified

    # Step 4: Save the cleaned data to a CSV file
    df.to_csv(output_file, index=False, mode='w')  # Overwrite the file if exists

    # Record the time taken for the process
    processing_time = time.time() - start_time
    metrics['processing_time'] = processing_time  # Track time taken for processing

    # Insert the cleaned data into SQL with the same name as the cleaned CSV file
    insert_data_to_sql(df, base_name, engine)
    
    # Insert the metrics into the SQL table
    insert_metrics_to_sql(metrics, input_file, engine)
    
    print(f"Data cleaning complete for {input_file}.")
    print(f"Rows processed: {metrics['rows_processed']}")
    print(f"Rows removed: {metrics['rows_removed']}")
    print(f"Rows modified: {metrics['rows_modified']}")
    print(f"Processing time (seconds): {metrics['processing_time']}")
    
    return metrics

def insert_data_to_sql(df, base_name, engine):
    """
    Insert the cleaned data into a SQL table with the same name as the cleaned CSV file.
    """
    table_name = base_name + "_cleaned"  # Use the base name for the table name

    # Insert the DataFrame into the SQL table
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

    print(f"Data saved to SQL table: {table_name}")

def insert_metrics_to_sql(metrics, file_name, engine):
    """
    Insert metrics into the SQL table.
    """
    query = """
        INSERT INTO data_cleaning_metrics (file_name, rows_processed, rows_removed, rows_modified, processing_time_seconds)
        VALUES (:file_name, :rows_processed, :rows_removed, :rows_modified, :processing_time_seconds)
    """
    
    # Ensure you are using an open connection to execute the query
    with engine.connect() as connection:
        # Use `text()` to indicate that we're passing raw SQL query with parameters
        connection.execute(text(query), {
            'file_name': file_name,
            'rows_processed': metrics['rows_processed'],
            'rows_removed': metrics['rows_removed'],
            'rows_modified': metrics['rows_modified'],
            'processing_time_seconds': metrics['processing_time']
        })

def main():
    parser = argparse.ArgumentParser(description="Cleanse CSV data and track metrics.")
    parser.add_argument("server_name", help="SQL Server name or IP address")
    parser.add_argument("database_name", help="SQL Server database name")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Create the connection string to the database
    connection_string = f'mssql+pyodbc://{args.server_name}/{args.database_name}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    
    # Create SQLAlchemy engine to interact with the SQL Server
    engine = create_engine(connection_string)

    # Get the list of all CSV files in the current directory
    csv_files = glob.glob("*.csv")

    # Check if any CSV files are found
    if not csv_files:
        print("No CSV files found in the current directory.")
        return

    # Process each CSV file and track metrics
    for input_file in csv_files:
        cleanse_data(input_file, engine)

if __name__ == "__main__":
    main()

