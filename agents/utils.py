import os
import importlib


def load_agents():
    agents = {}
    agent_dir = 'agents'

    for filename in os.listdir(agent_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(f'agents.{module_name}')

            # Extract metadata and functions from the agent module
            agent_info = {
                "name": getattr(module, "name", "Unknown Agent"),
                "description": getattr(module, "description", ""),
                "keywords": getattr(module, "keywords", []),
                "functions": getattr(module, "functions", {}),
                "execute": getattr(module, "execute", None)
            }

            agents[module_name] = agent_info

    return agents
