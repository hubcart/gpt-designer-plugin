import json
import aiohttp
import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

OPENAI_API_URL = "https://api.openai.com/v1/images/generations"

async def create_design(prompt):
    # Read the API key from api-key.txt file
    with open("api-key.txt", "r") as f:
        api_key = f.read().strip()

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
        async with session.post(OPENAI_API_URL, headers=headers, json=data) as response:
            if response.status == 200:
                response_json = await response.json()
                image_url = response_json["data"][0]["url"]
                return {"image_url": image_url}
            else:
                return None

@app.post("/images/generations")
async def handle_image_generation():
    try:
        data = await request.json
        prompt = data.get("prompt")

        if prompt:
            design_info = await create_design(prompt)
            if design_info:
                return quart.Response(response=json.dumps(design_info), status=200)
            else:
                return quart.Response(response="Failed to create the design", status=500)
        else:
            return quart.Response(response="Invalid request payload", status=400)
    except Exception as e:
        return quart.Response(response="Error occurred during API call: " + str(e), status=500)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

@app.get("/legal.html")
async def serve_legal_html():
    try:
        with open("legal.html") as f:
            text = f.read()
            return quart.Response(text, mimetype="text/html")
    except FileNotFoundError:
        return quart.Response(response="Legal page not found", status=404)

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
