import argparse
import base64

import openai

def api_call(custom_prompt: str) -> str:

    try:
        # Instanciate OpenAI client
        client = openai.OpenAI()

        # Send prompt
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", "content": "You are a helpful assistant."
                },
                {
                    "role": "user", "content": custom_prompt
                }
            ]
        )
        # Extract and return the reply
        return response.choices[0].message
    except Exception as e:
        return f"An error occurred: {e}"

def vision_api_call(img_path: str, custom_prompt: str = "What is in this image?") -> str:

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    try:
        # Instanciate OpenAI client
        client = openai.OpenAI()

        # Getting the Base64 string
        base64_image = encode_image(img_path)

        # Send prompt
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": custom_prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
        )

        # Extract and return the reply
        return response.choices[0].message
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    argparse_description =  "Test an API call for OpenAI LLM and receive a"
    argparse_description += " response for any given prompt."

    parser = argparse.ArgumentParser(
        description=argparse_description, fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "--img-path",
        type=str,
        help="path to the image to be passed via API call",
        required=True
    )

    parser.add_argument(
        "--prompt",
        type=str,
        help="Any prompt is just fine",
        required=False
    )

    args = parser.parse_args()

    if args.prompt is None:
        print(vision_api_call(args.img_path))
    else:
        print(vision_api_call(args.img_path, args.prompt))
