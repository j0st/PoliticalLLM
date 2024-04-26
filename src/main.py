from llms import LLM

if __name__ == "__main__":
    # Define and run test setups here

    # Choose LLM
    mixtral = LLM("Mixtral-8x7B-Instruct-v0.1")

    # Choose ideology tests and modifications
    mixtral.pct("Example_Filename", iterations=1)
   