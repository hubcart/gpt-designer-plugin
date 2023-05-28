import json
import quart
from quart import request
import openai
from api_integration import generate_design_image

app = quart.Quart(__name__)

# Initialize the GPT-3.5 model from OpenAI
openai.api_key = ''

# Define a decorator to add CORS headers to the responses
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://plugin.hubcart.ai"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
    return response

@app.post("/designs")
@add_cors_headers
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
@add_cors_headers
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
@add_cors_headers
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

def main():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
