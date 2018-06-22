import re

_whole_word = lambda x: re.compile(r'(?<=\W)' + x + '(?=\W)')
_mixed_ordinal_pat = _whole_word(r'-?\d+(st|th|nd|rd)')
# _integer_pat = _whole_word(r'\d+')
_integer_pat = _whole_word(r'\d+[\d,]+')
_floating_point_after_pat = re.compile(r'\.\d+[^a-zA-Z.]')
_floating_point_before_pat = re.compile(r'(?<=\d\.)')
# _date_with_month_abbrev_pat = _whole_word(r'\d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),? \d{4}')
_date_with_month_abbrev_pat = _whole_word(r'\d{2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),? \d{4}')
# _date_iso8601_pat = _whole_word(r'\d{4}-\d{2}-\d{2}')
# _date_iso8601_pat = re.compile(r'2018-06-22 18:22:19.123')
# _date_iso8601_pat = re.compile(r'(\d{4}-(0\d|1[012])-(0[1-9]|[12][0-9]|3[01]))(( |T)(\d+:)+([\d.]+)?)?')
# _date_iso8601_pat = re.compile(r'(\d{4}-(0\d|1[012])-(0[1-9]|[12][0-9]|3[01]))(( |T)(\d+:)+([\d.]+)?)?(([-|+])|( [A-Z]{1,3}))?')
# _date_iso8601_pat = re.compile(r'(\d{4}-(0\d|1[012])-(0[1-9]|[12][0-9]|3[01]))(( |T)(\d+:)+([\d.]+)?)?(\+0100|( [A-Z]{1,3}))?')
# _date_iso8601_pat = re.compile(r'(\d{4}-(0\d|1[012])-(0[1-9]|[12][0-9]|3[01]))(( |T)(\d+:)+([\d.]+)?)?(\+\d+|( [A-Z]{1,3}))?')
_date_iso8601_pat = re.compile(r'(\d{4}-(0\d|1[012])-(0[1-9]|[12][0-9]|3[01]))(( |T)(\d+:)+([\d.]+)?)?([\+|-]\d+|( [A-Z]{1,3}))?')
# _date_iso8601_pat = re.compile(r'(\d{4}-(0\d|1[012])-(0[1-9]|[12][0-9]|3[01]))(( |T)(\d+:)+([\d.]+)?)?')


def dates_iso8601(text):
    ##  When you're matching ISO 8601 dates, you should also handle dates
    ##  with timestamps, like "2018-06-22 18:22:19.123". These dates might
    ##  end with a time precision of minutes, or of seconds, or of milliseconds.
    ##  The delimiter between the date and the time portion could be either
    ##  a space or 'T'. And there might be a timezone specifier on the end--
    ##  either a 3-letter abbreviation like "MDT" or the single letter "Z"
    ##  (for "Zulu" or UTC), or an offset like "-0800".
    '''Find tokens that begin with a number, and then have an ending like 1st or 2nd.'''
    for match in _date_iso8601_pat.finditer(text):
        yield('date month', match)

def dates_month_abbrev(text):
    '''Find tokens that begin with a number, and then have an ending like 1st or 2nd.'''
    for match in _date_with_month_abbrev_pat.finditer(text):
        yield('date', match)

def mixed_ordinals(text):
    '''Find tokens that begin with a number, and then have an ending like 1st or 2nd.'''
    for match in _mixed_ordinal_pat.finditer(text):
        yield('ordinal', match)

def integers(text):
    '''Find integers in text. Don't count floating point numbers.'''
    for match in _integer_pat.finditer(text):
        # If the integer we're looking at is part of a floating-point number, skip it.
        if _floating_point_before_pat.match(text, match.start()) or \
                _floating_point_after_pat.match(text, match.end()):
            continue
        yield ('integer', match)

def scan(text, *extractors):
    '''
    Scan text using the specified extractors. Return all hits, where each hit is a
    tuple where the first item is a string describing the extracted number, and the
    second item is the regex match where the extracted text was found.
    '''
    for extractor in extractors:
        for item in extractor(text):
            yield item
