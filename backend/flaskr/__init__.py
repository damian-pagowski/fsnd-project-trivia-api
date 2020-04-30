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

  # set Access-Control-Allow
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Origin', '*')
      response.headers.add('Access-Control-Allow-Headers',
                           'Content-Type,Authorization')
      response.headers.add('Access-Control-Allow-Methods',
                           'GET,PUT,POST,DELETE,OPTIONS')
      return response

  # GET all available categories.
  @app.route('/categories')
  def get_categories():
      categories = list(map(Category.format, Category.query.all()))
      result = {"categories": categories}
      return jsonify(result)

  # GET questions with pagination (every 10 questions).
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


  # Create  a new question,
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
 
  # get questions to play the quiz.
  # This endpoint should take category and previous question parameters
  # and return a random questions within the given category,
  # if provided, and that is not one of the previous questions.
  @app.route("/quizzes", methods=['POST'])
  def get_next_quiz_question():
    try:
      previous_questions = request.json['previous_questions']
      previous_questions = map(str, previous_questions)
      quiz_category = request.json['quiz_category']['id']
      current_category = { "id": 0,"type": "ALL"}
      results =  None
      if int(quiz_category) == 0:
        results = Question.query
      else:
        results = Question.query.filter(Question.category == str(quiz_category))
        current_category = Category.format(Category.query.get(quiz_category))

      matching_questions = results.filter(Question.id.notin_(previous_questions)).all()

      response_data = Question.format(
                matching_questions[random.randrange(0, len(matching_questions))]) if len(matching_questions) > 0 else None

      return jsonify({"question": response_data})
    except:
      abort(422)

  # error handlers for all expected errors
  # including 404 and 422.
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
