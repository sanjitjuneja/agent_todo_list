from utils import load_agents
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def extract_keywords(input_prompt):
    # Sophisticated NLP-based extraction (here using TF-IDF for simplicity)
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([input_prompt])
    feature_names = vectorizer.get_feature_names_out()
    dense = vectors.todense().tolist()
    return dict(zip(feature_names, dense[0]))


def classify_task(user_input):
    agents = load_agents()
    input_keywords = extract_keywords(user_input)

    # Prepare a document consisting of user input and all agent keywords
    documents = [user_input] + [' '.join(agent_info.get('keywords', [])) for agent_name, agent_info in agents.items()]

    # Convert documents to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compute cosine similarity between user input and each agent
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    scores = {agent_name: cosine_similarities[0][idx] for idx, (agent_name, agent_info) in enumerate(agents.items())}

    # Selecting the top-scoring agent
    top_agent = max(scores, key=scores.get, default=None)
    return agents.get(top_agent)
