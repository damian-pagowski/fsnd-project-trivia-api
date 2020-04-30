import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{user}:{pw}@{url}/{db}'.format(
            user="postgres", pw="postgres", url='localhost:5432', db="trivia_test")
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(data["categories"]), 6)

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(data["questions"]), 0)

    def test_create_question(self):
        request_body = {
            'question': '2+2',
            'answer': '5',
            'difficulty': 5,
            'category': 6
        }
        res = self.client().post('/questions', json=request_body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["status"], "question added")

    def test_create_question_missing_parameters(self):
        request_body = {
            'question': '2+2',
            'answer': '5',
            'difficulty': 5
        }
        res = self.client().post('/questions', json=request_body)
        self.assertEqual(res.status_code, 422)

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        self.assertEqual(res.status_code, 200)

    def test_delete_question_question_non_existing(self):
        res = self.client().delete('/questions/100')
        self.assertEqual(res.status_code, 404)

    def test_search_questions(self):
        request_body = {'searchTerm': 'Van Gogh'}
        res = self.client().post('/questions-search', json=request_body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(data["questions"]), 1)
        self.assertEqual(data["questions"][0]['id'], 18)

    def test_search_questions_missing_param_searchTerm(self):
        request_body = {}
        res = self.client().post('/questions-search', json=request_body)
        self.assertEqual(res.status_code, 422)

    def test_quizzes(self):
        request_body = {"previous_questions": [
            16, 17, 19], "quiz_category": {"type": "Art", "id": 2}}
        res = self.client().post('/quizzes', json=request_body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question']['id'], 18)
    
    def test_quizzes_invalid_category(self):
        request_body = {"previous_questions": [
            16, 17, 19], "quiz_category": {"type": "Programming", "id": 9}}
        res = self.client().post('/quizzes', json=request_body)
        self.assertEqual(res.status_code, 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
