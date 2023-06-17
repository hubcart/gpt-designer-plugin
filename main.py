import json
import aiohttp
import quart
from quart import request, jsonify

app = quart.Quart(__name__)

async def create_design(prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": get_api_key()
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

def get_api_key():
    with open("api-key.txt", "r") as f:
        return f.read().strip()

@app.after_request
async def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://chat.openai.com"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/create-design", methods=["POST", "OPTIONS"])
async def handle_create_design():
    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    try:
        data = await request.json
        prompt = data.get("prompt")

        if prompt:
            design_info = await create_design(prompt)
            if design_info:
                return jsonify(design_info), 200
            else:
                return jsonify({"message": "Failed to create the design"}), 500
        else:
            return jsonify({"message": "Invalid request payload"}), 400
    except Exception as e:
        return jsonify({"message": "Error occurred during API call: " + str(e)}), 500

@app.route("/logo.png", methods=["GET"])
async def plugin_logo():
    filename = "logo.png"
    return await quart.send_file(filename, mimetype="image/png")

@app.route("/.well-known/ai-plugin.json", methods=["GET"])
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/json"}

@app.route("/openapi.yaml", methods=["GET"])
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
