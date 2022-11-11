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

Antes de navegarmos por exemplos práticos de consumo, é importante garantir que todas as etapas de preparação e instalação foram cumpridas. Para maiores detalhes, o arquivo [GETTINGSTARTED.md](https://github.com/ThiagoPanini/terraglue/blob/develop/GETTINGSTARTED.md) contempla todo o processo necessário de iniciação.

Adicionalmente, é válido citar que esta documentação será separada em diferentes **cenários**, cada um trazendo à tona uma possível seara de aplicação do **terraglue** de acordo com um propósito específico. É importante destacar que os cenários contemplam desafios próprios e particulares, sendo direcionados para públicos específicos que podem se beneficiar das funcionalidades deste projeto. Encontre aquele que mais faça sentido dentro de sua jornada de aprendizado e mergulhe fundo!

| 🎬 **Cenário** | **🎯 Público alvo** |
| :-- | :-- |
| [#1 Um primeiro passo na análise dos recursos](#cenário-1-um-primeiro-passo-na-análise-dos-recursos) | Todos os usuários |
| [#2 Aprendendo mais sobre o runtime Terraform](#cenário-2-aprendendo-mais-sobre-o-runtime-terraform) | Usuários com conhecimentos básicos |
| [#3 Compreendendo detalhes de um job Spark no Glue](#cenário-3-compreendendo-detalhes-de-um-job-spark-no-glue) | Usuários com conhecimentos intermediários |
| [#4 Implenentando seu próprio conjunto de dados](#cenário-4-implementando-seu-próprio-conjunto-de-dados) | Usuários com conhecimentos intermediários |
| [#5 Implementando seu próprio conjunto de dados](#cenário-5-implementando-seu-próprio-job-do-glue) | Usuários com conhecimentos intermediários |

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
<br>

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
<br>

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
<br>

Entrando em maiores detalhes e utilizando a tabela `customers` como exemplo, a imagem abaixo exemplifica os detalhes técnicos catalogados e permite analisar atributos como *location*, *input format*, *output format* e propriedades *SerDe*:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-data-catalog-02.png?raw=true" alt="terraglue-practical-data-catalog-02">
</div>
</details>
<br>

Por fim, reforçando de uma vez por todas o poder dessa funcionalidade de catalogação do projeto, a imagem abaixo traz as colunas obtidas automaticamente através de funções Terraform dos arquivos brutos e inseridos automaticamente no Data Catalog como atributos da tabela:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-data-catalog-03.png?raw=true" alt="terraglue-practical-data-catalog-03">
</div>
</details>
<br>

___

### Athena workgroup

Provavelmente uma das primeiras ações realizadas por usuários após a inserção de dados em um bucket e sua posterior catalogação é a **execução de queries no Athena**. Visando alcançar este público, o `terraglue` considera a criação automática de um [Athena workgroup](https://docs.aws.amazon.com/athena/latest/ug/user-created-workgroups.html) já configurado para uso.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-athena-workgroup.png?raw=true" alt="terraglue-practical-athena-workgroup">
</div>
</details>
<br>

Com isso, os usuários já podem iniciar o consumo de dados no Athena sem a necessidade de realizar configurações prévias ou adicionais na conta alvo.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-athena-query.png?raw=true" alt="terraglue-practical-athena-query">
</div>
</details>
<br>

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
<br>

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
<br>

Considerando a lógica definida na ferramenta de IaC, o job do Glue possui todo um arcabolso de parâmetros e configuração estabelecidos de forma automática para que o usuário tenha em mãos um exemplo mais fidedigno possível de um processo de ETL na AWS sem se preocupar com definições adicionais.

Ao acessar o job através do console e navegar até o menu *Job details* (ou detalhes do job), o usuário poderá analisar todas as configurações estabelecidas, como por exemplo, a role IAM, os caminhos no s3 para armazenamento do *script* Python, *assets* e outros objetos. Ao final deste menu, o usuário também poderá verificar todo o *set* de parâmetros do job disponibilizados como padrão para a realização e execução do processo de transformação de dados.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-glue-job-02.png?raw=true" alt="terraglue-practical-glue-job-02">
</div>
</details>
<br>

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
