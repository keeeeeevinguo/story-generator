import anthropic

from sanic import Sanic
from sanic.response import json, file
from dotenv import load_dotenv
import os
from pathlib import Path
from sanic_cors import CORS

# Get the directory containing the script
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the project root
load_dotenv(BASE_DIR / '.env')

app = Sanic("StorybookGenerator")
CORS(app)
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()

@app.route("/", name="index")
async def index(request):
    return await file("static/index.html")



# You might need to serve additional static assets:
app.add_static("/css", "./static/css", name="css_static")
app.add_static("/js", "./static/js", name="js_static")
app.add_static("/assets", "./static/assets", name="assets_static")

@app.route("/generate_story", methods=["POST"])
async def generate_story(request):
    """
    Endpoint to generate a children's story based on a user prompt/topic.
    """
    data = request.json
    prompt = data.get("prompt", "")
    grade = data.get("grade", "3rd Grade")
    vocab = data.get("vocab", "")
    genre = data.get("genre", "")


    if not prompt:
        return json({"error": "No prompt provided"}, status=400)

    try:
        # Call OpenAI (or any other LLM) to generate the story
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            system="""You are a bestselling children's book author who writes stories directly without asking for clarification. 
                    Always generate a complete story based on the given prompt or theme. If the prompt is vague, use your creativity 
                    to fill in the details. Each story should be engaging, age-appropriate, and contain:
                    - A clear beginning, middle, and end
                    - Memorable characters
                    - A positive message or moral
                    - Appropriate length for a {grade} reader (around 300-400 words)
                    - Ensure the story uses the following vocabulary words: {vocab}.
                    - Ensure the story isin the {genre} genre.
                    
                    Write the story directly without any meta-commentary or questions.""",
            messages=[
                {"role": "user", "content": [{"type": "text", "text": f"Generate a children's story about {prompt}. Write the story directly without asking any questions or seeking clarification."}]},
            ],
            temperature=0.8,
            max_tokens=1500,
        )

        story_text = response.content[0].text
        return json({"story": story_text})
    except Exception as e:
        return json({"error": str(e)}, status=500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
