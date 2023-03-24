<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/examples/01-header-examples.png?raw=true" alt="terraglue-logo">
</div>


## Table of Contents
- [Table of Contents](#table-of-contents)
- [Cenário 1: implementando seu próprio conjunto de dados](#cenário-1-implementando-seu-próprio-conjunto-de-dados)
  - [Sobre os dados de exemplo (Brazilian E-Commerce)](#sobre-os-dados-de-exemplo-brazilian-e-commerce)
  - [Utilizando dados próprios](#utilizando-dados-próprios)
  - [Visualizando efeitos na conta AWS](#visualizando-efeitos-na-conta-aws)
- [Cenário 2: implementando seu próprio job do Glue](#cenário-2-implementando-seu-próprio-job-do-glue)
  - [Etapas para adaptação da aplicação](#etapas-para-adaptação-da-aplicação)
  - [Alterando parâmetros do job](#alterando-parâmetros-do-job)
  - [Modificando o dicionário DATA\_DICT](#modificando-o-dicionário-data_dict)
  - [Codificando novos métodos de transformação](#codificando-novos-métodos-de-transformação)
  - [Sequenciando passos no método run()](#sequenciando-passos-no-método-run)
  - [Visualizando resultados](#visualizando-resultados)
- [Continue navegando nas documentações](#continue-navegando-nas-documentações)

___

## Cenário 1: implementando seu próprio conjunto de dados

Considerando que o usuário, neste momento da jornada de consumo da documentação, tem uma noção básica sobre o funcionamento do **terraglue** como produto, o primeiro cenário de utilização prática a ser exemplificado envolve a adaptação da solução para ingestão e catalogação de bases próprias a serem utilizadas, posteriormente, como insumos de jobs Glue a serem programados.

Este tipo de adaptação é fundamentalmente importante aos usuários de todos os níveis pois, a partir dela, é possível:

- 🎲 Utilizar amostras de bases produtivas para validações e testes na AWS
- 🕹️ Simular um cenário de desenvolvimento próximo daquele encontrado em ambientes produtivos
- 🧙‍♂️ Acelerar o processo de desenvolvimento de *jobs* a partir do entendimento e utilização de amostras próprias de dados
- 🔍 Executar consultas *ad-hoc* em dados catalogados automaticamente

Antes de iniciar o processo de adaptação da solução para uso de dados próprios, é preciso entender um pouco mais sobre os dados originalmente disponibilizados no repositório.

### Sobre os dados de exemplo (Brazilian E-Commerce)

Antes de iniciar as discussões desta seção, é imprescindível abordar, de forma resumida, alguns detalhes sobre o conjunto de dados fornecido por padrão no repositório: trata-se de bases que contemplam o famoso dataset [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Originalmente disponível na plataforma [Kaggle](https://www.kaggle.com/), o referido conjunto contempla dados de vendas online no *e-commerce* brasileiro separados em diferentes arquivos de texto, cada um em seu respectivo domínio. Juntos, os arquivos podem ser utilizados e trabalhados para retirar os mais variados *insights* relacionados ao comércio online.

<details>
  <summary>🎲 Clique para visualizar o schema original dos dados</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/examples/examples-cenario03-schema-br-ecommerce.png?raw=true" alt="br-ecommerce-schema">
</div>
</details>

Visando proporcionar uma maior simplicidade no exemplo de geração de SoT, apenas alguns arquivos do conjunto de dados Brazilian E-Commerce foram selecionados como SoRs do projeto, sendo eles:

| 🗂️ **Arquivo** | 📝 **Descrição** |
| :-- | :-- |
| `orders.csv` | Contempla dados de pedidos realizados online |
| `customers.csv` | Contempla dados cadastrais dos clientes que realizaram os pedidos online |
| `payments.csv` | Contempla dados dos pagamentos utilizados para quitação dos pedidos realizados |
| `reviews.csv` | Contempla dados das revisões, nota e comentários deixados por clientes para os pedidos realizados |
| `geolocation.csv` | Contempla dados demográficos de pedidos realizados online |
| `order_items.csv` | Traz uma visão de cada item presente em cada um dos pedidos |
| `products.csv` | Contempla uma visão categórica dos produtos/itens presentes nos pedidos |
| `sellers.csv` | Traz uma visão categóricas dos vendedores |

Assim, os conjuntos citados então são disponibilizados localmente em uma estrutura hierárquica de pastas que simula uma organização de dados em um ambiente Data Lake no formato `db/tbl/file`, sendo esta uma dinâmica **mandatória** para o sucesso de implantação de conjuntos próprios de dados.

### Utilizando dados próprios

Conhecidos os arquivos que fazem parte do repositório em seu modo natural, o usuário agora poderá adaptar todo o processo de ingestão e catalogação proporcionado no **terraglue** para seus próprios conjuntos.

Em um primeiro momento, é extremamente ressaltar algumas premissas e limitações do processo de catalogação de dados no Data Catalog da conta AWS:

1. Somente arquivos `csv` poderão ser utilizados
2. Os arquivos `csv` devem possuir o *header* na primeira linha
3. A estrutura hierárquica deve seguir o modelo `db/tbl/file` a partir do diretório `data/` do repositório

> 🚨 Avaliar as premissas acima é de suma importância pois, em seus detalhes técnicos de construção, o **terraglue** considera a aplicação de funções do Terraform para iterar sobre os diretórios presentes em `data/`, realizar a leitura da primeira linha dos arquivos CSV para extração dos atributos e catalogação no Data Catalog. Sem o cumprimento das premissas, as funções do Terraform irão retornar erro e o fluxo não será implantado conforme esperado pelo usuário. Para maiores detalhes, consulte a documentação da função [fileset()](https://developer.hashicorp.com/terraform/language/functions/fileset) do Terraform.

Endereçado este ponto, os exemplos ilustrados a seguir simulam a obtenção de novos conjuntos de dados a serem utilizados no processo de ingestão e catalogação em substituição aos dados originais do dataset Brazilian E-Commerce fornecidos como padrão.

Como um primeiro passo, o usuário pode navegar até o repositório do **terraglue** clonado localmente e executar o comando abaixo para remover todo o contéudo presente em `data/` no repositório do projeto. Também é possível excluir os arquivos e diretórios manualmente, se preferir.

```bash
# Removendo todos os arquivos de /data
rm -r data/*
```

Com o diretório `/data` agora vazio, basta obter os novos dados a serem utilizados e organizá-los na estrutura adequada. Como exemplo, utilizarei dados do [naufrágio do Titanic](https://www.kaggle.com/competitions/titanic/data) previamente baixados e armazenados no diretório `~/Downloads` com o nome `titanic.csv`. Antes de realizar a movimentação do arquivo, é importante criar toda a estrutura de pastas locais que simulam a organização de um Data Lake a ser replicado no S3 durante o processo de implantação do **terraglue**. O nome do *database* será escolhido aleatoriamente.

```bash
# Criando estrutura de pastas locais
mkdir -p data/tt3/tbl_titanic_data
```

Onde `tt3` é o nome fictício para o *database* e `tbl_titanic_data` o nome escolhido para a tabela. Com isso, é possível movimentar o arquivo desejado para a estrutura criada.

```bash
# Movendo arquivo
mv ~/Downloads/titanic.csv data/tt3/tbl_titanic_data/
```

Validado que o novo arquivo já consta organizado localmente na estrutura necessária, bastas executar os procedimentos de implantação do **terraglue** através do comando `terraform apply` para implementar todos os processos atrelados.

### Visualizando efeitos na conta AWS

Uma vez obtido e organizado o(s) novo(s) conjunto(s) de dado(s) a serem inseridos junto com os processos de implantação do **terraglue**, o usuário poderá acessar o S3 para avaliar o sucesso de ingestão dos novos dados dentro do bucket `terraglue-sor`. Na imagem abaixo, é possível verificar que o conjunto de dados `titanic.csv` foi inserido com sucesso com o prefixo `tt3/tbl_titanic_data`, assim como o esperado.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/examples/examples-cenario03-titanic-data-on-s3.PNG?raw=true" alt="titanic-data-on-s3">
</div>
</details>

Além disso, é possível também acessar o serviço Glue e, dentro do menu Data Catalog, validar se o arquivo inserido no S3 também passou pelo processo de catalogação. Na imagem abaixo, é possível verificar que uma entrada no catálogo foi automaticamente criada para os dados do Titanic recém disponibilizados:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/examples/examples-cenario03-titanic-data-on-data-catalog.PNG?raw=true" alt="titanic-data-on-data-catalog">
</div>
</details>

Ao selecionar a tabela no catálogo, será ainda possível perceber que todo o processo de obtenção de atributos pôde ser realizado com sucesso. Essa afirmação tem como base o próprio *schema* da tabela presente no catálogo:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/examples/examples-cenario03-titanic-schema-on-catalog.PNG?raw=true" alt="titanic-schema-on-data-catalog">
</div>
</details>

Por fim, a validação final realizada envolve o acesso ao serviço Athena para execução de uma simples *query* para extração dos dados recém catalogados. A imagem abaixo exemplifica a retirada de 10 registros da base através do comando `SELECT * FROM tt3.tbl_titanic_data LIMIT 10;`:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/examples/examples-cenario03-titanic-data-on-athena.PNG?raw=true" alt="titanic-data-on-athena">
</div>
</details>

Com isso, é possível validar que todo o processo de adaptação do **terraglue** para uso de novas bases de dados em substituição aos dados de e-commerce fornecidos por padrão pode ser tranquilamente realizado.

___

## Cenário 2: implementando seu próprio job do Glue

O segundo cenário de exemplos práticos fornecidos envolve a adaptação do script principal `main.py`, fornecido como padrão para processamento de dados do E-Commerce Brasileiro, de acordo com necessidades específicas do usuário. Visando seguir uma linha sequencial, o processo de adaptação da aplicação a ser exemplificado considera a utilização dos dados do Titanic ingeridos e catalogados na exemplificação do [cenário 1 de adaptação de dados](#cenário-1-implementando-seu-próprio-conjunto-de-dados) previamente abordado.

Como também detalhado na [documentação específica sobre a aplicação Spark](https://github.com/ThiagoPanini/terraglue/blob/main/APP.md) entregue ao usuário, existem algumas etapas importantes a serem seguidas para garantir a extração do maior valor possível de toda a dinâmica entregue pelo **terraglue**. Compreender o processo de adaptação do script principal de trabalho pode proporcionar as seguintes vantagens ao usuário:

- ⚗️ Implantar e testar jobs próprios do Glue em um ambiente de desenvolvimento
- 🔬 Validar regras de transformação codificadas para geração de tabelas SoT e Spec
- 🔧 Iterar sobre as regras estabelecidas e se as visões geradas são realmente as esperadas

### Etapas para adaptação da aplicação

Para o usuário que inseriu novos dados e deseja codificar suas próprias transformações para testar, validar ou simplesmente entender como um *job* Glue funciona, a lista de tópicos abaixo pode servir como um simples resumo das operações necessárias:

<details>
  <summary>1. Analisar e modificar, se necessário, a variável <code>ARGV_LIST</code> presente no script principal para mapear e coletar possíveis novos parâmetros do job inseridos pelo usuário</summary>
  
  > O processo de inclusão de novos parâmetros pode ser feito através da variável Terraform `glue_job_user_arguments` presente no arquivo `./infra/variables.tf`.
</div>
</details>

<details>
  <summary>2. Modificar, em caso de inclusão de novos dados, a variável <code>DATA_DICT</code> com todas as informações necessárias para leitura dos dados a serem trabalhados</summary>

  > Para este processo, todos os argumentos do método `glueContext.create_dynamic_frame.from_catalog()` são aceitos.
</div>
</details>

<details>
  <summary>3. Codificar novos métodos de transformação na classe <code>GlueTransformationManager</code> de acordo com as regras de negócio a serem aplicadas na geração das novas tabelas</summary>

  > Para fins de organização, os métodos de transformação fornecidos como padrão iniciam com o prefixo "transform_". São esses os métodos que devem ser substituídos para o novo processo de ETL codificado.
</div>
</details>

<details>
  <summary>4. Modificar o método <code>run()</code> da classe `GlueTransformationManager` de acordo com a nova sequênciad e passos necessários até o alcance do objetivo final do job</summary>

  > Aqui, o usuário poderá utilizar todos os métodos presentes no script principal e no módulo `terraglue.py` para coordenar todos os passos e etapas do processo de ETL, desde a leitura dos dados até a escrita e catalogação dos mesmos.
</div>
</details>

### Alterando parâmetros do job

Como um primeiro passo rumo ao processo de adaptação da aplicação Spark proporcionada pelo **terraglue**, é importante garantir que todos os parâmetros do job do Glue estão devidamente configurados. Existem diferentes formas de se fazer essa validação, seja alterando diretamente os valores no template de IaC considerado ou mesmo indo manualmente até o AWS Management Console da conta de *sandbox* ou de desenvolvimento.

Nessa demonstração, será proposta a alteração dos seguintes parâmetros diretamente nos módulos Terraform disponibilizados no projeto:

- Nome do job do Glue através da variável `glue_job_name`
- Parâmetros `--OUTPUT_DB` e `--OUTPUT_TABLE` através da variável `glue_job_user_arguments`

Para isso, basta acessar o arquivo `variables.tf` no módulo *root*, procurar pelas variáveis acima citadas e, enfim, aplicar as modificações desejadas. Visando proporcionar um exemplo prático desta modificação, o bloco abaixo contém propostas de um novo nome para o *job* modificado, bem como para novos parâmetros de saída do banco de dados e da tabela resultante:

<details>
  <summary>🍃 Variáveis glue_job_name e glue_job_user_arguments do arquivo variables.tf no módulo root </summary>

```
variable "glue_job_name" {
  description = "Nome ou referência do job do glue a ser criado"
  type        = string
  default     = "gluejob-sot-titanic"
}

[...]

variable "glue_job_user_arguments" {
  description = "Conjunto de argumentos personalizados do usuário a serem associados ao job do glue"
  type        = map(string)
  default = {
    "--OUTPUT_DB"             = "tt3"
    "--OUTPUT_TABLE"          = "tbsot_titanic"
    "--CONNECTION_TYPE"       = "s3"
    "--UPDATE_BEHAVIOR"       = "UPDATE_IN_DATABASE"
    "--PARTITION_NAME"        = "anomesdia"
    "--PARTITION_FORMAT"      = "%Y%m%d"
    "--DATA_FORMAT"           = "parquet"
    "--COMPRESSION"           = "snappy"
    "--ENABLE_UPDATE_CATALOG" = "True"
  }
}
```
</details>

Dessa forma, ao executar o comando `terraform apply`, o usuário poderá ter em mãos um job com a nomenclatura correta e com os parâmetros configurados de maneira a proporcionar a escrita de uma tabela totalmente nova.

### Modificando o dicionário DATA_DICT

Reforçando a consideração de que os novos dados a serem trabalhados nesta adaptação do script principal foram previamente inseridos e catalogados no [exemplo de cenário anterior](#cenário-1-implementando-seu-próprio-conjunto-de-dados), o início do nosso processo de adaptação envolve modificar a variável `DATA_DICT` no script `main.py` para inserir os parâmetros de leitura da tabela do Titanic presente agora no processo. Dessa forma, a nova variável é dada por:

```python
# Definindo dicionário para mapeamento dos dados
DATA_DICT = {
    "titanic": {
        "database": "tt3",
        "table_name": "tbl_titanic_data",
        "transformation_ctx": "dyf_titanic",
        "create_temp_view": True
    }
}
```

Os valores inseridos na variável `DATA_DICT` correspondem às entradas existentes no catálogo de dados para a dada tabela. Como estamos realizando a leitura de apenas uma origem, o dicionário é composto apenas por uma chave.

### Codificando novos métodos de transformação

Agora que o dicionário de mapeamento de leitura de dados está devidamente configurado, vamos estabelecer um objetivo final para garantir que as inclusões dos métodos de transformação da classe `GlueTransformationManager` tenham um propósito claro. Antes de formalizar uma proposta, é importante ter uma visão prévia sobre os dados atualmente disponíveis:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://raw.githubusercontent.com/ThiagoPanini/terraglue/develop/docs/imgs/examples/terraglue-examples-titanic-data.png" alt="titanic-data-athena">
</div>
</details>

Considerando o conteúdo da base Titanic presente, a proposta de transformação poderia envolver:

- Transformação de tipos primitivos das colunas de acordo com o significado de cada campo
- Extração do "título" da pessoa (Mr ou Mrs) através da coluna *name*
- Extração da "classe da cabine" (A, B ou C) através da coluna *cabin*
- Criação de categoria de idade para separação da coluna *age* em faixas
- Criação de categoria de ganhos para separação da coluna *fare* em faixas
- Extração do "tamanho da família" através da soma das colunas *parch* e *sibsp*

Assim, a classe `GlueTransformationManager` pode conter então o método `transform_titanic()` seguindo as transformações mapeadas através do seguinte código:

```python
# Método de transformação: payments
def transform_titanic(self, df: DataFrame) -> DataFrame:
    logger.info("Preparando DAG de transformações para a base titanic")
    try:
        # Selecionando e transformando atributos
        df_titanic_select = df.selectExpr(
            "cast(passengerid AS INT) AS id_passageiro",
            "cast(survived AS INT) AS flag_sobrevivencia",
            "cast(pclass AS INT) AS classe_passageiro",
            "name AS nome_passageiro",
            "sex AS genero_passageiro",
            "cast(age AS INT) AS idade_passageiro",
            "cast(sibsp AS INT) AS qtd_irmaos_ou_conjuges",
            "cast(parch AS INT) AS qtd_pais_ou_criancas",
            "ticket",
            "cast(fare AS DECIMAL(17,2)) AS vlr_ticket_pago",
            "cabin AS cabine_passageiro",
            "embarked AS codigo_porto_embarque"
        )

        # Criando atributos adicionais
        df_titanic_prep = df_titanic_select.selectExpr(
            "*",
            "regexp_extract(nome_passageiro, '([a-zA-Z]+\.)') AS titulo_passageiro",
            "lpad(cabine_passageiro, 1, ' ') AS classe_cabine_passageiro,"
            "case\
                when idade_passageiro <= 10 then '0_10'\
                when idade_passageiro <= 20 then '10_20'\
                when idade_passageiro <= 40 then '20_40'\
                when idade_passageiro <= 60 then '40_60'\
                when idade_passageiro > 60 then 'maior_60'\
                else null\
            end AS categoria_idade",
            "case\
                when vlr_ticket_pago <= 8 then '0_8'\
                when vlr_ticket_pago <= 15 then '8_15'\
                when vlr_ticket_pago <= 25 then '15_25'\
                when vlr_ticket_pago <= 50 then '25_50'\
                when vlr_ticket_pago > 50 then 'maior_50'\
                else null\
            end AS categoria_vlr_ticket",
            "qtd_irmaos_ou_conjuges + qtd_pais_ou_criancas + 1 AS tamanho_da_familia"
        )

        # Retornando DataFrame preparado
        return df_titanic_prep

    except Exception as e:
        logger.error("Erro ao preparar DAG de transformações para dados "
                      f"do Titanic. Exception: {e}")
        raise e
```

### Sequenciando passos no método run()

Uma vez preparado o método de transformação dos dados do Titanic utilizando `pyspark`, podemos navegar pelo método `run()` e mapear todos os passos necessários para sequenciamento das etapas. Considerando os objetivos propostos, queremos:

1. Realizar a leitura da base de dados em um DataFrame Spark
2. Aplicar o método de transformação codificado de modo a gerar um DataFrame transformado
3. Gerenciar partições (eliminar existente e adicionar nova com base em data de execução)
4. Escrever a tabela resultante no S3 e realizar a catalogação no Data Catalog

Com os passos mapeados acima, o método `run()` pode ser escrito como:

```python
# Encapsulando método único para execução do job
def run(self) -> None:
    # Preparando insumos do job
    job = self.init_job()

    # Lendo DynamicFrames e transformando em DataFrames Spark
    dfs_dict = self.generate_dataframes_dict()

    # Separando DataFrames em variáveis
    df_titanic = dfs_dict["titanic"]

    # Transformando dados
    df_titanic_prep = self.transform_titanic(df=df_titanic)

    # Criando variável de partição
    partition_value = int(datetime.now().strftime(
        self.args["PARTITION_FORMAT"]
    ))

    # Removendo partição física do S3
    self.drop_partition(
        partition_name=self.args["PARTITION_NAME"],
        partition_value=partition_value
    )

    # Adicionando coluna de partição ao DataFrame
    df_titanic_prep_partitioned = self.add_partition(
        df=df_titanic_prep,
        partition_name=self.args["PARTITION_NAME"],
        partition_value=partition_value
    )

    # Escrevendo e catalogando dados
    self.write_data_to_catalog(df=df_titanic_prep_partitioned)

    # Commitando job
    job.commit()
```

Caso queira visualizar o script completo, basta expandir o bloco abaixo.

<details>
  <summary>🐍 Script main.py completo após as modificações</summary>

```python
"""
JOB: main.py

CONTEXTO:
---------
Script principal da aplicação Spark implantada como job do
Glue dentro dos contextos estabelecidos pelo processo de
ETL a ser programado.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Bibliotecas utilizadas na construção do módulo
from datetime import datetime
from pyspark.sql import DataFrame
from terraglue import GlueETLManager, log_config


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.2 Definindo variáveis da aplicação
---------------------------------------------------"""

# Configurando objeto de log
logger = log_config(logger_name=__file__)

# Argumentos do job
ARGV_LIST = [
    "JOB_NAME",
    "OUTPUT_BUCKET",
    "OUTPUT_DB",
    "OUTPUT_TABLE",
    "CONNECTION_TYPE",
    "UPDATE_BEHAVIOR",
    "PARTITION_NAME",
    "PARTITION_FORMAT",
    "DATA_FORMAT",
    "COMPRESSION",
    "ENABLE_UPDATE_CATALOG"
]

# Definindo dicionário para mapeamento dos dados
DATA_DICT = {
    "titanic": {
        "database": "tt3",
        "table_name": "tbl_titanic_data",
        "transformation_ctx": "dyf_titanic",
        "create_temp_view": True
    }
}


"""---------------------------------------------------
--------- 2. GERENCIAMENTO DE TRANSFORMAÇÕES ---------
            2.2 Definição de classe Python
---------------------------------------------------"""


class GlueTransformationManager(GlueETLManager):
    """
    Classe responsável por gerenciar e fornecer métodos típicos
    de transformação de um job do Glue a serem pontualmente
    adaptados por seus usuários para que as operações nos dados
    possam ser aplicadas de acordo com as necessidades exigidas.

    Em essência, essa classe herda os atributos e métodos da
    classe GlueETLManager existente no módulo terraglue.py,
    permitindo assim o acesso a todos os atributos e métodos
    necessários para inicialização e configuração de um job do Glue.
    Assim, basta que o usuário desenvolva os métodos de
    transformação adequados para seu processo de ETL e coordene
    a execução dos mesmos no método run() desta classe.

    Para maiores informações sobre os atributos, basta consultar
    a documentação das classes e métodos no módulo terraglue.py.
    """

    def __init__(self, argv_list: list, data_dict: dict) -> None:
        self.argv_list = argv_list
        self.data_dict = data_dict

        # Herdando atributos de classe de gerenciamento de job
        GlueETLManager.__init__(self, argv_list=self.argv_list,
                                data_dict=self.data_dict)

    # Método de transformação: payments
    def transform_titanic(self, df: DataFrame) -> DataFrame:
        """
        Método de transformação específico para uma das origens
        do job do Glue.

        Parâmetros
        ----------
        :param: df
            DataFrame Spark alvo das transformações aplicadas.
            [type: pyspark.sql.DataFrame]

        Retorno
        -------
        :return: df_prep
            Elemento do tipo DataFrame Spark após as transformações
            definidas pelos métodos aplicadas dentro da DAG.
            [type: DataFrame]
        """

        logger.info("Preparando DAG de transformações para a base titanic")
        try:
            # Selecionando e transformando atributos
            df_titanic_select = df.selectExpr(
                "cast(passengerid AS INT) AS id_passageiro",
                "cast(survived AS INT) AS flag_sobrevivencia",
                "cast(pclass AS INT) AS classe_passageiro",
                "name AS nome_passageiro",
                "sex AS genero_passageiro",
                "cast(age AS INT) AS idade_passageiro",
                "cast(sibsp AS INT) AS qtd_irmaos_ou_conjuges",
                "cast(parch AS INT) AS qtd_pais_ou_criancas",
                "ticket",
                "cast(fare AS DECIMAL(17,2)) AS vlr_ticket_pago",
                "cabin AS cabine_passageiro",
                "embarked AS codigo_porto_embarque"
            )

            # Criando atributos adicionais
            df_titanic_prep = df_titanic_select.selectExpr(
                "*",
                "regexp_extract(nome_passageiro, '([a-zA-Z]+\.)') AS titulo_passageiro",
                "lpad(cabine_passageiro, 1, ' ') AS classe_cabine_passageiro,"
                "case\
                    when idade_passageiro <= 10 then '0_10'\
                    when idade_passageiro <= 20 then '10_20'\
                    when idade_passageiro <= 40 then '20_40'\
                    when idade_passageiro <= 60 then '40_60'\
                    when idade_passageiro > 60 then 'maior_60'\
                    else null\
                end AS categoria_idade",
                "case\
                    when vlr_ticket_pago <= 8 then '0_8'\
                    when vlr_ticket_pago <= 15 then '8_15'\
                    when vlr_ticket_pago <= 25 then '15_25'\
                    when vlr_ticket_pago <= 50 then '25_50'\
                    when vlr_ticket_pago > 50 then 'maior_50'\
                    else null\
                end AS categoria_vlr_ticket",
                "qtd_irmaos_ou_conjuges + qtd_pais_ou_criancas + 1 AS tamanho_da_familia"
            )

            # Retornando DataFrame preparado
            return df_titanic_prep

        except Exception as e:
            logger.error("Erro ao preparar DAG de transformações para dados "
                        f"do Titanic. Exception: {e}")
            raise e

    # Encapsulando método único para execução do job
    def run(self) -> None:
        """
        Método responsável por consolidar todas as etapas de execução
        do job do Glue, permitindo assim uma maior facilidade e
        organização ao usuário final. Este método pode ser devidamente
        adaptado de acordo com as necessidades de cada usuário e de
        cada job a ser codificado, possibilitando uma centralização
        de todos os processos operacionais a serem realizados.
        Na prática, este método realiza as seguintes operações:

            1. Inicializa o job e obtém todos os insumos necessários
            2. Realiza a leitura dos objetos DataFrame/DynamicFrame
            3. Aplica as transformações necessárias
            4. Gerencia partições (elimina existente e adiciona uma nova)
            5. Escreve o resultado no s3 e cataloga no Data Catalog
        """

        # Preparando insumos do job
        job = self.init_job()

        # Lendo DynamicFrames e transformando em DataFrames Spark
        dfs_dict = self.generate_dataframes_dict()

        # Separando DataFrames em variáveis
        df_titanic = dfs_dict["titanic"]

        # Transformando dados
        df_titanic_prep = self.transform_titanic(df=df_titanic)

        # Criando variável de partição
        partition_value = int(datetime.now().strftime(
            self.args["PARTITION_FORMAT"]
        ))

        # Removendo partição física do S3
        self.drop_partition(
            partition_name=self.args["PARTITION_NAME"],
            partition_value=partition_value
        )

        # Adicionando coluna de partição ao DataFrame
        df_titanic_prep_partitioned = self.add_partition(
            df=df_titanic_prep,
            partition_name=self.args["PARTITION_NAME"],
            partition_value=partition_value
        )

        # Escrevendo e catalogando dados
        self.write_data_to_catalog(df=df_titanic_prep_partitioned)

        # Commitando job
        job.commit()


"""---------------------------------------------------
--------------- 4. PROGRAMA PRINCIPAL ----------------
        Execução do job a partir de classes
---------------------------------------------------"""

if __name__ == "__main__":

    # Inicializando objeto para gerenciar o job e as transformações
    glue_manager = GlueTransformationManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    # Executando todas as lógicas mapeadas do job
    glue_manager.run()
```

</details>


### Visualizando resultados

Após a completa adaptação do script e execução do job no Glue, o usuário terá em mãos uma nova tabela SoT (no exemplo, chamada `tbsot_titanic`) com novos dados disponíveis para uso.

Considerando a demonstração fornecida, seria possível acessar o serviço Athena e visualizar, logo de cara, uma nova entrada para a tabela gerada no database selecionado:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://raw.githubusercontent.com/ThiagoPanini/terraglue/develop/docs/imgs/examples/terraglue-examples-titanic-sot-athena.png" alt="titanic-data-athena-sot">
</div>
</details>

Para validar as transformações codificadas, o usuário poderia, ainda, executar a query abaixo para visualizar os novos dados disponíveis.

```sql
SELECT
    idade_passageiro,
    categoria_idade,
    vlr_ticket_pago,
    categoria_vlr_ticket,
    tamanho_da_familia,
    cabine_passageiro,
    classe_cabine_passageiro

FROM tt3.tbsot_titanic LIMIT 5;
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/examples/terraglue-examples-titanic-sot-athena-query.png?raw=true" alt="titanic-data-athena-sot-query">
</div>
</details>

E assim completamos o cenário de adaptação do script `main.py` para finalidades específicas de acordo com novos dados inseridos no processo!

___

## Continue navegando nas documentações

- [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main)
- [2. Implantando e conhecendo a infraestrutura](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md)
- [3. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/APP.md)
- 👉 [4. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/EXAMPLES.md) *Você está aqui!*
- [5. Testes unitários em jobs do Glue na AWS](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/TESTS.md)
