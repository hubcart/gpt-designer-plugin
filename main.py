import openai
from api_integration import generate_design_image

def start_plugin():
    print("Welcome to the Print-on-Demand Design Plugin!")
    print("Let's brainstorm some design ideas.")

    # Initialize the GPT-3.5 model from OpenAI
    openai.api_key = ''

    # Start the conversation loop
    while True:
        user_input = input("User: ")

        # Exit the plugin if the user enters "exit"
        if user_input.lower() == "exit":
            print("Exiting the plugin.")
            break

        # Use the GPT-3.5 model to generate a response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Extract the generated design idea from the response
        design_idea = "print on demand design of a dog"

        print(f"Plugin: {design_idea}")

        # Ask the user if they are ready to generate the design image
        generate_image = input("Plugin: Are you ready to generate the design image? (yes/no): ")

        if generate_image.lower() == "yes":
            # Make the API call to generate the design image
            image = generate_design_image(design_idea, width=512, height=512)

            if image is not None:
                # Display the generated image
                print("Generated design image:")
                print(image)

                # Ask the user if they want to download or generate another image
                decision = input("Plugin: What would you like to do? (download/generate another/exit): ")

                if decision.lower() == "download":
                    # TODO: Implement the logic to download the image
                    print("Downloading the image...")
                elif decision.lower() == "generate another":
                    print("Generating another image...")
                elif decision.lower() == "exit":
                    print("Exiting the plugin.")
                    break
                else:
                    print("Invalid option. Generating another image...")
            else:
                print("Error occurred during image generation.")
        else:
            print("Plugin: Let's continue brainstorming!")

if __name__ == '__main__':
    start_plugin()
