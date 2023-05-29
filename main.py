import json
import aiohttp
import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

async def create_design(prompt):
    url = "https://try.hubcart.ai:8001/sdapi/v1/txt2img"  # API endpoint for creating designs
    headers = {"accept": "application/json", "Content-Type": "application/json"}  # Request headers
    data = {"prompt": prompt}  # Request payload with the prompt

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:  # If the API call is successful
                return await response.json()  # Return the design information in JSON format
            else:
                return None  # Return None if the API call fails

@app.post("/create-design")
async def handle_create_design():
    try:
        data = await request.json  # Extract the request payload
        prompt = data.get("prompt")  # Get the prompt from the payload

        if prompt:  # If a valid prompt is provided
            design_info = await create_design(prompt)  # Create the design using the prompt
            if design_info:  # If the design is created successfully
                return quart.Response(response=json.dumps(design_info), status=200)  # Return the design information as JSON
            else:
                return quart.Response(response="Failed to create the design", status=500)  # Return an error message if the design creation fails
        else:
            return quart.Response(response="Invalid request payload", status=400)  # Return an error message for an invalid request payload
    except Exception as e:
        return quart.Response(response="Error occurred during API call: " + str(e), status=500)  # Return an error message for any exceptions during the API call

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
