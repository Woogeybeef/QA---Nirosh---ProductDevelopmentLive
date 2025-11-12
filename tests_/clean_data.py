import pandas as pd
import argparse
from sqlalchemy import create_engine
import os
import glob

# Function to cleanse data
def cleanse_data(input_file, server_name, database_name):
    # Extract base file name without extension for output file and SQL table name
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = 'Cleaned_Data'  # The directory to save cleaned files

    # Ensure the directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the directory if it doesn't exist

    output_file = os.path.join(output_dir, f"{base_name}_cleaned.csv")  # Save in the Cleaned_Data folder
    table_name = f"{base_name}_cleaned"

    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Clean column names by stripping leading/trailing spaces and converting to lowercase
    df.columns = df.columns.str.strip().str.lower()

    # Print out the columns to debug if the expected columns exist
    print(f"\nColumns in {input_file}:")
    print(df.columns.tolist())

    # Step 1: Check for null values
    print(f"\nProcessing file: {input_file}")
    print("Null values summary:")
    print(df.isnull().sum())  # Show the number of null values per column

    # Optionally: Handle null values
    # Option 1: Drop rows with null values
    df = df.dropna()

    # Option 2: Fill null values with a specific value (e.g., 'N/A' for strings, 0 for numbers)
    # df = df.fillna({'column_name': 'N/A', 'numeric_column': 0})

    # Step 2: Check for duplicates
    print("\nDuplicate rows summary:")
    print(df.duplicated().sum())  # Show the number of duplicate rows

    # Option: Drop duplicate rows
    df = df.drop_duplicates()

    # Step 3: Ensure consistent data formats
    # Convert the 'book checkout' column to datetime format if it exists
    if 'book checkout' in df.columns:
        print("\nProcessing 'book checkout' column.")
        df['book checkout'] = df['book checkout'].str.replace('"', "", regex=True)  # Remove any quotes
        df['book checkout'] = pd.to_datetime(df['book checkout'], errors='coerce')  # Convert to datetime, coerce errors to NaT
    else:
        print("Column 'book checkout' not found in the dataset. Skipping datetime conversion.")

    # Convert the 'book returned' column to datetime format if it exists
    if 'book returned' in df.columns:
        print("\nProcessing 'book returned' column.")
        df['book returned'] = pd.to_datetime(df['book returned'], errors='coerce')  # Same for the 'book returned' column
    else:
        print("Column 'book returned' not found in the dataset. Skipping datetime conversion.")

    # Drop rows where 'book checkout' or 'book returned' are NaT (invalid dates)
    if 'book checkout' in df.columns:
        df = df.dropna(subset=['book checkout'])

    if 'book returned' in df.columns:
        df = df.dropna(subset=['book returned'])

    # Example 2: Convert string columns to lowercase (if applicable)
    if 'string_column' in df.columns:
        df['string_column'] = df['string_column'].str.lower()
    else:
        print("Column 'string_column' not found in the dataset. Skipping lowercase conversion.")

    # Example 3: Ensure numeric columns are in the correct format
    if 'numeric_column' in df.columns:
        df['numeric_column'] = pd.to_numeric(df['numeric_column'], errors='coerce')
    else:
        print("Column 'numeric_column' not found in the dataset. Skipping numeric conversion.")

    # Enriching data by adding the time a book was on loan (duration between checkout and return)
    # Make sure the columns for the date calculations exist
    if 'book checkout' in df.columns and 'book returned' in df.columns:
        df = enrich_date_duration(df, 'book returned', 'book checkout')
        # Ensure that loan_duration is non-negative
        df = df[df['loan_duration'] >= 0]  # Filter out negative durations
    else:
        print("One or both of the date columns ('book checkout', 'book returned') are missing. Skipping enrichment.")

    # Drop rows where loan_duration is less than 0
    #if 'book checkout' in df.columns and 'book returned' in df.columns:
    #    df = df[df['loan_duration'] >= 0]

    # Define the connection string to your MS SQL Server
    server = server_name  
    database = database_name

    # Create the connection string with Windows Authentication
    connection_string = f'mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

    # Create SQLAlchemy engine
    engine = create_engine(connection_string)

    # Step 4: Write the cleaned data to the SQL Server database (overwrite if the table exists)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

    # Save the cleaned data to a CSV file (overwrite if the file exists)
    df.to_csv(output_file, index=False, mode='w')  # 'mode=w' explicitly overwrites

    print(f"\nData cleaning complete for {input_file}. Data saved to table '{table_name}' in SQL database.")
    print(f"Cleaned data saved to file: {output_file}")

def enrich_date_duration(df, colA, colB):
    """
    Takes the two input date columns and calculates the difference in days between them.
    The result is added as a new column 'date_delta'.
    
    colA should be the later of the two date columns (e.g., 'book returned').
    """
    if colA in df.columns and colB in df.columns:
        # Calculate loan duration in days
        df['loan_duration'] = (df[colA] - df[colB]).dt.days

        # Ensure loan duration is non-negative, replace negative durations with NaN or 0
        df['loan_duration'] = df['loan_duration'].apply(lambda x: max(x, 0))  # Replace negative durations with 0
    return df

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Cleanse CSV data by removing null values, duplicates, and ensuring consistent formats.")
    parser.add_argument("server_name", help="SQL Server name or IP address")
    parser.add_argument("database_name", help="SQL Server database name")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the list of all CSV files in the current directory
    csv_files = glob.glob("*.csv")

    # Check if any CSV files are found
    if not csv_files:
        print("No CSV files found in the current directory.")
        return

    # Process each CSV file in the current directory
    for input_file in csv_files:
        cleanse_data(input_file, args.server_name, args.database_name)

if __name__ == "__main__":
    main()


