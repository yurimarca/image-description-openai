import openai
import argparse

def main(folder: str, prompt: str, output: str):
    # Read Images

    # Salvar os resultados
    with open(output, "w") as output_file:
        json.dump(results, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder",
        type=str,
        help="Caminho para a pasta de imagens",
        required=False)
    parser.add_argument(
        "--prompt",
        type=str,
        help="Prompt para a descrição das imagens",
        required=False)
    parser.add_argument(
        "--output",
        type=str,
        help="Nome do arquivo de saída",
        required=False)
    args = parser.parse_args()

