from flask import Flask, render_template, request
import json,os

app = Flask(__name__)

# Home route – shows all topics
@app.route('/')
def home():
    return render_template('index.html')

#Route for selection of topics
@app.route('/topics')
def topics():
    with open('lessons.json') as f:
        lessons = json.load(f)
    return render_template('topics.html', lessons=lessons)

# Route to show a specific lesson by ID
@app.route('/lesson/<int:lesson_id>')
def show_lesson(lesson_id):
    with open('lessons.json') as f:
        lessons = json.load(f)
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    return render_template('lesson.html', lesson=lesson)

# Route to show the quiz for each lesson
@app.route('/quiz/<int:lesson_id>')
def show_quiz(lesson_id):
    with open('questions.json') as f:
        questions = json.load(f)
    with open('lessons.json') as f:
        lessons = json.load(f)

    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    if not lesson:
        return "Lesson not found", 404

    quiz = questions.get(str(lesson_id), [])
    return render_template('quiz.html', lesson=lesson, questions=quiz)


# Route to handle quiz submission and show result
@app.route('/quiz/<int:lesson_id>/submit', methods=['POST'])
def submit_quiz(lesson_id):
    with open('questions.json') as f:
        questions = json.load(f)
    with open('lessons.json') as f:
        lessons = json.load(f)

    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    quiz = questions.get(str(lesson_id), [])

    score = 0
    total = len(quiz)

    for i, q in enumerate(quiz):
        user_answer = request.form.get(f'q{i}')
        correct_answer = q['answer']
        if user_answer == correct_answer:
            score += 1

    return render_template('results.html', lesson=lesson, score=score, total=total)

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render’s port
    app.run(host="0.0.0.0", port=port)
