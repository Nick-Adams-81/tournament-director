import mlflow

# Simulated chatbot function (replace this with your actual chatbot call)
def chat_bot(user_input):
    """Mock chatbot response function for testing."""
    responses = {
        "What is the minimum bet rule in a tournament?": "The minimum bet must be at least the big blind.",
        "Can I talk about my hand while in play?": "No, discussing your hand in play is against the rules.",
        "What happens if a player acts out of turn?": "Action out of turn may be binding if the action does not change."
    }
    return responses.get(user_input, "I'm sorry, I don't know the answer.")

# Test dataset (Expected vs Actual Responses)
benchmark_tests = [
    {
        "question": "What is the minimum bet rule in a tournament?",
        "expected": ["The minimum bet must be at least the big blind.", "A bet must be at least the size of the big blind."],
    },
    {
        "question": "Can I talk about my hand while in play?",
        "expected": ["No, discussing your hand in play is against the rules.", "You are not allowed to discuss your hand."]
    },
    {
        "question": "What happens if a player acts out of turn?",
        "expected": ["Action out of turn may be binding if the action does not change.", "An out-of-turn action might be enforced if it doesn't change."]
    },
]

# Start MLflow experiment
mlflow.set_experiment("TDA Chatbot Benchmarking")

# Start a top-level run for benchmarking
with mlflow.start_run(run_name="benchmark_run"):
    total_tests = len(benchmark_tests)
    correct = 0

    for idx, test in enumerate(benchmark_tests, 1):
        question = test["question"]
        expected_responses = test["expected"]
        actual_response = chat_bot(question)

        # Check if the response is similar to any expected response
        is_correct = any(expected.lower() in actual_response.lower() for expected in expected_responses)

        # Log unique parameters and metrics for each test case
        mlflow.log_param(f"Test_{idx}_Question", question)  # Unique name for each question
        mlflow.log_param(f"Test_{idx}_Actual_Response", actual_response)  # Log actual response
        mlflow.log_metric(f"Test_{idx}_Correct", int(is_correct))  # Log correctness for each question

        if is_correct:
            correct += 1

    # Calculate accuracy and log it in the top-level run
    accuracy = correct / total_tests
    mlflow.log_metric("Benchmark_Accuracy", accuracy)

    print(f"Benchmarking completed. Accuracy: {accuracy:.2%}")
