# Descrição de Imagens com API OpenAI

## Desafio Técnico

O objetivo deste projeto é desenvolver um sistema que gera descrições detalhadas de roupas contidas em imagens, utilizando a API da OpenAI. A aplicação lê imagens de uma pasta designada, envia cada imagem juntamente com um prompt customizado para a API, e retorna a descrição gerada para cada imagem. 

## Estrutura do Projeto

```
image-description-openai/
├── client.py          # Módulo para estabelecer a conexão com a API da OpenAI
├── main.py            # Script principal que processa uma batch de imagens
├── utils.py           # Funções utilitárias para manipulação de imagens e arquivos
└── requirements.txt   # Dependências do projeto
```

## Como Executar

1. **Instalar as Dependências:**

   - Em um computador Linux, crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate

   pip install -r requirements.txt
   ```

2. **Configurar a Chave da API:**

   - Certifique-se de configurar a variável de ambiente com chave da API da OpenAI:
   ```bash
   export OPENAI_API_KEY='sua-chave-aqui'
   ```

3. **Testar a API com um Único Arquivo:**

   - Você pode testar a chamada à API usando o `client.py`:
   ```bash
   python client.py --img-path "images/Gen AI Test_imagens_-2015-Women-two-pieces-set-summer-jumpsuit-solid-Lace-stitching-tassel-backless-hollow-out-rompers.jpg_220x220.jpg" --prompt "Descreva a roupa na imagem."
   ```

4. **Batch de Imagens:**

   - Para processar uma pasta inteira de imagens e salvar os resultados em um arquivo JSON:
   ```bash
   python main.py --folder images/ --prompt "Descreva a roupa na imagem." --output resultados.json --batch-size 10
   ```
	
	- Ou simplesmente:
	```bash
   python main.py
	```


5. **Amostragem Visual dos Resultados**

	- E possivel chamar a funcao `utils.py` para gerar um sample dos resultados atraves de uma apresentacao visual.
	```bash
	python utils.py
	```
	- **Exemplo:**

	![sample_result](sample_result.png)

## Comments:

- Data lekeage through image file names.
- Image file names can give us a label for testing multiple prompts.
- Prompt testing could be optimized with mlflow, which would also facilitate scalable deployment.
- Challenge should be to focus on the reply being only related with the clothes with precision detail.