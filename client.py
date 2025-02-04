import argparse

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test an API call for OpenAI LLM and receive a response for any given prompt.", fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "--prompt", type=str, help="Any prompt is just fine", required=True
    )

    args = parser.parse_args()

    print(api_call(args.prompt))
