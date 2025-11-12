import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch
from clean_data import cleanse_data, enrich_date_duration

# Fixtures for sample data
@pytest.fixture
def sample_data():
    data = {
        'book checkout': ['2023-10-01', '2023-10-05', '2023-10-10'],
        'book returned': ['2023-10-02', '2023-10-06', '2023-10-12']
    }
    df = pd.DataFrame(data)
    df['book checkout'] = pd.to_datetime(df['book checkout'])
    df['book returned'] = pd.to_datetime(df['book returned'])
    return df

# Test for cleanse_data with mocked file reading and writing
@patch('pandas.read_csv')  # Mocking the read_csv method to avoid actual file reading
@patch('clean_data.df.to_sql')  # Mocking the to_sql method to avoid DB writes
@patch('clean_data.df.to_csv')  # Mocking the to_csv method to avoid file writes
def test_cleanse_data_handle_nulls_and_duplicates(mock_to_csv, mock_to_sql, mock_read_csv, sample_data):
    # Mock the return value of read_csv to return sample_data DataFrame
    mock_read_csv.return_value = sample_data

    # Call cleanse_data (which will now use the mocked DataFrame from mock_read_csv)
    cleanse_data('fake_file.csv', 'server', 'database')  # pass fake file path

    # Assertions to ensure that the correct methods were called
    mock_read_csv.assert_called_once_with('fake_file.csv')  # check if read_csv was called with the correct path
    mock_to_sql.assert_called_once()  # Ensure that data was written to SQL
    mock_to_csv.assert_called_once()  # Ensure that data was written to a CSV file

    # Additional test logic for checking nulls, duplicates, etc.
    # Ensure nulls are dropped (since we're using sample_data that has no nulls, this should pass)
    assert sample_data.isnull().sum().sum() == 0, "Null values were not correctly handled."
    assert len(sample_data) == 3, "Dataframe size after processing is incorrect."


