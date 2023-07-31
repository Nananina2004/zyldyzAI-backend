import random
from . import router
    
@router.get("")
def get_question():
    question_data = [
    {
      "id": 1,
      "question": "What is my zodiac sign?",
    },
    {
      "id": 2,
      "question": "Will I get to travel abroad for education?",
    },
    {
      "id": 3,
      "question": "When will I meet the love of my life?",
    },
    {
      "id": 4,
      "question": "Can you tell me about money flow throughout my life?",
    },
    {
      "id": 5,
      "question": "Tell me about my personality.",
    },
    {
      "id": 6,
      "question": "What are my strengths and weaknesses ?",
    },
    {
      "id": 7,
      "question": "What kind of person should I marry ?",
    },
    {
      "id": 8,
      "question": "Does my future hold anything big ?",
    },
  ]
    random_question = random.choice(question_data)

    if not random_question:
        response_data = {
            "message": "No question was found in the response."
        }
        return response_data, 500

    response_data = {
        "question": random_question["question"],
    }

    return response_data







