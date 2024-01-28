# Apollo

## A self completing to-do list

Intellegently select multiple agents to break down complex tasks, and complete them

"Schedule a meeting with Mark for next weekend"
- Calendar agent checks for conflicts
- Same agent schedules a meeting
- GPT agent drafts an email, asking if Mark is free
- Gmail agent sends email


# Technical details

## Pipeline

Our pipeline can be broken down into 3 steps
- Classification - using cosine similary to select which agents to use out of a large list
- Clarification - Ask clarifying questions that will fill missing information for the agents
- Executaion - Run agents sequentially, completing the task

## Tech Stack
- Next.js, tailwind
- Flask/Python backend
- AWS Database


