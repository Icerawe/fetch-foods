import openai
import json


with open('secrets.json', 'r') as f:
    secrets = json.load(f)

keyword = "kindle"
openai.api_key = secrets['api_key']
response = openai.Completion.create(
    engine='text-davinci-003',  # Use 'text-davinci-003' for GPT-3.5 Turbo
    prompt=f"""Help me write a blog post in English with the title {keyword} with convincing points in segmented writing and displayed images using markdown syntax. To display the images, use the markdown syntax with the url from unsplash (https://source.unsplash.com/960x640/?{keyword} before each heading outline""",
    max_tokens=2000,
)

value = response['choices'][0]['text'].strip()
import markdown
html = markdown.markdown(value)

