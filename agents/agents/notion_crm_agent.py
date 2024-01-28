from openai import OpenAI
import json
import requests

client = OpenAI(api_key="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")

# Notion API configuration
notion_token = 'secret_cWVtCXqPe20ozxdHiBtbmS60i1jLx3HtNCxJUecP8xZ'
notion_database_id = '333127d8f6ea423d86105d2f5c2e9963'
notion_headers = {
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}


# AGENT ACTIONS
def save_to_notion(name, date, summary):
    """Saves a contact and meeting summary to a Notion CRM page"""
    data = {
        "parent": {"database_id": notion_database_id},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": name
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": date
                }
            },
            "Summary": {
                "rich_text": [
                    {
                        "text": {
                            "content": summary
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(
        'https://api.notion.com/v1/pages/',
        headers=notion_headers,
        data=json.dumps(data)
    )

    # Detailed response handling
    if response.status_code in [200, 201]:
        return json.dumps({"status": "success", "message": "Contact and summary saved to Notion"})
    else:
        return json.dumps({"status": "error", "message": "Failed to save to Notion", "details": response.text})



# METADATA
name = "Notion CRM Agent"
description = "Saves a contact and meeting summary to a Notion CRM page"
keywords = ["notion", "crm", "customer", "relationship", "management", "save", "contact", "meeting", "summary"]
functions = {
    "save_to_notion": save_to_notion
}
actions = [
    {
        "type": "function",
        "function": {
            "name": "save_to_notion",
            "description": "Saves a contact and meeting summary to a Notion CRM page",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the contact"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date of the meeting"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Summary of the meeting"
                    }
                },
                "required": ["name", "date", "summary"],
            },
        },
    }
]


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