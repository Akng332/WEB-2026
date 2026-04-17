import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

app.template_folder = 'app/templates'
app.static_folder = 'app/static'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.test_client() as client:
        yield client