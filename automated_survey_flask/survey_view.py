from . import app
from .models import Survey
from flask import url_for, session
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse


@app.route('/voice')
def voice_survey():
    response = VoiceResponse()
    #response.record()

    survey = Survey.query.first()
    if survey_error(survey, response.say):
        return str(response)

    #response.say("hey there")
    #welcome_user(survey, response.say)

    # test collecting feedback
    response.gather()
    
    # test playing audio
    response.play("https://erogol.github.io/ddc-samples/wavs/s1.wav")
    redirect_to_first_question(response, survey)
    return str(response)

def welcome_user(survey, send_function):
    welcome_text = 'yoyo robin Welcome to the %s' % survey.title
    send_function(welcome_text)

def redirect_to_first_question(response, survey):
    first_question = survey.questions.order_by('id').first()
    first_question_url = url_for('question', question_id=first_question.id)
    response.redirect(url=first_question_url, method='GET')

def survey_error(survey, send_function):
    if not survey:
        send_function('Sorry, but there are no surveys to be answered.')
        return True
    elif not survey.has_questions:
        send_function('Sorry, there are no questions for this survey.')
        return True
    return False

@app.route('/message')
def sms_survey():
    response = MessagingResponse()

    survey = Survey.query.first()
    if survey_error(survey, response.message):
        return str(response)

    if 'question_id' in session:
        response.redirect(url_for('answer', question_id=session['question_id']))
    else:
        welcome_user(survey, response.message)
        redirect_to_first_question(response, survey)
    return str(response)

