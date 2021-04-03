import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# VERY IMPORTANT:
## 1) PLEASE MAKE SURE TO ADJUST THE DATABASE URI BECAUSE I HAD TO CHANGE IT TO MAKE IT WORK ON MY PC

def paginate(request, questions_list):
  """to structure the questions in multiple pages"""
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  formatted_questions = [ question.format() for question in questions_list]
  questions_in_page = formatted_questions[start: end]
  return questions_in_page


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r'/*': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=["GET"])
  def get_categories():

    categories_list = Category.query.order_by(Category.id).all()

    # in case no categories exist in the database
    if len(categories_list) == 0:
      abort(404)
    # format the categories in 2 steps to obtain a dictionary with {id: type} format
    list_formatted_categories = [category.format() for category in categories_list]
    dict_formatted_categories = {category['id']: category['type']for category in list_formatted_categories}
    return jsonify({
      "success": True,
      "categories": dict_formatted_categories
    })





  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route("/questions", methods=['GET'])
  def get_all_questions():

    # get all the questions ordered from the database and paginate them
    db_questions = Question.query.order_by(Question.id).all()

    questions_to_show = paginate(request, db_questions)

    # in case no questions exist in the database or in the requested page
    if len(questions_to_show) == 0:
      abort(404)


    # get all the categories ordered from the database and format them in { id: type } format
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [category.format() for category in categories]
    dict_formatted_categories = {category['id']: category['type']for category in formatted_categories}

    return jsonify({
      "success": True,
      "questions": questions_to_show,
      "total_questions": len(db_questions),
      "categories": dict_formatted_categories,
      "current_category": "1"
    })



  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    # NOTE: if the users enters a bad format for the question_id ( like a string for example ) the following line will
    # raise a 404 error
    question_to_delete = Question.query.filter(Question.id == question_id).one_or_none()

    # in case the id entered by the user doesn't belong to any question
    if question_to_delete is None:
      abort(422)
    question_to_delete.delete()
    number_of_questions = len(Question.query.all())
    return jsonify({
      'success': True,
      'number_of_questions': number_of_questions
    })






  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  # to simplify the function of the route /questions which will have both functionalities of search and add question
  # i will use 2 functions and then include them with if statements in the route function
  def search(search_term):
    all_questions = Question.query.all()
    questions_found = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    questions_to_show = paginate(request, questions_found)

    # in case no question matches the search term or the page number desired is too big
    if len(questions_found) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'questions': questions_to_show,
      'total_questions': len(all_questions),
      'current_category': "1"
    })

  def add(request_body, question, answer, difficulty, category):

    # in case the user doesn't provide all the necessary fields
    if question is None or answer is None or difficulty is None or category is None:
      abort(400)

    new_question = Question(question, answer, category, difficulty)
    new_question.insert()
    number_of_questions = len(Question.query.all())

    return jsonify({
      'success': True,
      'number_of_questions': number_of_questions
    })

  @app.route('/questions', methods=['POST'])
  def add_or_search_question():
    request_body = request.get_json()
    if request_body is None:
      abort(400)
    search_term = request_body.get('searchTerm', None)
    question = request_body.get('question', None)
    answer = request_body.get('answer', None)
    difficulty = request_body.get('difficulty', None)
    category = request_body.get('category', None)

    if search_term is None:
      return add(request_body, question, answer, difficulty, category)
    else:
      return search(search_term)



  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''



  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route("/categories/<int:category_id>/questions", methods=['GET'])
  def get_questions_by_category(category_id):
    category = Category.query.filter(Category.id == category_id).one_or_none()

    #in case the user enters a category id that doesn't exist
    if category is None:
      abort(422)

    category_type = category.format()['type']
    db_questions = Question.query.order_by(Question.id).filter(Question.category == str(category_id)).all()
    questions_to_show = paginate(request, db_questions)

    # in case no question matches the desired category
    if len(questions_to_show) == 0:
      abort(404)
    return jsonify({
      "success": True,
      "questions": questions_to_show,
      "category": category_type
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_the_game():
    request_body = request.get_json()
    # if the user doesnt give a request
    if request_body is None:
      abort(400)

    quiz_category = request_body.get('quiz_category', None)
    previous_questions = request_body.get('previous_questions', None)

    # in case the user doesn't give a quiz_category or a previous questions list
    if quiz_category is None or previous_questions is None:
      abort(400)

    if quiz_category['id'] != 0:
      questions = Question.query.filter(Question.category == quiz_category['id']).all()
    else:
      questions = Question.query.all()

    # in case no questions are in the category or no question exist altogether in the database
    if len(questions) == 0:
      abort(404)

    # in case the questions of a category are less than 5
    if len(questions) == len(previous_questions):
      return jsonify({
        "success": True,
        "state": "end_of_game"
      })
    random_question = random.choice(questions).format()
    while random_question['id'] in previous_questions:
      random_question = random.choice(questions).format()

    return jsonify({
      "success": True,
      "question": random_question
    })




  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unproccesable_entity(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable entity"
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "internal server error"
    }),500

  return app

    