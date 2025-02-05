import base64
import os

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
    
    Args:
        filename (str): Nome do arquivo
    
    Returns:
        bool: True se o arquivo for uma imagem válida, False caso contrário.
    """

    valid_extensions = {".png", ".jpeg", ".jpg", ".webp", ".gif"}
    ext = os.path.splitext(filename)[1].lower()
    return ext in valid_extensions

def list_images(folder: str) -> list:
    """
    List all images in a folder.
    Reference: https://platform.openai.com/docs/guides/vision
    
    Args:
        folder (str): Folder path
    
    Returns:
        list: list of image files in the folder
    """
    return [f for f in os.listdir(folder) if is_valid_image(f)]