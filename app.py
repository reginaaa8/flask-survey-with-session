from flask import Flask, request, render_template, redirect, flash, session 
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def index():
    '''home page - start survey'''
    return render_template('home.html', survey=survey)

@app.route('/start-survey', methods=['POST'])
def start_survey():
    '''clear responses from "database" before beginning survey'''
    session['responses'] = []
    return redirect(f'/questions/{len(session['responses'])}')

@app.route('/questions/<id>')
def show_question(id):
    '''show user current question'''
    if int(id) != len(session['responses']):
        #redirect to current question if user tries to access questions out of order
        flash(f'INVALID QUESTION ID: {id}')
        return redirect(f'/questions/{len(session['responses'])}')
    id = len(session['responses'])
    if len(session['responses']) == len(survey.questions):
        # when survey is complete, show user 'thank you' page
        return redirect('/completed')
    return render_template('questions.html', survey=survey, questions=survey.questions[id], id=id)

@app.route('/response', methods=['POST'])
def handle_response():
    '''add user response to session['responses'] (aka my fake db) and redirect to next question'''
    responses = session['responses']
    response = request.form['response']
    responses.append(response)
    session['responses'] = responses
    return redirect(f'/questions/{len(session['responses'])}')

@app.route('/completed')
def complete():
    return render_template('complete.html', survey=survey)

