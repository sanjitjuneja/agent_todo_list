from utils import load_agents


def extract_keywords(input_prompt):
    # You can replace this with a more sophisticated NLP-based extraction
    return input_prompt.lower().split()


def classify_task(user_input):
    agents = load_agents()
    input_keywords = extract_keywords(user_input)

    # Scoring system: For each agent, count how many keywords match the input
    scores = {}
    for agent_name, agent_info in agents.items():
        agent_keywords = agent_info.get('keywords', [])
        scores[agent_name] = sum(keyword in input_keywords for keyword in agent_keywords)

    # Selecting the top-scoring agent
    top_agent = max(scores, key=scores.get, default=None)
    return agents.get(top_agent)
