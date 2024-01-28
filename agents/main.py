from classification_agent import classify_task
from clarification_agent import get_clarifying_question
from utils import load_agents

agents = load_agents()


def return_all_agents():
    return agents


def classification(user_input):
    return classify_task(user_input)


def clarification(agent, user_input):
    return get_clarifying_question(agent, user_input)


def execution(agent, user_input, clarifications=None):
    if agent:
        # Execute the relevant function from the agent
        response = getattr(agent, 'execute')(user_input, clarifications)
        return response.choices[0].message.content.strip()
    else:
        return "No suitable agent found."


if __name__ == '__main__':
    user_input = input("Enter your task: ")

    agent = classify_task(user_input)
    print("Agent Picked: ", agent.get('name'))
    clarifiying_question = get_clarifying_question(agent, user_input)

    print("\n")
    print("\n")

    # Ask clarifying questions
    clarifications = input(clarifiying_question) if clarifiying_question else None


    if agent:
        # Execute the relevant function from the agent
        response = agent['execute'](user_input, clarifications)
        print(response.choices[0].message.content.strip())
    else:
        print("No suitable agent found.")
