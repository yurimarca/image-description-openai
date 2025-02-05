import base64
import os
import cv2
import numpy as np
import json
import random


def encode_image(image_path: str) -> base64.b64encode:
    """
    Encode an image file to base64.
    Reference: https://platform.openai.com/docs/guides/vision

    Inputs:
        image_path (str): The path to the image file

    Output:
        base64.b64encode -- The base64 encoded image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def is_valid_image(filename: str) -> bool:
    """
    Check if image file extension is valid according with ref.
    Reference: https://platform.openai.com/docs/guides/vision

    Inputs:
        filename (str): Name of the image file

    Output:
        bool: True if the image file is valid.
    """

    valid_extensions = {".png", ".jpeg", ".jpg", ".webp", ".gif"}
    ext = os.path.splitext(filename)[1].lower()
    return ext in valid_extensions


def list_images(folder: str) -> list:
    """
    List all images in a folder.
    Reference: https://platform.openai.com/docs/guides/vision

    Inputs:
        folder (str): Folder path

    Output:
        list: list of image files in the folder
    """
    return [f for f in os.listdir(folder) if is_valid_image(f)]


def check_output_file(output: str) -> bool:
    """
    Check if the output file exists.

    Inputs:
        output (str): Name path of the output file
        """
    return os.path.exists(output)


def produce_result_sample(image_path: str, text: str, output_img: str):
    """
    Produce an image with text placed on the right side.

    Inputs:
        image_path (str): Path to the input image.
        text (str): The text from OpenAI's response.
        output_img (str): File name of new image.

    Output:
        Saves the image with text on the right side.
    """

    # Load the image
    image = cv2.imread(image_path)
    assert image is not None, f"ERROR: Unable to load image {image_path}"

    # Define text properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (255, 255, 255)  # White text
    bg_color = (0, 0, 0)  # Black background for better readability

    # Fix special characters by replacing unsupported ones
    replacements = {"ç": "c", "ã": "a", "õ": "o", "é": "e", "ê": "e", "á": "a", "í": "i"}
    for key, value in replacements.items():
        text = text.replace(key, value)

    # Get image dimensions
    img_height, img_width, _ = image.shape

    # Define text box width (adjust based on text length)
    text_box_width = int(img_width * 3)  # Allocate 50% extra space for text

    # Split text into multiple lines if necessary
    max_text_width = text_box_width - 20  # Leave padding
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        text_size = cv2.getTextSize(test_line, font, font_scale, font_thickness)[0]

        if text_size[0] < max_text_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)  # Add the last line

    # Calculate text block height
    line_height = cv2.getTextSize("Test", font, font_scale, font_thickness)[0][1] + 10
    text_block_height = len(lines) * line_height + 20  # Extra padding

    # Create a new image with extra width for the text
    new_image = np.zeros((img_height, img_width + text_box_width, 3), dtype=np.uint8)
    new_image[:, :img_width, :] = image  # Copy original image to the left

    # Draw text background rectangle
    cv2.rectangle(new_image, (img_width, 0), (img_width + text_box_width, img_height), bg_color, -1)

    # Write the text on the right side
    y_offset = 20  # Start text near the top
    x_offset = img_width + 10  # Start text within the new area

    for line in lines:
        cv2.putText(new_image, line, (x_offset, y_offset), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
        y_offset += line_height  # Move to next line

    # Save the new image
    cv2.imwrite(output_img, new_image)
    print(f"Image saved with text on the right: {output_img}")


if __name__ == "__main__":
    # Check output file
    output_file = "results/resultado.json"
    if check_output_file(output_file):
        # Read the JSON file as a dictionary
        with open(output_file, "r") as file:
            json_data = json.load(file)
        # Sample an item from json
        sample = random.sample(list(json_data.items()), 1)[0]

        # Call function to produce an image with text
        image_path = "images/" + sample[0]
        text = sample[1]
        output_img = "results/sample_result.png"
        produce_result_sample(image_path, text, output_img)
