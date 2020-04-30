# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
PGPASSWORD=postgres psql --host=localhost --port=5432 --username=postgres < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
## REST API 


### Endpoints

```
GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions/<id>'
POST '/questions-search'
GET '/categories/<int:category_id>/questions'
POST'/quizzes'

```

```
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and 
the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that 
contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

```
GET '/questions'
- Fetches a dictionary containing all questions stored in the database. Results are paginated. 
By default, the first page with 10 questions/page is returned. 
- Request Arguments: page - representing umber of page to be returned. Example: ?page=1 
- Returns: An object containing a question list. Example below: 
{
  "categories": [
    {
      "id": 5,
      "type": "science"
    }
],
  "current_category": "science",
  "questions": [
    {
      "answer": "5",
      "category": "4",
      "difficulty": 5,
      "id": 4,
      "question": "2+2"
    }
  ],
  "total_questions": 1
}
```

```
POST '/questions'
- Creates a new question
- Request Arguments: a json with fields: question, answer, difficulty, category.
Example:
{"question":"2+2","answer":"5","difficulty":"5","category":"5"}
- Returns: An object containing operation status:
{
  "status": "question added"
}
```

```
DELETE '/questions/<id>'
- Removes question by its id
- Request Arguments: question id - path parameter.
- Returns: An object containing operation status:
{
  "status": "deleted"
}
```

```
POST '/questions-search'
- Retrieve questions that match the search phrase. 
Field 'question' will be matched with the question phrase. The response is paginated.
- Request Arguments: Json with fields: searchTerm and page. Exaample: 
{"searchTerm":"blah","page":"1"}
- Returns: An object containing list of questions:
{
  "categories": [
    {
      "id": 1,
      "type": "art"
    },
    {
      "id": 2,
      "type": "entertainment"
    },
    {
      "id": 3,
      "type": "geography"
    },
    {
      "id": 4,
      "type": "history"
    },
    {
      "id": 5,
      "type": "science"
    },
    {
      "id": 6,
      "type": "sports"
    }
  ],
  "current_category": "ALL",
  "questions": [
  
    {
      "answer": "blaaaah",
      "category": "1",
      "difficulty": 1,
      "id": 1,
      "question": "blah"
    }
  ],
  "total_questions": 1
}
```


```
GET '/categories/<int:category_id>/questions'
- Retrieve questions in given category

- Request Arguments: path parameter - category_id
- Returns: An object containing list of questions in given category:
{
  "categories": [
    {
      "id": 1,
      "type": "art"
    },
    {
      "id": 2,
      "type": "entertainment"
    },
    {
      "id": 3,
      "type": "geography"
    },
    {
      "id": 4,
      "type": "history"
    },
    {
      "id": 5,
      "type": "science"
    },
    {
      "id": 6,
      "type": "sports"
    }
  ],
  "current_category": "art",
  "questions": [
  
    {
      "answer": "blaaaah",
      "category": "1",
      "difficulty": 1,
      "id": 1,
      "question": "blah"
    }
  ],
  "total_questions": 1
}
```

```
POST '/quizes'

- Fetches a dictionary containing all questions stored in the database. Results are paginated. 
By default, the first page with 10 questions/page is returned. 
- Request Arguments: json containing category and previous question parameters
Example:
{"previous_questions":[],"quiz_category":{"type":"art","id":4}}
- Returns: a random questions within the given category. 
Example:
{
  "question": {
    "answer": "none",
    "category": "4",
    "difficulty": 5,
    "id": 5,
    "question": "what is your favourite color"
  }
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
### alternative commands
- log in to db with password, 
PGPASSWORD=postgres psql --host=localhost --port=5432 --username=postgres trivia_test < trivia.psql
- create database:
create database trivia_test
- drop database
drop database trivia_test
- run db script
PGPASSWORD=postgres psql --host=localhost --port=5432 --username=postgres trivia_test
