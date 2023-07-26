from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os

load_dotenv()
app = Flask(__name__, static_url_path='', static_folder='.')

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get the user's input from the request
    data = request.get_json()
    name = data['name']
    current_city = data['currentCity']
    birth_city = data['birthCity']
    facts = ' '.join(data['facts'])

    # Generate the story and images using OpenAI's APIs
    story_parts, image_prompts = generate_story(name, current_city, birth_city, facts)
    image_urls = [generate_image(prompt) for prompt in image_prompts]

    return jsonify({'story': story_parts, 'image': image_urls})

def generate_story(name, current_city, birth_city, facts):
    # Use the ChatGPT API to generate the story
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{name} lives in {current_city}. They were born in {birth_city}. Here are three facts about them: {facts}"},
            {"role": "user", "content": "Tell me a 10-part story based on this information, with each part separated by '###'"},
        ]
    )

    print(f'Full story from ChatGPT: {response}')

    # Break the story into 10 pieces
    story = response['choices'][0]['message']['content']
    story_parts = story.split('###')
    print(f'Story parts together: {story_parts}')


    # Use the ChatGPT API to generate the image prompts
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "I am going to provide a story with 10 parts, for each of the stories, Create a prompts that describes the image that accompanies the story. Each prompt needs to be separated by '###'. Do not use character names. No need to start the sentence with Prompt or Part, just write the ten prompts separated by '###'"},
            {"role": "system", "content": "Here is an example of a type of prompt I am looking for: A highly detailed sketch of a quiet suburb in autumn, drawn using colored pencils"},            
            {"role": "system", "content": "Here is another example: Watercolor illustration of two kids who are best friends having a perfect summer day"},            
            {"role": "system", "content": f"Here are the 10 story parts: {story_parts}"},    
            {"role": "system", "content": "Do use the character names, instead substitude the name with a description like young man, or young woman. End each promot with '###'. The prompts should be short and hepful for a kid to understand the scene"}
        ]
    )
    print(f'Full prompts for submission: {response}')


    # Extract the image prompts
    image_prompts = response['choices'][0]['message']['content'].split('###')
    print(f'Promots ready for the submission: {image_prompts}')

    # Remove any empty strings from the story_parts and image_prompts lists
    story_parts = [part for part in story_parts if part]
    image_prompts = [prompt for prompt in image_prompts if prompt]
    print(len(story_parts))

    print(len(image_prompts))

    return story_parts, image_prompts


def generate_image(prompt):
    # Print the prompt for debugging
    print(f'Generating image for prompt: {prompt}')

    # Use the DALLE API to generate the image
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )

    return response['data'][0]['url']

if __name__ == '__main__':
    app.run(debug=True)
