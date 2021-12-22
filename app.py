from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.wrappers.response import Response
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route('/')
def appstart():
    return render_template('home.html', survey=survey)

@app.route('/begin' ,methods=["POST"])
def begin_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def get_answer():
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    if len(responses) == len(survey.questions):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}') 
        

    

@app.route('/questions/<int:qid>')
def show_question(qid):
    
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        return redirect('/')

    if len(responses) == len(survey.questions):
        return redirect('/complete')

    if len(responses) != qid:
        flash(f'Invalid question Id: {qid}, back to question {len(responses)}')
        return redirect(f'/questions/{len(responses)}')


    question = survey.questions[qid]
    return render_template('question.html', question=question) 

@app.route('/complete')
def complete():
    return render_template('completion.html')  



