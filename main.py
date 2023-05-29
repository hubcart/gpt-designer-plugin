import json
import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="*")  # Allow requests from any origin for browser access

# Keep track of user information. Does not persist if Python session is restarted.
USERS = {}

@app.route("/user/", methods=["GET"])
async def get_user():
    # Make the API call to retrieve user information
    # Replace this with your actual API call implementation
    # For simplicity, this example returns a static response
    response = "User information"
    
    # Check if the request is coming from a browser or SSH
    user_agent = request.headers.get("User-Agent")
    is_browser_request = "Mozilla" in user_agent or "Chrome" in user_agent
    
    if is_browser_request:
        # Return a JSON response for browser access
        return quart.jsonify({"response": response})
    else:
        # Return a plain text response for SSH access
        return quart.Response(response=response, status=200, content_type="text/plain")

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
