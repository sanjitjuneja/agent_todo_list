from flask import Flask

app = Flask(__name__)

@app.route("/api/agents")
def return_all_agents():
    return "<p>Agents</p>"

@app.route('/api/classification')
def classification(user_input):
    return '<p>Classification</p>'

@app.route('/api/clarification')
def clarification(agent, user_input):
    return '<p>Clarification</p>'

@app.route('/api/execution')
def execution(agent, user_input, clarifications=None):
    return '<p>Execution</p>'

