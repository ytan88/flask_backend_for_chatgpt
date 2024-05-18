import requests, json
from datetime import datetime
import readline

def send_message_to_flask_server(user_input):
    url = 'http://127.0.0.1:8080/chat'
    prefix = "You are a chatbot that can list and manage events on a Calendly account. "
    full_message = prefix + user_input
    data = {'message': full_message}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)
    return response.text

def parse_iso_datetime(iso_str):
    # Parse an ISO 8601 datetime string to a datetime object
    try:
        return datetime.fromisoformat(iso_str.rstrip('Z'))
    except ValueError:
        return None

def format_datetime(dt_obj):
    # Return a formatted, more readable string from a datetime object
    if dt_obj:
        return dt_obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return 'Unknown time'

def extract_event_details(json_payload):
    # Convert the JSON payload into a dictionary
    data_dict = json.loads(json_payload)

    # Iterate over each event in the 'collection'
    for event in data_dict.get('collection', []):
        # Extract and format event start and end times
        start_time = format_datetime(parse_iso_datetime(event.get('start_time', '')))
        end_time = format_datetime(parse_iso_datetime(event.get('end_time', '')))

        # Extract the UUID from the 'uri'
        uri = event.get('uri', '')
        uuid = uri.split('/')[-1] if uri else 'No UUID found'

        print(f"Event Start Time: {start_time}, Event End Time: {end_time}, UUID: {uuid}")

def main():
    print("Welcome to the Calendly Event Management CLI")
    print("Type your command or type 'quit' to exit.")

    # cli history
    histfile = ".cli_history"
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass

    while True:
        try:
            user_input = input("Ask chatbot (or 'quit' to exit): ")

            if user_input.lower() == 'quit':
                print("Exiting the CLI. Goodbye!")
                break

            response = send_message_to_flask_server(user_input)

            # print out the original/complete JSON data
            #print(f"Chatbot: {response}")

            try:
                # print out events' key info with readible format
                extract_event_details(response)
            except:
                print(f"Chatbot: {response}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting the chat bot CLI. Goodbye!")
            break

    # Save cli history
    readline.write_history_file(histfile)

if __name__ == "__main__":
    main()
