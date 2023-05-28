import json

import quart
import quart_cors
from quart import request
import openai
from api_integration import generate_design_image

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Set your API key here
API_KEY_FILE = "/api_key.txt"

# Initialize the GPT-3.5 model from OpenAI
openai.api_key = ""

def load_api_key():
    with open(API_KEY_FILE, "r") as file:
        return file.read().strip()

@app.before_serving
async def setup():
    api_key = load_api_key()
    openai.api_key = api_key

@app.post("/design-plugin/generate")
async def generate_design():
    request_data = await quart.request.get_json(force=True)
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
    design_idea = "print on demand design of a dog"  # Replace with your logic to extract the design idea

    # Make the API call to generate the design image
    image = generate_design_image(design_idea, width=512, height=512)

    if image is not None:
        # Convert the image to base64 for sending in the response
        image_base64 = "<base64-encoded-image>"  # Replace with your logic to convert the image to base64

        # Create the response data
        response_data = {
            "design_idea": design_idea,
            "image_base64": image_base64
        }
        return quart.Response(response=json.dumps(response_data), status=200, mimetype="application/json")
    else:
        error_data = {
            "error": "Error occurred during image generation."
        }
        return quart.Response(response=json.dumps(error_data), status=500, mimetype="application/json")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
