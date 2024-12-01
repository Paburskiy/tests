from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# A simple in-memory database for tests
tests = {}

@app.route('/')
def index():
    return render_template('index.html', tests=tests)

@app.route('/take_test/<test_name>', methods=['GET', 'POST'])
def take_test(test_name):
    test = tests.get(test_name)
    if not test:
        return "Test not found!", 404

    if request.method == 'POST':
        answers = request.form.to_dict()
        correct_count = sum(
            1 for question, answer in test['questions'].items() if answers.get(question) == answer
        )
        return render_template('result.html', score=correct_count, total=len(test['questions']))

    return render_template('take_test.html', test_name=test_name, questions=test['questions'])

@app.route('/create_test', methods=['GET', 'POST'])
def create_test():
    if request.method == 'POST':
        test_name = request.form['test_name']
        questions = {}
        for i in range(len(request.form) // 2):  # Divide by 2 (question-answer pairs)
            question = request.form.get(f'question_{i}')
            answer = request.form.get(f'answer_{i}')
            if question and answer:
                questions[question] = answer
        
        tests[test_name] = {'questions': questions}
        return redirect(url_for('index'))

    return render_template('create_test.html')

if __name__ == '__main__':
    app.run(debug=True)