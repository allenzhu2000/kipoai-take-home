"""
Tests for the search blueprint.
"""
from flask.testing import FlaskClient
from bs4 import BeautifulSoup

def test_substitute_post(test_client: FlaskClient):
    """"
    When the '/substitute/' page is posted to, check that response is correct. 
    """
    response = test_client.post('/substitute/',
        data={'query': "MIL-DTL-28840 size 19 straight male plug"}
    )
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    table_body = soup.find('tbody')
    num_rows = len(table_body.find_all('tr'))
    assert num_rows == 10
