import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEqual(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Second unit test; prove we find integers with commas
    def test_integers_with_commas(self):
        integers_with_commas = 'how many balloons? 111,222,333 ballons! How many ice creams? 1,234.'
        self.assert_extract(integers_with_commas, library.integers, '111,222,333', '1,234')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)


    # unit test; prove that invalid months are ignored
    def test_ignore_invalid_months_and_days(self):
        invalid_month_str = 'Being from mars, I was born on 2015-89-54.'
        self.assert_extract(invalid_month_str, library.dates_iso8601)

    # unit test; find dates format DD mmm YYYY
    def test_simple_date_format(self):
        valid_date_str = 'Other date format 22 Jun 2018.'
        self.assert_extract(valid_date_str, library.dates_month_abbrev, '22 Jun 2018')

    # unit test; find dates format DD mmm YYYY
    def test_simple_date_format_with_comma(self):
        date='22 Jun, 2018'
        valid_date_str = 'Other date format: ' + date + ' found here.'
        self.assert_extract(valid_date_str, library.dates_month_abbrev, date)

    # unit test; prove that we find iso dates in the form YYYY-MM-DD
    def test_iso_01(self):
        simple_str = 'I was born on 2015-07-25.'
        ## self.assert_extract(simple_str, r'\d\d\d\d-\d\d-\d\d', '2015-07-25')
        self.assert_extract(simple_str, library.dates_iso8601, '2015-07-25')

    # unit test; prove that we find iso dates in the form YYYY-MM-DD dd:dd:dd.ddd
    def test_iso_02(self):
        iso_date='2018-06-22 18:22:19.123'
        test='Here is the date ' + iso_date + ' right here.'
        self.assert_extract(test, library.dates_iso8601, iso_date)

    # unit test; prove that we find iso dates in the form YYYY-MM-DDTdd:dd:dd.ddd (with T)
    def test_iso_03(self):
        iso_date='2018-06-22T18:22:19.123'
        test='Here is the date ' + iso_date + ' right here.'
        self.assert_extract(test, library.dates_iso8601, iso_date)

    # unit test; prove that we find iso dates in the form YYYY-MM-DDTdd:dd (minutes)
    def test_iso_04(self):
        iso_date='2018-06-22T18:22'
        test='Here is the date ' + iso_date + ' right here.'
        self.assert_extract(test, library.dates_iso8601, iso_date)

    # unit test; prove that we find iso dates in the form YYYY-MM-DDTdd:dd:dd (seconds)
    def test_iso_05(self):
        iso_date='2018-06-22T18:22:19'
        test='Here is the date ' + iso_date + ' right here.'
        self.assert_extract(test, library.dates_iso8601, iso_date)

    # unit test; prove that we find iso dates in the form YYYY-MM-DDTdd:dd:dd (milliseconds)
    def test_iso_06(self):
        iso_date='2018-06-22T18:22:19'
        test='Here is the date ' + iso_date + ' right here.'
        self.assert_extract(test, library.dates_iso8601, iso_date)

    # unit test; prove that we find iso dates in the form YYYY-MM-DDTdd:dd:dd MDT
    def test_iso_06(self):
        iso_date='2018-06-22T18:22:19 MDT'
        test='Here is the date ' + iso_date + ' right here.'
        self.assert_extract(test, library.dates_iso8601, iso_date)

    # unit test; prove that we find iso dates in the form YYYY-MM-DDTdd:dd:dd+0100
    def test_iso_07(self):
        iso_date='2018-06-22T18:22:19+0100'
        test='Here is the date ' + iso_date + ' right here.'
        self.assert_extract(test, library.dates_iso8601, iso_date)

    # unit test; prove that we find iso dates in the form YYYY-MM-DDTdd:dd:dd-0800
    def test_iso_08(self):
        iso_date='2018-06-22T18:22:19-0800'
        test='Here is the date ' + iso_date + ' right here.'
        self.assert_extract(test, library.dates_iso8601, iso_date)

if __name__ == '__main__':
    unittest.main()
