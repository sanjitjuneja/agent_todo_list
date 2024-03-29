import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from openai import OpenAI
import json

client = OpenAI(api_key="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")





def send_email(subject, body, recipient):
    smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server
    port = 587  # Replace with your SMTP port (commonly 587 for TLS)
    username = 'albertsun0000@gmail.com'  # Replace with your email address
    password = '765660aa'  # Replace with your email password
    recipient = 'sanjit.juneja@utexas.edu'  # Replace with the recipient's email address

    # Create the message
    message = MIMEMultipart()
    message['From'] = username
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to the server and send the email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Enable security
        server.login(username, password)
        server.sendmail(username, recipient, message.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

# METADATA
name = "Email Agent"
description = "Send an email with a subject, body, and recipient"
keywords = ["email", "send", "subject", "body", "recipient"]
functions = {
    "send_email": send_email,
}
actions = [
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email with a subject, body, and recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "The subject of the email",
                    },
                    "body": {
                        "type": "string",
                        "description": "The body content of the email",
                    },
                    "recipient": {
                        "type": "string",
                        "description": "The recipient's email address",
                    }
                },
                "required": ["subject", "body", "recipient"],
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