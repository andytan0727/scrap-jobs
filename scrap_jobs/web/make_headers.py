"""
This module contains method to produce HTTP headers which are able to
circumvent website's block by faking a real human user
"""
import random

from fake_useragent import UserAgent


def make_headers():
    """Function to make headers to be used in HTTP request
    """
    accepts = {
        'Firefox': 'text/html,'
                   'application/xhtml+xml,'
                   'application/xml;q=0.9,*/*;q=0.8',

        'Safari, Chrome': 'application/xml,'
                          'application/xhtml+xml,'
                          'text/html;q=0.9,'
                          'text/plain;q=0.8,'
                          'image/png,*/*;q=0.5'
    }

    # randomly generate a User-Agent header
    # to fake a human user
    ua = UserAgent()
    if random.random() > 0.5:
        random_user_agent = ua.chrome
    else:
        random_user_agent = ua.firefox

    valid_accept = accepts['Firefox'] if random_user_agent.find(
        'Firefox') > 0 else accepts['Safari, Chrome']

    headers = {
        "User-Agent": random_user_agent,
        "Accept": valid_accept
    }

    return headers
