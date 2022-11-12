*Fornecendo exemplos práticos de cenários de utilização do projeto*

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Antes de começar](#antes-de-começar)
- [Cenário 1: um primeiro passo na análise dos recursos](#cenário-1-um-primeiro-passo-na-análise-dos-recursos)
  - [Buckets SoR, SoT, Spec e outros](#buckets-sor-sot-spec-e-outros)
  - [Dados na camada SoR](#dados-na-camada-sor)
  - [Catalogação no Data Catalog](#catalogação-no-data-catalog)
  - [Athena workgroup](#athena-workgroup)
  - [IAM policies e roles](#iam-policies-e-roles)
  - [Glue job](#glue-job)
  - [Dados na camada SoT](#dados-na-camada-sot)
- [Cenário 2: compreendendo detalhes de um job Spark no Glue](#cenário-2-compreendendo-detalhes-de-um-job-spark-no-glue)
  - [O script main-terraglue.py](#o-script-main-terragluepy)
  - [Classes GlueJobManager e GlueTransformationManager](#classes-gluejobmanager-e-gluetransformationmanager)
  - [Ações do usuário para utilizar e adaptar o script](#ações-do-usuário-para-utilizar-e-adaptar-o-script)
- [Cenário 3: implementando seu próprio conjunto de dados](#cenário-3-implementando-seu-próprio-conjunto-de-dados)
  - [Utilizando dados próprios](#utilizando-dados-próprios)
  - [Visualizando efeitos na conta AWS](#visualizando-efeitos-na-conta-aws)
- [Cenário 4: implementando seu próprio job do Glue](#cenário-4-implementando-seu-próprio-job-do-glue)
  - [Codificando novas transformações](#codificando-novas-transformações)
  - [Executando jobs próprios](#executando-jobs-próprios)
___

## Antes de começar

Antes de navegarmos por exemplos práticos de consumo, é importante garantir que todas as etapas de preparação e instalação foram cumpridas. Para maiores detalhes, o arquivo [GETTINGSTARTED.md](https://github.com/ThiagoPanini/terraglue/blob/develop/GETTINGSTARTED.md) contempla todo o processo necessário de iniciação.

Adicionalmente, é válido citar que esta documentação será separada em diferentes **cenários**, cada um trazendo à tona uma possível seara de aplicação do **terraglue** de acordo com um propósito específico. É importante destacar que os cenários contemplam desafios próprios e particulares, sendo direcionados para públicos específicos que podem se beneficiar das funcionalidades deste projeto. Encontre aquele que mais faça sentido dentro de sua jornada de aprendizado e mergulhe fundo!

| 🎬 **Cenário** | **🎯 Público alvo** |
| :-- | :-- |
| [#1 Um primeiro passo na análise dos recursos](#cenário-1-um-primeiro-passo-na-análise-dos-recursos) | Todos os usuários |
| [#2 Compreendendo detalhes de um job Spark no Glue](#cenário-2-compreendendo-detalhes-de-um-job-spark-no-glue) | Usuários com conhecimentos básicos |
| [#3 Implementando seu próprio conjunto de dados](#cenário-3-implementando-seu-próprio-conjunto-de-dados) | Usuários com conhecimentos intermediários |
| [#4 Implementando seu próprio job do Glue](#cenário-4-implementando-seu-próprio-job-do-glue) | Usuários com conhecimentos intermediários |

___

## Cenário 1: um primeiro passo na análise dos recursos

O primeiro cenário de aplicação envolve basicamente uma análise geral sobre todos os recursos implantados através do **terraglue** na conta AWS alvo. Conhecer todas as possibilidades é o ponto de partida para ganhar uma maior autonomia em processos de Engenharia envolvendo transformação de dados na nuvem.

| 🎯 **Público alvo** | Todos os usuários |
| :-- | :-- |

### Buckets SoR, SoT, Spec e outros

O primeiro ponto a ser destacado no *kit* de funcionalidades está relacionado à criação automática de buckets S3 na conta AWS alvo de implantação para simular toda uma organização de **Data Lake** presente em grandes corporações.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-buckets-s3.png?raw=true" alt="terraglue-practical-buckets-s3">
</div>
</details>

| **Bucket** | **Descrição** |
| :-- | :-- |
| `terraglue-athena-query-results` | Bucket criado para armazenar os resultados de query do Athena |
| `terraglue-glue-assets` | Bucket responsável por armazenar todos os *assets* do Glue, incluindo o script Python utilizado como alvo do job e demais logs |
| `terraglue-sor-data` | Armazenamento de dados SoR do projeto de acordo com a organização local presente no diretório `./data` |
| `terraglue-sot-data` | Bucket responsável por armazenar possíveis dados gerados a partir de jobs do Glue caracterizados na camada SoT |
| `terraglue-spec-data` | Bucket responsável por armazenar possíveis dados gerados a partir de jobs do Glue caracterizados na camada Spec |

Todo o processo consolidado na ferramenta de IaC para a criação dos buckets considera a adição de um sufixo que contempla o ID da conta AWS e a região de implantação de forma totalmente automática, garantindo assim que, independente do ambiente (dev, homologação e produção com diferentes contas) ou da região, os nomes dos buckets serão dinâmicos e únicos.

___

### Dados na camada SoR

Além da criação automática de buckets s3 simulando uma organização de Data Lake, o **terraglue** também considera a inserção de dados presentes no diretório `./data` na raíz do repositório respeitando a organização local considerada. Isto significa que, ao posicionar um arquivo de qualquer extensão em uma hierarquia de pastas adequada para representar tal arquivo em uma estrutura de Data Lake, este será automaticamente ingerido no bucket `terraglue-sor-data` da conta.

Para uma melhor compreensão desta funcionalidade, considere a existência de um arquivo CSV presenta na raíz do repositório do projeto dentro do seguinte caminho:

```./data/ra8/customers/olist_customers_dataset.csv```

Ao executar o comando terraform para implantação dos recursos, este mesmo arquivo estará presente no bucket SoR no seguinte caminho:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-data-customers.png?raw=true" alt="terraglue-practical-buckets-s3">
</div>
</details>

Em outras palavras, toda a estrutura de dados (arquivos locais) armazenadas no diretório `./data` do repositório será ingerida no bucket `terraglue-sor` da conta AWS alvo, respeitando toda a hierarquia local de diretórios através da materialização de *folders* no S3. Por padrão, o `terraglue` proporciona alguns conjuntos de dados contendo dados de vendas online no [e-commerce brasileiro](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) e, sem nenhuma alteração por parte do usuário, a tabela abaixo traz uma relação completa dos arquivos locais e suas respectivas ARNs no S3 após a implantação dos recursos.

| 📁 **Caminho local** | 🧺 **S3 URI de objeto na AWS** |
| :-- | :-- |
| `data/ra8/customers/olist_customers_dataset.csv` | <details><summary>Clique para expandir</summary>`arn:aws:s3:::terraglue-sor-data-<accountid>-<region>/ra8/customers/olist_customers_dataset.csv`</details> |
| `data/ra8/orders/olist_orders_dataset.csv` | <details><summary>Clique para expandir</summary>`arn:aws:s3:::terraglue-sor-data-<accountid>-<region>/ra8/orders/olist_orders_dataset.csv`</details> |
| `data/ra8/payments/olist_order_payments_dataset.csv` | <details><summary>Clique para expandir</summary>`arn:aws:s3:::terraglue-sor-data-<accountid>-<region>/ra8/orders/olist_order_payments_dataset.csv`</details> |
| `data/ra8/reviews/olist_order_reviews_dataset.csv` | <details><summary>Clique para expandir</summary>`arn:aws:s3:::terraglue-sor-data-<accountid>-<region>/ra8/orders/olist_order_reviews_dataset.csv`</details> |
| | |

___

### Catalogação no Data Catalog

Até este momento da exemplificação, foi possível notar que o `terraglue` proporciona a criação de toda uma infraestrutura de buckets S3 e a subsequente ingestão de arquivos em um bucket específico de dados brutos na conta. Estas duas operações, por si só, trazem consigo uma tremenda facilidade em termos de automatização e disponibilização de dados para os mais variados propósitos em um ambiente AWS.

Entretanto, possuir dados brutos apenas armazenados no S3 não significa que alguns serviços específicos do ramo de Analytics poderão ser utilizados com os mesmos. Em outras palavras, considerando que os arquivos brutos não possuem **entradas no catálogo de dados** (Data Catalog) da AWS, serviços como o Athena e o Glue precisarão de algumas configurações adicionais para serem utilizados com toda sua eficiência.

Com isso em mente, o `terraglue` possui uma **incrível funcionalidade** capaz de catalogar arquivos CSV no Data Catalog de forma automática e instantânea. Isto significa que, ao executar o comando de implantação via Terraform, além dos dados brutos inseridos no S3, o usuário também terá em mãos toda uma catalogação dos referidos dados no Data Catalog de modo a disponibilizar prontamente os metadados para uso no universo de Analytics da AWS.

Na imagem abaixo, é possível visualizar todas as tabelas e bancos de dados catalogados automaticamente no projeto:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-data-catalog-01.png?raw=true" alt="terraglue-practical-data-catalog-01">
</div>
</details>

Entrando em maiores detalhes e utilizando a tabela `customers` como exemplo, a imagem abaixo exemplifica os detalhes técnicos catalogados e permite analisar atributos como *location*, *input format*, *output format* e propriedades *SerDe*:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-data-catalog-02.png?raw=true" alt="terraglue-practical-data-catalog-02">
</div>
</details>

Por fim, reforçando de uma vez por todas o poder dessa funcionalidade de catalogação do projeto, a imagem abaixo traz as colunas obtidas automaticamente através de funções Terraform dos arquivos brutos e inseridos automaticamente no Data Catalog como atributos da tabela:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-data-catalog-03.png?raw=true" alt="terraglue-practical-data-catalog-03">
</div>
</details>

___

### Athena workgroup

Provavelmente uma das primeiras ações realizadas por usuários após a inserção de dados em um bucket e sua posterior catalogação é a **execução de queries no Athena**. Visando alcançar este público, o `terraglue` considera a criação automática de um [Athena workgroup](https://docs.aws.amazon.com/athena/latest/ug/user-created-workgroups.html) já configurado para uso.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-athena-workgroup.png?raw=true" alt="terraglue-practical-athena-workgroup">
</div>
</details>

Com isso, os usuários já podem iniciar o consumo de dados no Athena sem a necessidade de realizar configurações prévias ou adicionais na conta alvo.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-athena-query.png?raw=true" alt="terraglue-practical-athena-query">
</div>
</details>

___

### IAM policies e roles

Neste momento, estamos aproximando do objetivo do projeto que diz respeito a implementação de um job do Glue totalmente configurado. Uma etapa crucial que antecede a criação de um job no Glue está relacionada à definição e criação dos elementos capazes de fornecer os acessos necessários para o job. Aqui, estamos falando de *policies* e *roles* do IAM.

Dessa forma, o `terraglue` considera, em seus detalhes internos de implantação de recursos, a criação de **2 policies** e **1 role** do IAM a ser vinculada ao job do Glue já com todos os acessos necessários de execução e catalogação de dados.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-iam-role.png?raw=true" alt="terraglue-practical-iam-role">
</div>
</details>

Para maiores detalhes sobre o conteúdo das *policies* que foram a referida *role*, basta acessar os seguintes links:

- [glue-s3-ops-policy](https://github.com/ThiagoPanini/terraglue/blob/main/infra/modules/iam/policy/glue-s3-ops-policy.json)
- [glue-service-policy](https://github.com/ThiagoPanini/terraglue/blob/main/infra/modules/iam/policy/glue-service-policy.json)

___

### Glue job

E assim, alcançando o verdadeiro clímax do processo de implantação de recursos na conta AWS alvo, chegamos no **job do Glue** criado como parte da dinâmica de aprendizado que proporcionar um exemplo prático de consulta de dados em uma camada SoR com a subsequente preparação e disponibilização de dados curados na camada SoT.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-glue-job-01.png?raw=true" alt="terraglue-practical-glue-job-01">
</div>
</details>

Considerando a lógica definida na ferramenta de IaC, o job do Glue possui todo um arcabolso de parâmetros e configuração estabelecidos de forma automática para que o usuário tenha em mãos um exemplo mais fidedigno possível de um processo de ETL na AWS sem se preocupar com definições adicionais.

Ao acessar o job através do console e navegar até o menu *Job details* (ou detalhes do job), o usuário poderá analisar todas as configurações estabelecidas, como por exemplo, a role IAM, os caminhos no s3 para armazenamento do *script* Python, *assets* e outros objetos. Ao final deste menu, o usuário também poderá verificar todo o *set* de parâmetros do job disponibilizados como padrão para a realização e execução do processo de transformação de dados.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-glue-job-02.png?raw=true" alt="terraglue-practical-glue-job-02">
</div>
</details>

___

### Dados na camada SoT

E assim, ao acessar o job do Glue criado e realizar sua execução, o usuário poderá analisar todos os detalhes de construção envolvidos, incluindo os parâmetros associados, as configurações internas do job e também os logs de execução no CloudWatch.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-sot-01.png?raw=true" alt="terraglue-practical-glue-sot-01">
</div>
</details>

Como resultado, o usuário terá disponível uma nova base de dados materializada como uma tabela já catalogada com seus dados armazenados no S3 (bucket SoT) no caminho `s3://terraglue-sot-data-503398944907-us-east-1/ra8/tbsot_ecommerce_br/anomesdia=20221111/`:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-sot-02.png?raw=true" alt="terraglue-practical-glue-sot-02">
</div>
</details>

___

## Cenário 2: compreendendo detalhes de um job Spark no Glue

Agora que o usuário já passou pelo primeiro cenário de consumo do **terraglue** através do conhecimento geral sobre seus recursos e dinâmica de implantação, é chegado o momento de apresentar, em detalhes, a ideia de modelo padronizado de uma aplicação Spark a ser utilizada em toda e qualquer criação de *job* do Glue.

| 🎯 **Público alvo** | Usuários com conhecimentos básicos |
| :-- | :-- |

### O script main-terraglue.py

A ideia é ousada e ambiciosa: proporcionar, ao usuário final, um *template* de código muito além de um simples [*boilerplate*](https://pt.wikipedia.org/wiki/Boilerplate_code) e que permita entregar aplicações Spark implantadas como *jobs* do Glue de uma maneira muito mais fácil e ágil através de poucas modificações. Com esse objetivo, faz-se presente o script [main-terraglue.py](https://github.com/ThiagoPanini/terraglue/blob/develop/app/main-terraglue.py) ao qual será alvo da totalidade de exemplificações desta seção. Fique ligado e veja como otimizar seu processo de criação de ETLs na nuvem!

De início, é válido citar que toda a codificação presente no script `main-terraglue.py` fornecido como exemplo do projeto pode auxiliar grandemente usuários em dois perfis diferentes:

* 🤔 Usuários com pouco ou nenhum conhecimento em Spark, Python e Glue que possuem a intenção de construir processos através de uma adaptação simplória de um código já organizado e bem estruturado.
* 🤓 Usuários avançados que já possuem *jobs* Glue implantados, mas que percebem que a quantidade de linhas de código ou mesmo a organização adotada não é escalável, prejudicando assim a manutenção de suas aplicações.

No mais, a proposta de padronização de um *job* Glue no script `main-terraglue.py` tem como base a estruturação de duas classes Python codificadas exclusivamente para facilitar o trabalho do usuário final em meio as etapas de construção, configuração e execução de uma aplicação Spark.

### Classes GlueJobManager e GlueTransformationManager

Como introduzido previamente, o script Python presente no projeto é composto por duas classes extremamente úteis:

| **Classe Python** | **Atuação e Importância** |
| :-- | :-- |
| `GlueJobManager` | Utilizada para gerenciar toda a construção de um *job* Glue através da inicialização dos argumentos do processo e dos elementos que compõem o contexto (`GlueContext` e `SparkContext`) e sessão (`SparkSession`) de uma aplicação. |
| `GlueTransformationManager` | Utilizada para consolidar métodos prontos para leitura de `DynamicFrames` e `DataFrames` e transformação destes objetos no contexto de utilização do *job*. |

Para que se tenha uma noção do grande poder de utilização de ambas as classes em um cenário de construção de um *job* do Glue sustentável e com as melhores práticas de código limpo, o bloco abaixo representa a parte principal do script onde o usuário solicita a execução da aplicação com poucas instruções:

```python
if __name__ == "__main__":

    # Inicializando objeto para gerenciar o job e as transformações
    glue_manager = GlueTransformationManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    # Executando todas as lógicas mapeadas do job
    glue_manager.run()
```

Claro que, de maneira intuitiva, o método `run()` atua como um grande consolidador de outros métodos de transformação presentes na classe `GlueTransformationManager`. Mesmo assim, são poucas as atuações necessárias por parte do usuário para adaptar toda a estrutura de código proporcionada para seu respectivo *job*.

### Ações do usuário para utilizar e adaptar o script

Considerando os detalhes demonstrados acima, usuários iniciantes ou experientes que desejam utilizar o template do **terraglue** para construir seus *jobs* Glue deverão, essencialmente, seguir quatro passos importantes no processo de consumo:

1. Adaptar o vetor de argumentos do *job* através da variável `ARGV_LIST`
2. Adaptar o dicionário com os dados a serem utilizados no *job* através da variável `DATA_DICT`
3. Criar os métodos de transformação dos dados na classe `GlueTransformationManager`
4. Adaptar o método `run()` com os dados a serem lidos e os novos métodos gerados

Todas as demais operações já estão inclusas nos métodos internos das classes disponibilizadas ao usuário e não necessitam de alterações. Em outras palavras, o usuário pode focar nas codificações relacionadas às suas próprias transformações de dados ao invés de se preocupar os elementos de configuração do *job*.

> Neste momento, é importante citar que ambas as classes `GlueJobManager` e `GlueTransformationManager` possuem uma vasta documentação no script Python [main-terraglue.py](https://github.com/ThiagoPanini/terraglue/blob/develop/app/main-terraglue.py) disponibilizado. Consulte o arquivo fonte para informações mais detalhadas a respeito deste vasto leque de possibilidades envolvendo a padronização da construção de um job do Glue.
___

## Cenário 3: implementando seu próprio conjunto de dados

### Utilizando dados próprios

### Visualizando efeitos na conta AWS

___

## Cenário 4: implementando seu próprio job do Glue

### Codificando novas transformações

### Executando jobs próprios
