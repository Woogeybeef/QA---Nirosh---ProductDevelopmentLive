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
        expected_durations = [(datetime(2023, 10, 2) - datetime(2023, 10, 1)).days,
                              (datetime(2023, 10, 6) - datetime(2023, 10, 5)).days,
                              (datetime(2023, 10, 12) - datetime(2023, 10, 10)).days]

        # Call the enrichment function to add loan_duration column
        enriched_df = enrich_date_duration(self.df, 'book returned', 'book checkout')

        # Check if the computed loan_duration matches the expected values
        pd.testing.assert_series_equal(enriched_df['loan_duration'], pd.Series(expected_durations), check_exact=True)

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

        # Ensure that the loan_duration is >= 0 after filtering
        self.assertTrue((enriched_df['loan_duration'] >= 0).all(), "Loan duration should be non-negative after cleaning.")

if __name__ == '__main__':
    unittest.main()