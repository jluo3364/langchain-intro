import ollama

response = ollama.chat(model='llama3', messages=[
{
    'role': 'user',
    'content': 'What is Neo4j?',
},
])

print(response['message']['content'])

