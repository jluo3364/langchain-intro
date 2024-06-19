try:
    import ollama
except ImportError:
    print("The 'ollama' package is not installed. Install it using `pip install ollama-sdk`.")
try:
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': 'What is Neo4j?',
        },
    ])

    # Adjust based on actual response structure
    if 'message' in response and 'content' in response['message']:
        print(response['message']['content'])
    else:
        print("Unexpected response format:", response)
except Exception as e:
    print("An error occurred:", str(e))
