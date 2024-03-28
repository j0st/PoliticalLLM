from llms import LLM

if __name__ == "__main__":
    # Define and run test setups here
    mixtral = LLM("Mixtral-8x7B-Instruct-v0.1")
    mixtral.pct("TEST2803", iterations=2)
