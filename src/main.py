import argparse
import json
import logging
import time

import openai

from utils import list_images, check_output_file
from client import vision_api_call

from tqdm import tqdm

# Configure logging to print to console and save to file
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler("log.txt", mode="w")
file_handler.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def main(folder: str, prompt: str, output: str, limit_batch_size: int):
    """
    Main file to run a batch of api calls to openai's vision API.
    This function reads images from a folder, sends them to the vision API
    and saves the results in a JSON file.

    Inputs:
        folder (str): The path to the folder containing the images
        prompt (str): The prompt to be sent to the model
        output (str): The name of the output file
        limit_batch_size (int): The maximum number of images to send in a batch
    
    Output:
        Generates a JSON file with the results of the API calls
    """

    logger.info("Iniciando o processamento de imagens")

    assert output.endswith(".json"), \
        logger.error("O arquivo de saída deve ser um arquivo JSON")

    logger.info(f"Processando imagens na pasta {folder}")

    # Read images from the folder
    images = list_images(folder)

    logger.info(f"Encontradas {len(images)} imagens")

    # Initialize the OpenAI client
    client = openai.OpenAI()

    logger.info("Inicializado o cliente OpenAI")

    # Initialize the results dictionary
    results = {}

    # Compute the time taken for batch inference
    start = time.time()

    # Loop through the images
    for img in tqdm(images[:limit_batch_size]):
        # Call the vision API
        response = vision_api_call(client, folder + img, prompt)

        # Check each image and response
        logger.debug(f"Imagem {img} processada")
        logger.debug(f"Resposta: {response}")

        # Save the response
        results[img] = response

    # Compute the time taken for batch inference
    logger.info(f"Tempo total de inferência: {time.time() - start:.2f} segundos")

    # Check dictionary results
    logger.debug(f"Resultados: {results}")

    # Salvar os resultados
    with open(output, "w", encoding="utf-8") as output_file:
        json.dump(results, output_file, ensure_ascii=False)

    # Assert that the output file was created
    if check_output_file(output):
        logger.info(f"Resultados salvos em {output}")
    else:
        logger.error("Erro ao salvar os resultados")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--folder",
        type=str,
        help="Caminho para a pasta de imagens",
        required=False,
        default="images/")
    
    parser.add_argument(
        "--prompt",
        type=str,
        help="Prompt para a descrição das imagens",
        required=False,
        default="Descreva apenas a vestimenta presente na imagem")
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="Nome do arquivo de saída",
        required=False,
        default="resultado.json")
    
    parser.add_argument(
        "--batch-size",
        type=int,
        help="Quantidade máxima de imagens para processar",
        required=False,
        default=1000)
    
    args = parser.parse_args()

    main(args.folder, args.prompt,
         args.output_file, args.batch_size)

