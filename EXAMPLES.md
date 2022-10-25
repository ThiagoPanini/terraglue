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
- [Cenário 2: aprendendo mais sobre o runtime Terraform](#cenário-2-aprendendo-mais-sobre-o-runtime-terraform)
  - [O módulo storage](#o-módulo-storage)
  - [O módulo catalog](#o-módulo-catalog)
  - [O módulo iam](#o-módulo-iam)
  - [O módulo glue](#o-módulo-glue)
- [Cenário 3: compreendendo detalhes de um job Spark no Glue](#cenário-3-compreendendo-detalhes-de-um-job-spark-no-glue)
  - [A classe GlueJobManager](#a-classe-gluejobmanager)
  - [A classe GlueTransformationManager](#a-classe-gluetransformationmanager)
- [Cenário 4: implementando seu próprio conjunto de dados](#cenário-4-implementando-seu-próprio-conjunto-de-dados)
  - [Utilizando dados próprios](#utilizando-dados-próprios)
  - [Visualizando efeitos na conta AWS](#visualizando-efeitos-na-conta-aws)
- [Cenário 5: implementando seu próprio job do Glue](#cenário-5-implementando-seu-próprio-job-do-glue)
  - [Codificando novas transformações](#codificando-novas-transformações)
  - [Executando jobs próprios](#executando-jobs-próprios)
___

## Antes de começar

Antes de navegarmos por exemplos práticos de consumo, é importante garantir que todas as etapas de preparação e instalação foram cumpridas. Para maiores detalhes, o arquivo [GETTINGSTARTED.md]() contempla todo o processo necessário de iniciação.

Adicionalmente, é válido citar que esta documentação será separada em diferentes **cenários**, cada um trazendo à tona uma possível seara de aplicação do **terraglue** de acordo com um propósito específico. É importante destacar que os cenários contemplam desafios próprios e particulares, sendo direcionados para públicos específicos que podem se beneficiar das funcionalidades deste projeto. Encontre aquele que mais faça sentido dentro de sua jornada de aprendizado e mergulhe fundo!

___

## Cenário 1: um primeiro passo na análise dos recursos

O primeiro cenário de aplicação envolve basicamente uma análise geral sobre todos os recursos implantados através do **terraglue** na conta AWS alvo. Conhecer todas as possibilidades é o ponto de partida para ganhar uma maior autonomia em processos de Engenharia envolvendo transformação de dados na nuvem.

| | | |
| :-- | :-- | :-- |
| **Cenário** | Um primeiro passo na análise dos recursos |
| **Público** | Todos |
| **Descrição** | Navegação sobre todos os serviços implantados na conta AWS para uma visualização completa e holística sobre as diferentes possibilidades disponibilizadas pelo terraglue |
| | | |

### Buckets SoR, SoT, Spec e outros

O primeiro ponto a ser destacado no *kit* de funcionalidades está relacionado à criação automática de buckets S3 na conta AWS alvo de implantação para simular toda uma organização de **Data Lake** presente em grandes corporações.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-buckets-s3.png?raw=true" alt="terraglue-practical-buckets-s3">
</div>
</details>
<br>

| **Bucket** | **Descrição** |
| :-- | :-- |
| `terraglue-athena-query-results` | Bucket criado para armazenar os resultados de query do Athena |
| `terraglue-glue-assets` | Bucket responsável por armazenar todos os *assets* do Glue, incluindo o script Python utilizado como alvo do job e demais logs |
| `terraglue-sor-data` | Armazenamento de dados SoR do projeto de acordo com a organização local presente no diretório `./data` |
| `terraglue-sot-data` | Bucket responsável por armazenar possíveis dados gerados a partir de jobs do Glue caracterizados na camada SoT |
| `terraglue-spec-data` | Bucket responsável por armazenar possíveis dados gerados a partir de jobs do Glue caracterizados na camada Spec |

___

### Dados na camada SoR

Além da criação automática de buckets s3 simulando uma organização de Data Lake, o **terraglue** também considera a inserção de dados presentes no diretório `./data` na raíz do repositório respeitando a organização local considerada. Isto significa que, ao posicionar um arquivo de qualquer extensão em uma hierarquia de pastas adequada para representar tal arquivo em uma estrutura de Data Lake, este será automaticamente ingerido no bucket `terraglue-sor-data` da conta.

Para visualizar melhor esta funcionalidade, considere o seguinte arquivo presente na raíz do repositório do projeto:

```./data/ra8/customers/olist_customers_dataset.csv```

Ao executar o comando terraform para implantação dos recursos, este mesmo arquivo estará presente no bucket SoR no seguinte caminho:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-data-customers.png?raw=true" alt="terraglue-practical-buckets-s3">
</div>
</details>
<br>

| **Caminho local** | **ARN de objeto na AWS** |
| :-- | :-- |
| | |
| | |


### Catalogação no Data Catalog

### Athena workgroup

### IAM policies e roles

### Glue job

### Dados na camada SoT

___

## Cenário 2: aprendendo mais sobre o runtime Terraform

### O módulo storage

### O módulo catalog

### O módulo iam

### O módulo glue
___

## Cenário 3: compreendendo detalhes de um job Spark no Glue

### A classe GlueJobManager

### A classe GlueTransformationManager

___

## Cenário 4: implementando seu próprio conjunto de dados

### Utilizando dados próprios

### Visualizando efeitos na conta AWS
___

## Cenário 5: implementando seu próprio job do Glue

### Codificando novas transformações

### Executando jobs próprios
