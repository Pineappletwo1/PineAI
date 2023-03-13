import uuid
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account
from google.protobuf.struct_pb2 import Struct, Value
from flask import Flask, request, send_file

app = Flask(__name__)

creds = service_account.Credentials.from_service_account_file('pineapple-s-chatbot-px9h-dc9cff1c72de.json')
project_id = 'pineapple-s-chatbot-px9h'

def detect_intent(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient(credentials=creds)
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    return response.query_result.fulfillment_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input from the form
        user_input = request.form['user_input']  # debug
        # Call the AI function with the input
        ai_output = detect_intent(project_id, str(uuid.uuid4()), user_input, 'en')

        # Return the result to the user
        return ai_output
    else:
        return send_file('public/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
