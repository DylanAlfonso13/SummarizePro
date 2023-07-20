import unittest
import sys
from app import app
sys.path.append('../SummarizePro')


class TestFile(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_pdf_route(self):
        response = app.test_client().get('/pdf')
        self.assertEqual(response.status_code, 200)

    def test_article_route(self):
        response = app.test_client().get('/article')
        self.assertEqual(response.status_code, 200)

    def test_fake_route(self):
        response = app.test_client().get('/;aldkfj')
        self.assertNotEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
