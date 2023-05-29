import json
import asyncio
import aiohttp
import quart
import quart_cors
from quart import request, Response

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

async def create_design(prompt):
    # Your design creation logic here
    # Return the design information or image as a string

@app.post("/create-design")
async def handle_create_design():
    try:
        data = await request.json
        prompt = data.get("prompt")

        if prompt:
            design_info = await create_design(prompt)
            if design_info:
                # Chunked Transfer-Encoding implementation
                async def stream_response():
                    # Split the response into smaller chunks
                    chunk_size = 4096
                    for i in range(0, len(design_info), chunk_size):
                        chunk = design_info[i:i+chunk_size]
                        yield chunk
                        await asyncio.sleep(0.1)  # Optional delay to control chunk rate

                headers = {"Content-Type": "text/plain", "Transfer-Encoding": "chunked"}
                return Response(stream_response(), headers=headers)
            else:
                return quart.Response(response="Failed to create the design", status=500)
        else:
            return quart.Response(response="Invalid request payload", status=400)
    except Exception as e:
        return quart.Response(response="Error occurred during API call: " + str(e), status=500)

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
