import sys
import json
from datetime import datetime
from debate.crew import Debate

def run():
    """Run the Debate Crew"""
    inputs = {
        "topic": "AI LLMs and their impact on human creativity"
    }
    try:
        Debate().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """Train the Debate Crew"""
    inputs = {
        "topic": "AI LLMs and their impact on human creativity",
        "current_year": str(datetime.now().year)
    }
    try:
        Debate().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """Replay the Debate Crew from a specific task"""
    try:
        Debate().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """Test the Debate Crew"""
    inputs = {
        "topic": "AI LLMs and their impact on human creativity",
        "current_year": str(datetime.now().year)
    }
    try:
        Debate().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """Run Debate Crew with JSON trigger"""
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": trigger_payload.get("topic", ""),
        "current_year": str(datetime.now().year)
    }

    try:
        result = Debate().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")

if __name__ == "__main__":
    run()
