import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(page, questions):
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions_formatted = []
  for question in questions:
    questions_formatted.append(question.format())
  return questions_formatted[start:end]


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Origin', '*')
      response.headers.add('Access-Control-Allow-Headers',
                           'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods',
                           'GET,PUT,POST,DELETE,OPTIONS')
      return response

  # Create an endpoint to handle GET requests
  # for all available categories.

  @app.route('/categories')
  def get_categories():
      categories = list(map(Category.format, Category.query.all()))
      result = {"categories": categories}
      return jsonify(result)

  # GET questions with pagination (every 10 questions).
  # This endpoint should return a list of questions,
  # number of total questions, current category, categories.

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions.

  @app.route('/questions')
  def get_questions():
    questions = Question.query.all()
    page = request.args.get('page', 1, type=int)

    current_page_result = paginate_questions(page, questions)
    categories = list(map(Category.format, Category.query.all()))

    return jsonify({
      'questions': current_page_result,
      'total_questions': len(questions),
      'categories': categories,
      'current_category' : "ALL"
    })

  
  # DELETE question using a question ID.
  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page.
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = None
    try:
      question = Question.query.get(question_id)
      question.delete()
      return jsonify({'status': "deleted"})
    except:
      if question == None:
        abort(404)
      else:
        abort(422)


  # Create an endpoint to POST a new question,
  # which will require the question and answer text,
  # category, and difficulty score.

  # TEST: When you submit a question on the "Add" tab,
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.

  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    question = body.get('question')
    answer = body.get('answer')
    category = body.get('category')
    difficulty = body.get('difficulty')
    try:
        entity = Question(question, answer, category, difficulty)
        entity.insert()
        return jsonify({'status': 'question added'})
    except:
        abort(422)

  # POST endpoint to get questions based on a search term.
  # It should return any questions for whom the search term
  # is a substring of the question.

  # TEST: Search by any phrase. The questions list will update to include
  # only question that include that string within their question.
  @app.route("/questions-search", methods=['POST'])
  def search_questions():
    search_phrase = request.json['searchTerm']
    print("search for: " + search_phrase)

    page = 1
    if "page" in request.json:
      page = int(request.json['page'])
    try:     
      matching_questions = Question.query.filter(Question.question.contains(search_phrase))
      current_page_result = paginate_questions(page, matching_questions)
      categories = list(map(Category.format, Category.query.all()))
      return jsonify({
        'questions': current_page_result,
        'total_questions': len(current_page_result),
        'categories': categories,
        'current_category' : "ALL"
      })
    except:
      abort(422)


  # GET endpoint to get questions based on category.
  # TEST: In the "List" tab / main screen, clicking on one of the
  # categories in the left column will cause only questions of that
  # category to be shown.
  @app.route("/categories/<int:category_id>/questions")
  def questions_by_category(category_id):
    category_id = str(category_id)
    current_category = None
    try:     
      current_category = Category.query.get(category_id)
      matching_questions = Question.query.filter(Question.category == category_id)
      current_page_result = paginate_questions(1, matching_questions)
      categories = list(map(Category.format, Category.query.all()))
      return jsonify({
        'questions': current_page_result,
        'total_questions': len(current_page_result),
        'categories': categories,
        'current_category' : Category.format(current_category)
      })
    except:
      if current_category == None:
        abort(404)
      else:
        abort(422)
  #   '''
  # @TODO:
  # Create a POST endpoint to get questions to play the quiz.
  # This endpoint should take category and previous question parameters
  # and return a random questions within the given category,
  # if provided, and that is not one of the previous questions.

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not.
  # '''

  #   '''
  # @TODO:
  # Create error handlers for all expected errors
  # including 404 and 422.
  # '''

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Not found"
      }), 404

  @app.errorhandler(422)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable entity"
      }), 422

  return app
