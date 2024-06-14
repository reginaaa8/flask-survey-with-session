from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.route('/')
def index():
    '''home page - start survey'''
    return render_template('home.html', survey=survey)

@app.route('/start-survey', methods=['POST'])
def start_survey():
    '''clear responses from "database" before beginning survey'''
    RESPONSES.clear()
    return redirect(f'/questions/{len(RESPONSES)}')

@app.route('/questions/<id>')
def show_question(id):
    '''show user current question'''
    if int(id) != len(RESPONSES):
        #redirect to current question if user tries to access questions out of order
        flash(f'INVALID QUESTION ID: {id}')
        return redirect(f'/questions/{len(RESPONSES)}')
    id = len(RESPONSES)
    if len(RESPONSES) == len(survey.questions):
        # when survey is complete, show user 'thank you' page
        return redirect('/completed')
    return render_template('questions.html', survey=survey, questions=survey.questions[id], id=id)

@app.route('/response', methods=['POST'])
def handle_response():
    '''add user response to RESPONSES (aka my fake db) and redirect to next question'''
    response = request.form['response']
    RESPONSES.append(response)
    return redirect(f'/questions/{len(RESPONSES)}')

@app.route('/completed')
def complete():
    return render_template('complete.html', survey=survey)

