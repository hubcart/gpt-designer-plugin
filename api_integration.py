import requests

def generate_design_image(prompt, width, height):
    url = 'https://plugin.hubcart.ai:7860/sdapi/v1/txt2img'

    # Prepare the request payload
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        # Make the API request
        response = requests.post(url, json=payload, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Extract the image from the response
            image = response.json().get('images', [])[0]

            return image

        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

    return None
