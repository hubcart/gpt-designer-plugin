import json
import aiohttp
import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

async def create_design(prompt):
    url = "https://try.hubcart.ai:5000/sdapi/v1/txt2img"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "prompt": prompt,
        "send_images": False,
        "save_images": True
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                response_json = await response.json()
                # Extract the seed from the response
                seed = response_json.get("info", {}).get("seed")
                return {"seed": seed} if seed else None
            else:
                return None

@app.post("/create-design")
async def handle_create_design():
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

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
