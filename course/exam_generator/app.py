'''
Adam Forestier
June 20, 2023
Description: Create multiple choice exam by topic
'''

import openai

from key import key as openai_key

openai.api_key = openai_key 

def create_test_prompt(topic: str, num_questions: int, num_possible_answers=4, num_correct_answers=1) -> str:
    '''
    arguments: topic of test, number of questions in test, number of possible answers per question
    returns: prompt to feed to api
    descritpion: create_test_prompt returns a formatted prompt that requests api to create a multiple choice test
    '''
    return f"Create a multiple choice quiz on the topic of {topic}. It consists of {num_questions} questions. Each question should have {num_possible_answers} options. The questions must be based on fact, not opinion. Only include questions you are 100% sure you know the answer to. Also include the correct answer for each question using the starting string \'Correct Answer: \'"

def create_student_view(quiz: str, num_questions: int) -> dict:
    '''
    arguments: the quiz with answers and number of questions
    returns: quiz with no answers
    description: create_student_view takes in a quiz with answers and returns a quiz no answers
    '''
    student_view = {1:''}
    question_number = 1
    for line in quiz.split('\n'):
        if not line.startswith('Correct Answer'):
            student_view[question_number] += line + '\n'
        else:
            if question_number < num_questions:
                question_number += 1
                student_view[question_number] =''
    return student_view

def extract_answers(quiz: str, num_questions: int) -> dict:
    '''
    arguments: response

    description:
    '''
    answer_view = {1:''}
    question_number = 1
    for line in quiz.split('\n'):
        if line.startswith('Correct Answer:'):
            answer_view[question_number] += line + '\n'
            if question_number < num_questions:
                question_number += 1
                answer_view[question_number] = ''
    return answer_view

def take_quiz(student_view: dict) -> dict:
    '''
    arguments: quiz without answers
    returns: dictionary of questions and student responses
    description: take_quiz displays each question 1 at a time, the student answers and the answer is saved to that question
    '''
    student_answers = {}
    for question, question_view in student_view.items():
        print(question_view)
        answer = input("Enter your answer: ")
        student_answers[question] = answer
    return student_answers

def grade_quiz(student_answers: dict, correct_answers: dict) -> float:
    '''
    arguments: student answers and correct answers
    returns: a float of student grade
    description: grade_quiz compares student answers to correct answers and provides a grade based upon the percentage they answered correctly
    '''
    correct_answers = 0
    for question, answer in student_answers.items():
        if answer.upper() == correct_answers[question][16]:
            correct_answers += 1
    grade = 100 * correct_answers / len(answers)
    return grade

# Create quiz
prompt = create_test_prompt('Python', 4)
response = openai.Completion.create(
    model='text-davinci-003',
    prompt=prompt,
    max_tokens=256,
    temperature=.68
)

# Create test
quiz_with_answers = response['choices'][0]['text']
quiz = create_student_view(quiz=quiz_with_answers, num_questions=4)
answers = extract_answers(quiz=quiz_with_answers, num_questions=4)
print(answers[1][16])
# Simulate exam and grade
student_answers = take_quiz(student_view=quiz)
grade = grade_quiz(student_answers=student_answers, correct_answers=answers)
# print(f"You have received a {grade}% on the python quiz")