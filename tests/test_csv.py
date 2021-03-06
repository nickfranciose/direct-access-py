"""
test_csv.py

Test writing query results to CSV
"""

import os
import csv
import logging
from tempfile import mkdtemp

from directaccess import DirectAccessV2


DIRECTACCESS_API_KEY = os.environ.get('DIRECTACCESS_API_KEY')
DIRECTACCESS_CLIENT_ID = os.environ.get('DIRECTACCESS_CLIENT_ID')
DIRECTACCESS_CLIENT_SECRET = os.environ.get('DIRECTACCESS_CLIENT_SECRET')

if not os.environ.get('DIRECTACCESS_ACCESS_TOKEN'):
    access_token = DirectAccessV2(
        api_key=DIRECTACCESS_API_KEY,
        client_id=DIRECTACCESS_CLIENT_ID,
        client_secret=DIRECTACCESS_CLIENT_SECRET,
    ).access_token
    os.environ['DIRECTACCESS_ACCESS_TOKEN'] = access_token
DIRECTACCESS_ACCESS_TOKEN = os.environ.get('DIRECTACCESS_ACCESS_TOKEN')

LOG_LEVEL = logging.DEBUG
if os.environ.get('CIRCLE_JOB'):
    LOG_LEVEL = logging.ERROR


def test_csv():
    """
    Write Direct Access query results to CSV

    :return:
    """
    tempdir = mkdtemp()
    path = os.path.join(tempdir, 'rigs.csv')
    d2 = DirectAccessV2(
        api_key=DIRECTACCESS_API_KEY,
        client_id=DIRECTACCESS_CLIENT_ID,
        client_secret=DIRECTACCESS_CLIENT_SECRET,
        retries=5,
        backoff_factor=10,
        log_level=LOG_LEVEL,
        access_token=DIRECTACCESS_ACCESS_TOKEN
    )

    dataset = 'rigs'
    options = dict(
        pagesize=10000,
        deleteddate='null'
    )
    count = d2.count(dataset, **options)
    query = d2.query(dataset, **options)
    d2.to_csv(query, path=path, log_progress=True, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    with open(path, mode='r') as f:
        reader = csv.reader(f)
        row_count = len([x for x in reader])
        assert row_count == (count + 1)


if __name__ == '__main__':
    test_csv()
