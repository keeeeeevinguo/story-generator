import anthropic

from sanic import Sanic
from sanic.response import json, file
from dotenv import load_dotenv
import os
from pathlib import Path
from sanic_cors import CORS
from tortoise.contrib.sanic import register_tortoise
from models import Story, User
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

app = Sanic("StorybookGenerator")
CORS(app)
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()

@app.route("/", name="index")
async def index(request):
    return await file("static/index.html")

@app.route("/save_story", methods=["POST"], name="save_story")
async def save_story(request):
    data = request.json
    prompt = data.get("prompt", "")
    content = data.get("story", "")
    if not content:
        return json({"error": "No story content provided"}, status=400)
    try:
        story_obj = await Story.create(prompt=prompt, content=content)
        logger.info(f'story id: {story_obj.id}')
        return json({"message": "Story saved", "story_id": story_obj.id})
    except Exception as e:
        return json({"error": str(e)}, status=500)
    
@app.delete("/delete_story/<story_id:int>/", name="delete_story")
async def delete_story(request, story_id):
    try:
        story_obj = await Story.get(id=story_id)
        await story_obj.delete()
        return json({"message": "Story deleted"})
    except Exception as e:
        return json({"error": str(e)}, status=500)


@app.route("/stories", methods=["GET"], name="get_stories")
async def get_stories(request):
    try:
        stories = await Story.all().values("id", "prompt", "content", "generated_at")
        
        for story in stories:
            if story.get("generated_at"):
                story["generated_at"] = story["generated_at"].isoformat()
        
        return json({"stories": stories})
    except Exception as e:
        return json({"error": str(e)}, status=500)

@app.route("/generate_story", methods=["POST"])
async def generate_story(request):
    data = request.json
    prompt = data.get("prompt", "")
    grade = data.get("grade", "3rd Grade")
    vocab = data.get("vocab", "")
    genre = data.get("genre", "")


    if not prompt:
        return json({"error": "No prompt provided"}, status=400)

    try:
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
        
db_url = (
    f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST')}:3306/{os.getenv('MYSQL_DATABASE')}"
    )

register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["models"]},
        generate_schemas=True, 
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
