import unittest
from app import app

def test_index_route():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_pdf_route():
    response = app.test_client().get('/pdf')
    assert response.status_code == 200
def test_article_route():
    response = app.test_client().get('/article')
    assert response.status_code == 200

def test_summaries_route():
    response = app.test_client().get('/summaries')
    assert response.status_code == 200
