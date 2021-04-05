import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

# VERY IMPORTANT:
## 1) PLEASE MAKE SURE TO ADJUST THE DATABASE URI BECAUSE I HAD TO CHANGE IT TO MAKE IT WORK ON MY PC

## 2) PLEASE MAKE SURE TO RESET THE DATABASE SO ALL THE TESTS WILL FUNCTION

## 3) PLEASE MAKE SURE TO CHECK THE ID OF THE QUESTION TO DELETE IN THE TEST OF THE DELETE FUNCTIONALITY TO AVOID
## ANY KIND OF PROBLEM

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'trivia_test')
DB_PATH = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME
        self.database_path = DB_PATH
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # ================================================================================
    # tests for getting all the categories
    # ================================================================================

    def test_get_categories(self):
        """test if the /categories endpoint functions correctly with the GET method"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # ================================================================================
    # tests for getting all the questions
    # ================================================================================
    def test_get_all_questions(self):
        """test if the /questions endpoint functions correctly with the GET method"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_error_404_if_no_questions_found_in_page(self):
        """test if the 404 error functions correctly with the GET method in /questions endpoint
         if the page number is too big"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # ================================================================================
    # tests for getting the questions by category
    # ================================================================================
    def test_get_questions_by_category(self):
        """test the method GET for the endpoint /categories/<id/>questions
         to retrieve all the questions of a desired category"""
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_error_422_id_not_exist(self):
        """test the error 422 for the method GET for the endpoint /categories/<id/>questions
         if category_id doesn't exist"""
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable entity")

    def test_error_404_no_questions_found(self):
        """test the error 404 for the method GET for the endpoint /categories/<id/>questions
         if category_id doesn't exist"""
        res = self.client().get('/categories/1/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_error_404_bad_id(self):
        """test the error 404 for the method GET for the endpoint /categories/<id/>questions
        if category_id is in wrong format"""
        res = self.client().get('/categories/a/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # ================================================================================
    # tests for deleting the questions
    # ================================================================================
    def test_delete_questions(self):
        """test the method DELETE for the endpoint /questions/<id> to delete a question"""
        id_to_delete = Question.query.first().id

        res = self.client().delete(f'/questions/{id_to_delete}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_422_question_id_not_exist(self):
        """test the error 422 for the method DELETE for the endpoint /questions/<id> if the id doesn't exist"""
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable entity")

    def test_error_404_question_id_bad_format(self):
        """test the error 422 for the method DELETE for the endpoint /questions/<id> if the id is in a bad format"""
        res = self.client().delete('/questions/a')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # ================================================================================
    # tests for searching the questions
    # ================================================================================
    def test_search_questions(self):
        """test the method POST for the endpoint /questions to search a question"""
        res = self.client().post('/questions', json={
            "searchTerm": "world"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_error_404_search_term_not_exist(self):
        """test the error 404 for the method POST for the endpoint /questions if the search word doesn't exist"""
        res = self.client().post('/questions', json={
            "searchTerm": "madrid"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_error_400_bad_request_format(self):
        """test the error 400 for the method POST for the endpoint /questions if the request is empty"""
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    # ================================================================================
    # tests for adding the questions
    # ================================================================================
    def test_add_question(self):
        """test the method POST for the endpoint /questions to add a question"""
        res = self.client().post('/questions', json={
            "question": "who's won the world cup 2014?",
            "answer": "Germany",
            "difficulty": 1,
            "category": "3"
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # to avoid adding more than 5 questions to category sport because we want to keep it at 3 quetsions to test
        # the quiz functionality
        Question.query.filter(Question.answer == "Germany").delete()


    def test_error_400_bad_request(self):
        """test the error 404 for the method POST for the endpoint /questions if one of the question informations
        is not entered """
        res = self.client().post('/questions', json={
            "question": "who's won the world cup 2014?",
            "answer": "Germany",
            "difficulty": 1,
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    # ================================================================================
    # tests for adding the questions
    # ================================================================================
    def test_play_game(self):
        """test the method POST for the endpoint /quizzes to play"""
        res = self.client().post('/quizzes', json={
            "quiz_category": {'id': 1},
            "previous_questions": []
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_game_less_than_5_questions(self):
        """test the method POST for the endpoint /quizzes if all the questions are less than 5 and are already asked """
        res = self.client().post('/quizzes', json={
            "quiz_category": {'id': 4},
            "previous_questions": [5, 9, 23]
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['state'], "end_of_game")

    def test_error_400_bad_request_play_game(self):
        """test the error 404 for the method POST for the endpoint /quizzes if one of the informations
        is not entered """
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()