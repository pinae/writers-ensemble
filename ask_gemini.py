import os
from google import genai
from google.genai import types
from jinja2 import Environment, FileSystemLoader
env = Environment(
    loader=FileSystemLoader("templates/")
)

client = genai.Client()

state = {
    "story": "",
    "paragraph": "",
}
with open("story.md") as f:
    state["story"] = f.read()

template = env.get_template("daramaturgica.j2")
for filename in os.listdir("dramatugica"):
    with open(f"dramatugica/{filename}") as f:
        state["key_points"] = f.read()
    prompt = template.render(**state)
    print(prompt)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        )
    )
    print(response.text)