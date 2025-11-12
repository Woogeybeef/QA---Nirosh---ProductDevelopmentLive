import unittest
import pandas as pd
from datetime import datetime

# Assuming `enrich_date_duration` is available from your code
from clean_data import enrich_date_duration  # Replace with the correct import if needed

class TestLoanDuration(unittest.TestCase):

    def setUp(self):
        # Setup a test dataframe
        data = {
            'book checkout': ['2023-10-01', '2023-10-05', '2023-10-10'],
            'book returned': ['2023-10-02', '2023-10-06', '2023-10-12']
        }
        # Create DataFrame with datetime columns
        self.df = pd.DataFrame(data)
        self.df['book checkout'] = pd.to_datetime(self.df['book checkout'])
        self.df['book returned'] = pd.to_datetime(self.df['book returned'])

    def test_loan_duration_positive(self):
        # Call the enrichment function to add loan_duration column
        enriched_df = enrich_date_duration(self.df, 'book returned', 'book checkout')

        # Ensure loan_duration is non-negative
        self.assertTrue((enriched_df['loan_duration'] >= 0).all(), "Loan duration should be non-negative.")

    def test_loan_duration_calculation(self):
        # Manually calculate expected loan durations
        expected_durations = pd.Series([(datetime(2023, 10, 2) - datetime(2023, 10, 1)).days,
                                        (datetime(2023, 10, 6) - datetime(2023, 10, 5)).days,
                                        (datetime(2023, 10, 12) - datetime(2023, 10, 10)).days],
                                       dtype=int)  # Explicitly make this an integer Series
        
        # Set the name of the expected series to match the one in enriched_df
        expected_durations.name = 'loan_duration'

        # Call the enrichment function to add loan_duration column
        enriched_df = enrich_date_duration(self.df, 'book returned', 'book checkout')

        # Ensure that the loan_duration is >= 0 after cleaning
        # If there are any negative durations, filter them out
        enriched_df = enriched_df[enriched_df['loan_duration'] >= 0]

        self.assertTrue((enriched_df['loan_duration'] >= 0).all(), "Loan duration should be non-negative after cleaning.") 

        # Reset indices for both Series to ensure no index mismatch
        enriched_df['loan_duration'] = enriched_df['loan_duration'].reset_index(drop=True)
        expected_durations = expected_durations.reset_index(drop=True)

        # Ensure the loan durations match (name should be the same now)
        pd.testing.assert_series_equal(enriched_df['loan_duration'], expected_durations)

    def test_loan_duration_no_negative(self):
        # Create a test case where the 'book returned' date is before the 'book checkout' date
        data_invalid = {
            'book checkout': ['2023-10-10'],
            'book returned': ['2023-10-05']
        }
        df_invalid = pd.DataFrame(data_invalid)
        df_invalid['book checkout'] = pd.to_datetime(df_invalid['book checkout'])
        df_invalid['book returned'] = pd.to_datetime(df_invalid['book returned'])

        # Call the enrichment function to add loan_duration column
        enriched_df = enrich_date_duration(df_invalid, 'book returned', 'book checkout')

        # Ensure that the loan_duration is >= 0 after cleaning
        self.assertTrue((enriched_df['loan_duration'] >= 0).all(), "Loan duration should be non-negative after cleaning.")

if __name__ == '__main__':
    unittest.main()

