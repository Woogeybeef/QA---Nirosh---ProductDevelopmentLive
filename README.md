# Data Cleansing and Metrics Tracking Script

This Python script cleanses CSV data files by performing the following operations:
- Removing rows with null values
- Removing duplicate rows
- Modifying columns (e.g., converting dates to a consistent format, lowercasing string columns)
- Tracking various metrics related to the data cleansing process

The script also inserts both the cleaned data and metrics into a SQL Server database for easy monitoring and reporting. The metrics include:
- Number of rows processed
- Number of rows removed due to null values or duplicates
- Number of rows modified
- Time taken to process each file

## Workflow Overview

### 1. **Input**:
   - The script processes CSV files located in the same directory.
   - Each CSV file is loaded into a Pandas DataFrame for cleansing.

### 2. **Data Cleansing**:
   - **Column Name Standardization**: Strips any leading/trailing spaces and converts all column names to lowercase.
   - **Null Handling**: Removes rows containing any null (NaN) values.
   - **Duplicate Removal**: Identifies and removes duplicate rows.
   - **Column Modification**:
     - Converts specific columns (e.g., `book checkout` and `book returned`) to datetime format.
     - Converts string columns to lowercase (e.g., `string_column`).

### 3. **Metrics Tracking**:
   - The script tracks and stores metrics such as:
     - `rows_processed`: Total rows in the original data file.
     - `rows_removed`: Rows removed due to null values or duplicates.
     - `rows_modified`: Rows that had values modified (e.g., converted to lowercase, dates corrected).
     - `processing_time`: Time taken to process each CSV file.

### 4. **SQL Database Integration**:
   - The cleaned data is saved into a SQL Server database.
   - Metrics are inserted into a `data_cleaning_metrics` table in the SQL database, which allows for easy reporting and monitoring of the data cleaning process.

### 5. **Power BI Integration**:
   - Power BI can be connected to the `data_cleaning_metrics` table in the SQL Server database to visualize the metrics and track data processing trends over time.

## Setup Instructions

### Requirements:
- Python 3.x
- Required Python libraries:
  - `pandas`
  - `numpy`
  - `sqlalchemy`
  - `pyodbc`
  - `pip install pandas numpy sqlalchemy pyodbc`
- A running SQL Server database with the following table structure for metrics:
  
  
  ```sql
  CREATE TABLE data_cleaning_metrics (
      file_name VARCHAR(255),
      rows_processed INT,
      rows_removed INT,
      rows_modified INT,
      processing_time_seconds FLOAT
  );
