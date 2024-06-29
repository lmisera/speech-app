from openai import OpenAI
import os

openai_apikey = "sk-proj-2eGeQdHnlMBX8mXuyWzJT3BlbkFJu65H9JivfTxXJSFEuhGV"

client = OpenAI(api_key=openai_apikey)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)