import json
import aiohttp
from quart import Quart, request

app = Quart(__name__)

async def create_design(prompt):
    # Read the API key from api-key.txt file
    with open("api-key.txt", "r") as f:
        api_key = f.read().strip()

    url = "https://try.hubcart.ai/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "256x256",
        "response_format": "url"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                response_json = await response.json()
                image_url = response_json["data"][0]["url"]
                return {"image_url": image_url}
            else:
                return None

@app.route("/images/generations", methods=["POST"])
async def handle_image_generation():
    try:
        data = await request.json
        prompt = data.get("prompt")

        if prompt:
            design_info = await create_design(prompt)
            if design_info:
                return json.dumps(design_info)
            else:
                return "Failed to create the design", 500
        else:
            return "Invalid request payload", 400
    except Exception as e:
        return "Error occurred during API call: " + str(e), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)
