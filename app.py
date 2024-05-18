"""
chatbot's webserver based on Flask
"""

import openai
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = 'your OpenAI API key'
calendly_api_token = 'your calendly api access token'
calendly_account_userid = 'your calendly userid'

def get_calendy_events(event_uuid=None):
    # list scheduled events from the user's Calendly account
    calendly_get_api_url = f'https://api.calendly.com/scheduled_events?user=https://api.calendly.com/users/{calendly_account_userid}'

    headers = {"Authorization": f"Bearer {calendly_api_token}"}
    response = requests.get(calendly_get_api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve events from Calendly."}

def cancel_calendy_events(event_uuid):
    # cancel an event from the user's Calendly account
    calendly_cancel_api_url = f'https://api.calendly.com/scheduled_events/{event_uuid}/cancellation'

    headers = {"Authorization": f"Bearer {calendly_api_token}"}
    data = {
        'reason': "chatbot delete event"
    }
    response = requests.post(calendly_cancel_api_url, headers=headers, json=data)
    #print("### response.status_code = {}".format(response.status_code))

    if response.status_code == 201:
        return response.json()
    else:
        return {"error": "Failed to cancel event in Calendly."}

available_functions = {
    "get_calendy_events": get_calendy_events,
    "cancel_calendy_events": cancel_calendy_events,
}

functions = [
    {
        "name": "get_calendy_events",
        "description": "List all my scheduled events from Calendly.",
    },
    {
        "name": "cancel_calendy_events",
        "description": "Given one event's uuid, cancel this scheduled event from Calendly.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_uuid": {"type": "string", "description": "The event's uuid."}
            },
            "required": ["event_uuid"],
        },
    }
]

def execute_function_call(function_name, arguments=None):
    function = available_functions.get(function_name,None)
    if function:
        arguments = json.loads(arguments)
        if arguments is not None:
            results = function(**arguments)
    else:
        results = f"Error: function {function_name} does not exist"
    return results

@app.route('/chat', methods=['POST'])
def chat_interaction():
    data = request.json
    user_message = data.get('message', '')

    try:
        chat_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                      {"role": "user", "content": user_message}
                    ],
            functions=functions,
            function_call="auto",
        )

        #print("### chatgpt response  = {}".format(chat_response))
        if chat_response.choices[0].message.function_call is None:
            return "cannot help on this request. I can help you to list or delete events on Calendy."

        # extract function name from chatgpt reply and call it
        func_name = chat_response.choices[0].message.function_call.name
        args = chat_response.choices[0].message.function_call.arguments

        #print("### func_name = {}, args = {} \n".format(func_name, args))
        func_response = execute_function_call(func_name, args)

        return func_response
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
