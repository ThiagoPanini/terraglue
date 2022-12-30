*Fornecendo detalhes sobre toda a infraestrutura provisionada ao usuário*

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Antes de começar](#antes-de-começar)
- [Módulos Terraform](#módulos-terraform)
- [Analisando os recursos de infra provisionados](#analisando-os-recursos-de-infra-provisionados)
  - [Buckets SoR, SoT, Spec e outros](#buckets-sor-sot-spec-e-outros)
  - [Dados na camada SoR](#dados-na-camada-sor)
  - [Catalogação no Data Catalog](#catalogação-no-data-catalog)
  - [Athena workgroup](#athena-workgroup)
  - [IAM policies e roles](#iam-policies-e-roles)
  - [Glue job](#glue-job)
  - [Dados na camada SoT](#dados-na-camada-sot)

## Antes de começar

> Antes de navegarmos pelo detalhamento da infraestrutura provisionada no projeto, é importante garantir que todas as etapas de preparação e instalação foram cumpridas. Para maiores detalhes, o arquivo [GETTINGSTARTED.md](https://github.com/ThiagoPanini/terraglue/blob/develop/GETTINGSTARTED.md) contempla todo o processo necessário de iniciação.

- [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main)
- [2. Instalação e primeiros passos](https://github.com/ThiagoPanini/terraglue/blob/main/GETTINGSTARTED.md)
- 👉 [3. Infraestrutura provisionada](https://github.com/ThiagoPanini/terraglue/blob/main/INFRA.md) *Você está aqui!*
- [4. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/APP.md) 
- [5. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/EXAMPLES.md)

___

## Módulos Terraform

O **terraglue** é um projeto Terraform organizado de forma a proporcionar, a seus usuários, um entendimento claro sobre cada operação de implantação realizada. Seguindo as boas práticas de criação de um projeto, sua construção foi dividida em [módulos](https://developer.hashicorp.com/terraform/language/modules) responsáveis por declarações específicas de recursos de acordo com um tema relacionado.

| 🏯 **Módulo** | 📝 **Descrição** |
| :-- | :-- |
| [`root`](https://github.com/ThiagoPanini/terraglue/tree/main/infra)| Módulo principal do projeto responsável por acionar todos os módulos relacionados |
| [`modules/storage`](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/storage) | Módulo responsável por todas as declarações que dizem respeito à armazenamento na conta AWS alvo de implantação. Recursos como buckets S3 e a ingestão de objetos são definidos aqui. |
| [`modules/catalog`](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/catalog) | Este módulo possui uma importante missão de alocar uma lógica específica de catalogação dos objetos inseridos no S3 no Data Catalog. Aqui são criados os databases e tabelas no catálogo de dados de acordo com a organização local dos dados do repositório. Tudo de forma automática. Adicionalmente, um workgroup do Athena é fornecido ao usuário para que as consultas sejam realizadas sem a necessidade de configurações adicionais na conta. |
| [`modules/iam`](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/iam) | No módulo iam do projeto, uma role de serviço do Glue é criada com policies específicas e pré configuradas de modo a proporcionar todos os acessos necessários de execução de um job Glue na conta alvo de implantação. |
| [`modules/glue`](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/glue) | Por fim, o módulo glue comporta toda a parametrização e declaração do recurso responsável por implantar um job Glue na AWS considerando todas as boas práticas de uso. |

___

## Analisando os recursos de infra provisionados

O primeiro passo desta documentação envolve basicamente uma análise geral sobre todos os recursos implantados através do **terraglue** na conta AWS alvo. Conhecer todas as possibilidades é o ponto de partida para ganhar uma maior autonomia em processos de Engenharia envolvendo transformação de dados na nuvem.

### Buckets SoR, SoT, Spec e outros

O primeiro ponto a ser destacado no *kit* de funcionalidades está relacionado à criação automática de buckets S3 na conta AWS alvo de implantação para simular toda uma organização de **Data Lake** presente em grandes corporações.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-buckets-s3.png?raw=true" alt="terraglue-practical-buckets-s3">
</div>
</details>

| 🧺 **Bucket** | 📝 **Descrição** |
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

Considerando a lógica definida na ferramenta de IaC, o job do Glue possui todo um arcabouço de parâmetros e configuração estabelecidos de forma automática para que o usuário tenha em mãos um exemplo mais fidedigno possível de um processo de ETL na AWS sem se preocupar com definições adicionais.

Ao acessar o job através do console e navegar até o menu *Job details* (ou detalhes do job), o usuário poderá analisar todas as configurações estabelecidas, como por exemplo, a role IAM, os caminhos no s3 para armazenamento do *script* Python, *assets* e outros objetos. Ao final deste menu, o usuário também poderá verificar todo o *set* de parâmetros do job disponibilizados como padrão para a realização e execução do processo de transformação de dados.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-glue-job-02.png?raw=true" alt="terraglue-practical-glue-job-02">
</div>
</details>

Além disso, no menu *Schedules*, será possível visualizar um agendamento criado automaticamente via Terraform para execução do *job* Glue com uma expressão cron fornecida como exemplo (`cron(0 21 ? * 6 *)`) simulando o gatilho de execução todas às sextas-feiras às 21h00m. Para maiores detalhes, o usuário poderá consultar o [recurso `aws_glue_trigger`](https://github.com/ThiagoPanini/terraglue/blob/main/infra/modules/glue/main.tf#L49) no módulo glue presente no diretório de infra.

___

### Dados na camada SoT

E assim, ao acessar o job do Glue criado e realizar sua execução, o usuário poderá analisar todos os detalhes de construção envolvidos, incluindo os parâmetros associados, as configurações internas do job e também os logs de execução no CloudWatch.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-sot-01.png?raw=true" alt="terraglue-practical-glue-sot-01">
</div>
</details>

Como resultado, o usuário terá disponível uma nova base de dados materializada como uma tabela já catalogada com seus dados armazenados no S3 (bucket SoT) no caminho `s3://terraglue-sot-data-<accountid>-<region>/ra8/tbsot_ecommerce_br/anomesdia=<anomesdia>/`:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-sot-02.png?raw=true" alt="terraglue-practical-glue-sot-02">
</div>
</details>

___

Continue sua jornada no **terraglue** através das documentações!

- [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main)
- [2. Instalação e primeiros passos](https://github.com/ThiagoPanini/terraglue/blob/main/GETTINGSTARTED.md)
- 👉 [3. Infraestrutura provisionada](https://github.com/ThiagoPanini/terraglue/blob/main/INFRA.md) *Você está aqui!*
- [4. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/APP.md) 
- [5. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/EXAMPLES.md)