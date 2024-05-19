# flask backend use chatgpt api
A simple Flask backend that uses the ChatGPT API to show and remove events on a Calendly account for automated scheduling and management.

# This project implemented a chatbot server and CLI to interact with it.
    The sever part run on Ubuntu22 Linux as local or microservice.

# How to use it

## start the webserver locally:
    $ python3 app.py

## start the CLI:
    $ python3 chatbot_cli.py

## how to interact with chatbot CLI:

### Type in your message to chatgpt when this prompt show up:
    Welcome to the Calendly Event Management CLI
    Type your command or type 'quit' to exit.
    Ask chatbot (or 'quit' to exit):

### To list all events on Calendy, you can ask "show me the scheduled events".
    Events will be printed on CLI in JSON format as below:

    Ask chatbot (or 'quit' to exit): show me all events
    Event Start Time: 2024-03-15 16:00:00, Event End Time: 2024-03-15 16:30:00, UUID: 392b36c8-1e98-4403-b886-6d8272a84ed3
    Event Start Time: 2024-03-15 18:15:00, Event End Time: 2024-03-15 18:45:00, UUID: fa8a527d-194e-464f-bceb-643ae19c5b26
    Ask chatbot (or 'quit' to exit):

### To cancel an event, you can ask "I want to cancel one event with uuid = 392b36c8-1e98-4403-b886-6d8272a84ed3 on Calendy account.". The uuid is the UUID string in above reply.

# packages to install
    sudo apt install code
    sudo apt install apt-transport-https
    pip3 install Flask
    pip3 install connexion
    pip3 install 'connexion[swagger-ui]'
    pip3 install 'connexion[flask]'
    pip3 install 'connexion[uvicorn]'
    pip3 install scipy
    pip3 install tenacity
    pip3 install tiktoken
    pip3 install termcolor
    pip3 install openai
