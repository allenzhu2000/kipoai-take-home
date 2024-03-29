from dotenv import load_dotenv
load_dotenv()

import pytest
from app import create_app

# Fixtures
@pytest.fixture(scope='module')
def test_client():
    
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


