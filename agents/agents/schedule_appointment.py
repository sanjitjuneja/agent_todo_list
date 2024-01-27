from openai import OpenAI
import json

client = OpenAI(api_key="your-api-key")


# AGENT ACTIONS
from openai import OpenAI
import json
import requests  # For making API calls

client = OpenAI(api_key="your-api-key")

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def create_google_calendar_event(start_time, end_time, summary, description, attendees):
    # Load credentials
    creds = Credentials.from_authorized_user_file('token.json')

    # Build the service
    service = build('calendar', 'v3', credentials=creds)

    # Create event object
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Your/Timezone',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Your/Timezone',
        },
        'attendees': [{'email': attendee} for attendee in attendees],
    }

    # Call the Calendar API
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

    return event

def create_zoom_meeting(start_time, duration, topic, attendees):
    # Your Zoom JWT token
    jwt_token = 'Your JWT Token'

    headers = {
        'authorization': f'Bearer {jwt_token}',
        'content-type': 'application/json'
    }

    meeting_data = {
        'topic': topic,
        'type': 2,  # Scheduled meeting
        'start_time': start_time,
        'duration': duration,  # Duration in minutes
        'schedule_for': None,
        'timezone': 'Your/Timezone',
        'agenda': 'Meeting Agenda',
        'settings': {
            'host_video': False,
            'participant_video': False,
            'join_before_host': False,
            'mute_upon_entry': True,
            'watermark': False,
            'use_pmi': False,  # Personal Meeting ID
            'approval_type': 0,
            'registration_type': 1,
            'audio': 'both',
            'auto_recording': 'none',
            'enforce_login': False,
            'enforce_login_domains': '',
            'alternative_hosts': '',
            'global_dial_in_countries': ['US'],
        }
    }

    response = requests.post('https://api.zoom.us/v2/users/me/meetings', headers=headers, data=json.dumps(meeting_data))
    meeting_info = response.json()

    # Add attendees (if any)
    for attendee in attendees:
        # Code to add attendee to the meeting

    return meeting_info


# METADATA
name = "Calendar Zoom Agent"
description = "Set up Zoom meetings based on Google Calendar availability"
keywords = ["zoom", "meeting", "schedule", "calendar", "appointment"]
functions = {
    "schedule_zoom_meeting": schedule_zoom_meeting,
}
actions = [
    {
        "type": "function",
        "function": {
            "name": "schedule_zoom_meeting",
            "description": "Schedule a Zoom meeting based on the user's Google Calendar availability",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_schedule": {
                        "type": "string",
                        "description": "The user's current schedule in a structured format",
                    },
                    "meeting_details": {
                        "type": "object",
                        "properties": {
                            "email": {
                                "type": "string",
                                "description": "Email address of the person to meet with",
                            },
                            "description": {
                                "type": "string",
                                "description": "Brief description of the meeting",
                            }
                        },
                        "required": ["email"]
                    }
                },
                "required": ["user_schedule", "meeting_details"],
            },
        },
    }
]

# AGENT EXECUTE FUNCTION
def execute(user_input, clarifications=None):
    # Interaction logic with the GPT model
    # ... (similar to your provided example)


# AGENT EXECUTE FUNCTION
def execute(user_input, clarifications=None):
    # Step 1: send the conversation and available functions to the model
    if clarifications:
        messages = [{"role": "user", "content": "Here is the original user input: " + user_input + "\n Here are further clarifications for the actions: " + clarifications + "\n"}]
    else:
        messages = [{"role": "user", "content": user_input}]
    tools = actions
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = functions
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response
