import pandas as pd
import argparse

# Function to cleanse data
def cleanse_data(input_file, output_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Step 1: Check for null values
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
    # Example 1: Ensure a date column is in a consistent format
    if 'date_column' in df.columns:
        df['date_column'] = pd.to_datetime(df['date_column'], errors='coerce')

    # Example 2: Convert string columns to lowercase (or uppercase)
    if 'string_column' in df.columns:
        df['string_column'] = df['string_column'].str.lower()

    # Example 3: Ensure numeric columns are in the correct format
    if 'numeric_column' in df.columns:
        df['numeric_column'] = pd.to_numeric(df['numeric_column'], errors='coerce')

    # Step 4: Save the cleaned data to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"\nData cleaning complete. Cleaned file saved as '{output_file}'.")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Cleanse CSV data by removing null values, duplicates, and ensuring consistent formats.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to save the cleaned CSV file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the cleanse_data function with the provided file names
    cleanse_data(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
