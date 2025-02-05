import ollama

response = ollama.chat(model="mistral", messages=[
    {"role": "system", "content": "You are a helpful medical assistant."},
    {"role": "user", "content": "Generate a structured medical report for a patient with diabetes."}
])

print(response["message"]["content"])
