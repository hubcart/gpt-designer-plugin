import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.get("/user/")
async def get_user():
    url = "https://try.hubcart.ai:8001/user/"
    headers = {"accept": "application/json"}

    try:
        response = await quart.httpclient.get(url, headers=headers)
        if response.status_code == 200:
            return quart.Response(response=response.text, status=200)
        else:
            return quart.Response(response="Failed to retrieve user information", status=response.status_code)
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
