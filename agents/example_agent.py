from openai import OpenAI
import json

client = OpenAI(api_key="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")


# AGENT ACTIONS
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


# METADATA
name = "Weather Agent"
description = "Get the current weather in a given location"
keywords = ["weather", "forecast", "temperature", "hot", "cold", "rain", "snow", "sun", "cloudy", "windy", "humid"]
functions = {
    "get_current_weather": get_current_weather,
}
actions = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
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
