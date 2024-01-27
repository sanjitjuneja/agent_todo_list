import os

from openai import OpenAI

client = OpenAI(api_key="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")


def get_clarifying_question(agent, user_input):
    if not agent or not user_input:
        return "Invalid agent or user input."

    # Constructing the chat messages
    messages = [{"role": "user", "content": "Based on the following user input and agent capabilities, please formulate clarifying questions. For any additional info needed from the user be explicit with a bullet point list and type of info needed:"},
                {"role": "system", "content": "Here is the original user input: " + user_input},
                {"role": "system", "content": f"Agent Name: {agent.get('name')}"},
                {"role": "system", "content": f"Agent Description: {agent.get('description')}"},
                {"role": "system", "content": "Agent Actions:"}]
    for action in agent.get('actions', []):
        messages.append({"role": "system", "content": f"- {action['function']['name']}: {action['function']['description']}"})

    # Constructing the chat completion request
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages
    )

    # Extracting and returning the clarifying question(s)
    return response.choices[0].message.content.strip()
