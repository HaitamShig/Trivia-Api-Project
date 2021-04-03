GETTING STARTED:

-This Application is only hosted locally for now which is why it's working on the URL 127.0.0.1:5000
-No authentification required for this application


ERROR MESSAGES :

ERROR 400 : Bad Request

- This error happens whenever the user want to use POST method in an endpoint and provides a badly formatted request

{
  "success": False,
  "error": 400,
  "message": "bad request"
}



ERROR 404 : Resource Not Found

- This error happens whenever the application doesn't find any data that matches what the user demands

{
  "success": False,
  "error": 404,
  "message": "resource not found"
}



ERROR 422 : Unprocessable Entity

- This error happens whenever the uses a POST method with an endpoint and provides a well formatted request with the required data, but this data can't be processed and should be changed

{
  "success": False,
  "error": 422,
  "message": "unprocessable entity"
}



ERROR 500: Internal Server Error

- This error happens when some problem occurs with the server which makes it unable to load the data that the user asked for
 
{
  "success": False,
  "error": 500,
  "message": "internal server error"
}



ENDPOINTS :



GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

example: curl 127.0.0.1:5000/categories 

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

GET '/questions?page={number_of_page}'
- Retrieve all the questions of all the categories classified by pages of 10 questions maximum 
- Request Arguments : None
- Returns : An object that contains a key of questions which contains a list of 10 or less questions depending on the page number, as well as the key total_questions which contains them total number of the quetions and a key of categories which contains all the available categories 

example : curl http://127.0.0.1:5000/questions?page=1

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "1", 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": "5", 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": "4", 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Uruguay", 
      "category": "6", 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": "3", 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Escher", 
      "category": "2", 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": "2", 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": "2", 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": "2", 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 18
}


GET '/categories/{category_id}/questions?page={number_of_page}'
- Retrieve all the questions that belong to the specified category_id that the user enters classified by pages of 10 questions maximum 
- Request Arguments : None
- Returns : An object that contains a key of questions which contains a list of 10 or less questions depending on the page number, as well as the key category which specifies the desired category 

example: curl 127.0.0.1:5000/categories/1/questions?page=1

{
  "category": "Science", 
  "questions": [
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "2", 
      "category": "1", 
      "difficulty": 1, 
      "id": 24, 
      "question": "how 1+1 is"
    }, 
    {
      "answer": "madrid", 
      "category": "1", 
      "difficulty": 1, 
      "id": 32, 
      "question": "real"
    }
  ], 
  "success": true
}


DELETE  '/questions/{question_id}'
- Delete the question which its id is question_id
- Request Arguments : None
- Returns: an object which contains the Key number_of_questions which represents the number of the questions after deleting the desired question

example : curl -X DELETE 127.0.0.1:5000/questions/18
{
  "number_of_questions": 17,
  "success": true
}


POST '/questions'
- Search for a all the questions that contain the searchTerm from the request
- Request Arguments : { "searchTerm": "{search_term}"}
- Returns: An object which contains the Key questions which contains a list of the found questions

example: curl -X POST 127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "world" }'

{
    "current_category": "1",
    "questions": [
        {
            "answer": "Uruguay",
            "category": "6",
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Germany",
            "category": "6",
            "difficulty": 1,
            "id": 31,
            "question": "who has won the world cup of 2014"
        }
    ],
    "success": true,
    "total_questions": 17
}

POST '/questions'
- Add a new question with its answer, category and difficulty
- Request Arguments : 
{ "question": "{the_question_to_enter}",
  "answer": "{the_answer}",
  "difficulty": "{difficulty}",
  "category": "{category}"
}
all the values have to be strings excepr for the difficulty which need to be a number equal or less than 5 
- Returns: An object which contains the Key number_of_questions which contains the total number of the questions after adding the desired question

example : curl -X 127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "who's won the ballon d'or 2017", "answer" : "cristiano ronaldo" , "difficulty": 1, "category": "6"}'

{
  "number_of_questions": 18, 
  "success": true
}
 

POST '/quizzes'
- Sends back a random question from a choosen category and different from a list of previous questions sent in the request
- Request Arguments : 
{ "previous_question": "{a_list_of_questions}",
  "category": "{'id': 'category_id'}"
}
- Returns: An object which contains the key question which is a random choosen question from the specified category 
 
example: curl -X 127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{ "previous_questions": [], "category": {"id": 6}'

{
  "question": {
    "answer": "Germany", 
    "category": "6", 
    "difficulty": 1, 
    "id": 31, 
    "question": "who has won the world cup of 2014"
  }, 
  "success": true
}







