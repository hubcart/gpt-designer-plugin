import json

import quart
import quart_cors
from quart import request
import openai
from api_integration import generate_design_image

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Initialize the GPT-3.5 model from OpenAI
openai.api_key = ''

@app.post("/designs")
async def generate_design():
    request_data = await request.get_json(force=True)
    user_input = request_data.get("user_input")

    # Use the GPT-3.5 model to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Extract the generated design idea from the response
    design_idea = "print on demand design of a dog"

    return quart.jsonify({"design_idea": design_idea})

@app.post("/images")
async def generate_image():
    request_data = await request.get_json(force=True)
    design_idea = request_data.get("design_idea")

    # Make the API call to generate the design image
    image = generate_design_image(design_idea, width=512, height=512)

    if image is not None:
        # Return the generated image
        return await quart.send_file(image, mimetype='image/png')
    else:
        return quart.Response(response='Error occurred during image generation.', status=500)

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

def main():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
