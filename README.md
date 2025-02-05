# Descrição de Imagens com API OpenAI

## Desafio Técnico

O objetivo deste projeto é desenvolver um sistema que gera descrições detalhadas de roupas contidas em imagens, utilizando a API da OpenAI. A aplicação lê imagens de uma pasta designada, envia cada imagem juntamente com um prompt customizado para a API, e retorna a descrição gerada para cada imagem. O sistema gera um artefato de saída no formato JSON que relaciona o nome dos arquivos das imagens com a descrição produzida através da chamada de API da OpenAI.


## Estrutura do Projeto

```
image-description-openai/
├── images/                # Pasta possui diversas imagens para teste da API
├── results/               # Pasta destinada aos arquivos de saída do sistema
│   ├── log.txt            # Arquivo log gerado ao realizar o batch image processing
│   ├── resultado.json     # Arquivo JSON com os resultados das descrições geradas
│   └── sample_result.png  # Amostra do resultado para descrição de vestimenta
├── src/                   # Código fonte do projeto
│   ├── client.py          # Módulo com funções para realizar chamadas para API
│   ├── main.py            # Script principal que processa uma batch de imagens
│   └── utils.py           # Funções utilitárias para manipulação de imagens e arquivos
└── requirements.txt   	   # Dependências do projeto
```

## Como Executar

### 1. **Instalar as Dependências**

   - Em um computador Linux, crie um ambiente virtual Python e instale as dependências via `pip`:
	   ```sh
	   python -m venv openai_venv
	   source openai_venv/bin/activate

	   pip install -r requirements.txt
	   ```

### 2. **Configurar a Chave da API**

   - Certifique-se de configurar a variável de ambiente com chave da API da OpenAI:
	   ```sh
	   export OPENAI_API_KEY='sua-chave-aqui'
	   ```
   - Esta configuração é necessária a cada inicialização do sistema. Para certificar-se que a chave estará sempre instanciada de forma segura, podemos simplemente adiciona-la na nossa inicialização do shell. Segue uma  [Referência](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) que utiliza o `zsh`:
   
		- O comando a seguir adiciona a API key ao arquivo ~/.zshrc, que é carregado automaticamente sempre que um novo terminal com zsh é iniciado. Isso significa que a variável de ambiente OPENAI_API_KEY estará disponível em todas as sessões futuras do shell.
		   ```sh
		   echo "export OPENAI_API_KEY='sua-chave-aqui'" >> ~/.zshrc
		   ```
		- Atualize o shell com a nova variável:
		   ```sh
		   source ~/.zshrc
		   ```
		- Confirme que a variável de ambiente foi definida corretamente:  
		   ```sh
		   echo $OPENAI_API_KEY
		   ```

### 3. **Batch Processamento de Imagens**

- Para processar uma pasta inteira de imagens e salvar os resultados em um arquivo JSON:

	```sh
	python src/main.py --folder images/ \
			--prompt "Descreva a roupa na imagem." \
			--output results/resultado.json \
			--batch-size 10
	```
- Ou simplesmente utilize os argumentos default:

	```sh
	python src/main.py
	```
	
### 4. **Testar a API call**

- É possível testar a chamada à API usando o `client.py`:
   ```sh
   python src/client.py --img-path "images/Gen AI Test_imagens_-2015-Women-two-pieces-set-summer-jumpsuit-solid-Lace-stitching-tassel-backless-hollow-out-rompers.jpg_220x220.jpg" --prompt "Descreva a roupa na imagem."
   ```

### 5. **Amostragem Visual dos Resultados**

- É possível chamar a função `utils.py` para gerar um sample dos resultados através de uma apresentação visual. **Note:** This assumes the folder `results/` exists and contains the file `resultado.json`
	```sh
	python src/utils.py
	```
	
- **Exemplo:**

	![sample_result](results/sample_result.png)

## Design e Estratégia de Desenvolvimento

Iniciei o projeto acessando a documentação da OpenAI para rapidamente produzir uma função Python em `client.py` que realizasse chamadas à API com prompts customizados. Esse foi o primeiro passo de implementação: analisar a documentação, configurar o ambiente Python com os pacotes necessários, configurar a chave da API e criar um código simples para testar a conexão com a API.

Com essa base inicial, planejei três fases de desenvolvimento, todas realizadas na branch `developing`, com cada fase resultando em um Pull Request (PR):

1. **Ler imagens e enviá-las via API Vision (PR: API Vision successful call)**	
2. **Processamento e inferência das imagens em batches (PR: Batch API Processing and Sample Image Result);**
3. **Paralelizar chamadas à API para um processamento mais rápido e escalável.**
	
Os PRs seguiram a seguinte sequência:

### 1. API Vision successful call
Implementei uma chamada à API Vision no `client.py` e criei um novo arquivo `utils.py` para lidar com o encoding das imagens e outras funções auxiliares. Aqui, foi possível rodar `python client.py` passando o prompt e o caminho da imagem para obter uma resposta da LLM.

### 2. Batch API Processing and Sample Image Result
Criei o `main.py`, responsável por processar todas as imagens de um diretório, fazer chamadas à API Vision para cada uma e gerar um arquivo JSON que associa os nomes das imagens às respostas da API. Para facilitar a verificação da qualidade das respostas, implementei uma função usando OpenCV com a ajuda de uma LLM para gerar imagens contendo a imagem original e a descrição gerada.

Vale ressaltar que este processamento em batch apenas realiza chamadas sequenciais à API e não corresponde ao [batch processing da OpenAI](https://platform.openai.com/docs/guides/batch), que permite enviar várias chamadas ao mesmo tempo e recuperar os resultados depois com melhor custo.

### 3. Paralelização das Chamadas à API (Não Implementado)
Por limitação de tempo, essa fase não foi implementada, mas a OpenAI fornece materiais úteis para isso:
- [Exemplo de paralelização de chamadas assíncronas](https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py), que poderia ser utilizado para otimizar o tempo de inferência do projeto.
- [Guia de como lidar com limitações de taxa da API](https://cookbook.openai.com/examples/how_to_handle_rate_limits), essencial para garantir escalabilidade consistente.

## Melhores Práticas para Desenvolvimento e Deployment

Outras boas práticas para deploy e desenvolvimento incluem:

- **Tratamento de Erros**: Algumas tratativas de erros foram implementados no projeto, mas esse aspecto pode ser melhorado. Com relação as chamadas de API da OpenAI, poderíamos considerar a [referência de códigos de erro](https://platform.openai.com/docs/guides/error-codes) para lidar com diferentes falhas de forma mais eficiente.
- **Legibilidade do Código**: Ferramentas como `pylint` e `autopep8` garantem conformidade com os padrões Python. O `pylint` também pode ser integrado em pipelines de Continuous Integration (CI) no GitHub Actions.
- **Testes Unitários**: Para melhorar a confiabilidade, testes unitários devem ser adicionados usando `pytest`, que também poderia ser utilizado no CI com o GitHub Actions.

Essa abordagem garantiu um desenvolvimento estruturado e modularizado, possibilitando expansão futura para otimizações de performance e escalabilidade.

## Outras Considerações

- **Data Leakage**: Ao notar que o nome dos arquivos das imagens contém uma descrição em inglês correspondente ao que é solicitado via prompt para a LLM, devemos tomar cuidado com o vazamento dessa informação para o modelo. Como fazemos o encoding da imagem e esta é passada para a LLM, não corremos o risco de data leakage diretamente. 

- **Método para Avaliação do Prompt**: Essa informação presente no nome dos arquivos poderia ser utilizada como label das imagens, possibilitando o cálculo de uma métrica de desempenho da LLM. Isso permitiria a exploração de prompts alternativos que possam gerar respostas mais precisas. Ferramentas de MLOps, como o MLflow, poderiam ser utilizadas para rastrear esses experimentos na busca por uma melhor performance do modelo. Além disso, o MLflow facilitaria o deployment dessas soluções.

