import json
import aiohttp
import quart
import quart_cors
from quart import request, stream_with_context

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

async def create_design(prompt):
    url = "https://try.hubcart.ai:8001/sdapi/v1/txt2img"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"prompt": prompt, "send_images": False, "save_images": True}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                # Enable chunked transfer encoding
                response.enable_chunked_encoding()
                async with response:
                    while True:
                        chunk = await response.content.read(4096)
                        if not chunk:
                            break
                        yield chunk

@app.post("/create-design")
async def handle_create_design():
    try:
        data = await request.json
        prompt = data.get("prompt")

        if prompt:
            async def generate_chunks():
                async for chunk in create_design(prompt):
                    yield chunk

            return quart.Response(stream_with_context(generate_chunks()), status=200, content_type="application/json")
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
