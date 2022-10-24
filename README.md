# terraglue
*Auxiliando desenvolvedores, engenheiros e analistas a implantar e testar jobs do Glue na AWS*


## Table of Contents
- [terraglue](#terraglue)
  - [Table of Contents](#table-of-contents)
  - [O que é o terraglue?](#o-que-é-o-terraglue)
    - [Motivadores e principais desafios](#motivadores-e-principais-desafios)
    - [Quem pode utilizar o terraglue?](#quem-pode-utilizar-o-terraglue)
    - [Pré requisitos](#pré-requisitos)
  - [Visão de arquitetura](#visão-de-arquitetura)
    - [Organização do repositório](#organização-do-repositório)
    - [Detalhes de construção da infraestrutura](#detalhes-de-construção-da-infraestrutura)
  - [Utilizando o projeto](#utilizando-o-projeto)
  - [Exemplos práticos de funcionalidades](#exemplos-práticos-de-funcionalidades)
    - [Buckets SoR, SoT, Spec e outros](#buckets-sor-sot-spec-e-outros)
    - [Dados na camada SoR](#dados-na-camada-sor)
    - [Catalogação no Data Catalog](#catalogação-no-data-catalog)
    - [Athena workgroup](#athena-workgroup)
    - [IAM policies e roles](#iam-policies-e-roles)
    - [Glue job](#glue-job)
    - [Dados na camada SoT](#dados-na-camada-sot)

___

## O que é o terraglue?

Imagine o seguinte cenário: você é alguém da área de dados com o desejo de aprender e explorar soluções envolvendo o processamento de dados na AWS, em especial o serviço [AWS Glue](https://aws.amazon.com/glue/) e todos os seus componentes relacionado.

Nessa jornada, você procura por documentações, pesquisa em fóruns, assiste vídeos nas mais variadas plataformas mas, ainda sim, não sente a confiança necessária para entender e aplicar, de fato, todas as etapas de construção de um job de processamento de dados *end to end* na nuvem. Seria ótimo ter um ambiente próprio, totalmente configurado e de fácil implantação, não é mesmo?

E assim, para sanar essa e outras dificuldades, nasce o **terraglue** como um projeto desenvolvido exclusivamente para facilitar e acelerar o aprendizado em serviços como AWS Glue, [Athena](https://aws.amazon.com/athena/) e [Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html) em toda a dinâmica de obtenção, processamento e escrita de dados (ETL) na nuvem. Embarque nesta jornada e tenha em mãos um ferramental extremamente rico e de fácil utilização para se especializar no universo analítico da AWS.

___

### Motivadores e principais desafios

Uma vez apresentado o projeto, é importante destacar que o **terraglue** possui uma essência altamente dinâmica, isto é, suas funcionalidades abrem margem para uma série de possibilidades e ganhos. Para que se tenha uma ideia de todas as suas possíveis aplicações, as perguntas abaixo representam alguns obstáculos, dores e desafios reais que podem ser devidamente solucionados. Clique e expanda os blocos para visualizar algumas *features* do projeto.

<details>
  <summary>📌 "Como funciona o processo de criação de jobs do Glue na AWS? São muitos parâmetros a serem passados e fica difícil saber o impacto de cada configuração."</summary>

  > 💡 *Com o terraglue, os usuários poderão implantar jobs Glue na AWS de uma maneira fácil, prática e objetiva, sem se preocupar com todos os parâmetros de configuração exigidos. Em um curto espaço de tempo, os usuários terão a confiança necessária para entender toda a dinâmica e aplicar, por conta própria, modificações que atendam suas respectivas necessidades.*
</details>

<details>
  <summary>📌 "Mesmo que eu consiga criar um job, quais dados de exemplo posso utilizar para meu processo de ETL?"</summary>

  > 💡 *No projeto, diferentes arquivos da base de dados [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) são utilizados para servirem de exemplos de execução de um job responsável por simular um processo de especialização de dados. De forma alternativa, usuários mais experientes podem utilizar suas próprias bases de dados para simular jobs de acordo com os objetivos propostos.*
</details>

<details>
  <summary>📌 "No final de tudo, eu consigo automatizar toda a infraestrutura necessária para implantar um job do Glue na AWS?"</summary>

  > 💡 *Ao ter em mãos as funcionalidades do terraglue, o usuário poderá implantar toda a infraestrutura necessária para a execução de um job de ETL responsável pela especialização de um conjunto de dados na AWS através de **um único comando** em qualquer ambiente que se tenha acesso. Essa é, sem dúvidas, uma das principais vantagens do projeto!*
</details>

<details>
  <summary>📌 "GlueContext? DynamicFrame? Como todos esses elementos se encaixam na dinâmica de um job do Glue?"</summary>

  > 💡 *No script de aplicação do repositório, é possível encontrar toda a lógica de implementação de um job Glue com todas as documentações necessárias para um claro entendimento de como os elementos de contexto e sessão se relacionam em um processo de ETL.*
</details>

<details>
  <summary>📌 "Já construí jobs do Glue anteriormente seguindo uma lógica própria e tenho muita dificuldade em organizar meu código a medida que novas transformações são programadas."</summary>

  > 💡 *O exemplo de aplicação Spark fornecido como padrão no terraglue possui uma organização especificamente pensada na escalabilidade de código. As classes `GlueJobManager` e `GlueTransformationManager` auxiliam usuários com conhecimento prévio a organizarem jobs com um alto número de transformações sem abrir mão das boas práticas.*
</details>


Ansioso para conhecer mais sobre o projeto? Ainda nesta documentação, toda sua arquitetura será apresentada e um completo tutorial de utilização será fornecido. Continue acompanhando!
___

### Quem pode utilizar o terraglue?

De maneira clara e objetiva: o **terraglue** pode ser utilizado por toda e qualquer pessoa que tenha algum tipo de necessidade específica de aprender sobre jobs Glue na AWS. Sua construção tem como base o fornecimento de um ambiente dinâmico e totalmente reprodutível para implantação de um job Glue adaptável às necessidades dos usuários.

___

### Pré requisitos

Você verá que utilizar o **terraglue** é extremamente fácil e suas exigências e pré requisitos são igualmente simples. Basta ter:

- Conta AWS e usuário com acesso programático
- Terraform instalado no sistema
___

## Visão de arquitetura

Agora que você já conhece um pouco mais sobre o projeto, é chegado o momento de apresentar toda a arquitetura que está por trás das funcionalidades introduzidas. No final do dia, o **terraglue** é um projeto de IaC (*Infrastructure as Code*) construído com o *runtime* [Terraform](https://www.terraform.io/) e dividido em módulos responsáveis por implantar diferentes serviços AWS que, juntos, formam toda a dinâmica de consumo do projeto. Assim, o usuário obtém o código fonte disponibilizado neste repositório e executa os comandos específicos do runtime de IaC utilizado para realizar as implantações necessárias no ambiente alvo.

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-diagram-user-view.png" alt="terraglue-user-view">
</div>

Em uma visão mais técnica, os serviços declarados nos módulos Terraform são representados por:

  - Buckets S3 para armazenamento de dados e *assets*
  - Policies e role IAM para gerenciamento de acessos
  - Referências no catálogo de dados e workgroup do Athena
  - Job do Glue parametrizado com exemplo prático de uso

Assim, ao cumprir os requisitos e as ações evidenciadas pela imagem de arquitetura acima, o usuário poderá ter em mãos seu próprio "ambiente AWS portátil" composto dos seguintes recursos:

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-diagram-resources.png?raw=true" alt="terraglue-resources">
</div>

Como ponto de destaque da imagem acima, é possível visualizar que o **terraglue** comporta também a "ingestão" (ou simplesmente o *upload*) de alguns dados na conta alvo AWS para servirem de insumos de execução de um job Glue também implementado como exemplo. Trata-se de alguns arquivos do conjunto de dados [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) que estão publicamente disponíveis no [Kaggle](https://www.kaggle.com/).

___

### Organização do repositório

Considerando os insumos presentes, o repositório do **terraglue** está organizado da seguinte forma:

| **Diretório** | **Função** |
| :-- | :-- |
| `./app` | Aqui será possível encontrar o script Python disponibilizado como padrão para implantação de um job Glue na AWS seguindo as melhores práticas de código e documentação. O script considera um cenário de criação de uma base na camada [SoT](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/) (*Source of Truth*) utilizando dados de vendas online no [e-commerce brasileiro](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). |
| `./data` | Neste diretório, será possível identificar todas as fontes de dados disponibilizadas como exemplo para a execução de um job do Glue. Os dados estão presentes e organizados de modo a simular uma estrutura padrão de Data Lake em ambientes distribuídos, onde define-se o banco de dados, nome de tabela como diretórios pais em relação aos arquivos propriamente ditos (ex: `db/table/file.ext`). |
| `./docs` | Aqui o usuário poderá encontrar todos os diagramas e imagens utilizadas na documentação do projeto. |
| `./infra` | Este é, provavelmente, o principal diretório no projeto. Nele, será possível encontrar todas as declarações Terraform responsáveis pela implantação da infraestrutura necessária para utilização do projeto na AWS. Uma seção específica sobre esta parte será detalhada logo a seguir. |

___

### Detalhes de construção da infraestrutura

Como mencionado (e sugerido pelo próprio nome), o **terraglue** é um projeto Terraform organizado de forma a proporcionar, a seus usuários, um entendimento claro sobre cada operação de implantação realizada. Seguindo as boas práticas de criação de um projeto, sua construção foi dividida em [módulos](https://developer.hashicorp.com/terraform/language/modules) responsáveis por declarações específicas de recursos de acordo com um tema relacionado.

| **Módulo** | **Descrição** |
| :-- | :-- |
| `root` | Módulo principal do projeto responsável por acionar todos os módulos relacionados |
| `storage` | Módulo responsável por todas as declarações que dizem respeito à armazenamento na conta AWS alvo de implantação. Recursos como buckets S3 e a ingestão de objetos são definidos aqui. |
| `catalog` | Este módulo possui uma importante missão de alocar uma lógica específica de catalogação dos objetos inseridos no S3 no Data Catalog. Aqui são criados os databases e tabelas no catálogo de dados de acordo com a organização local dos dados do repositório. Tudo de forma automática. Adicionalmente, um workgroup do Athena é fornecido ao usuário para que as consultas sejam realizadas sem a necessidade de configurações adicionais na conta. |
| `iam` | No módulo iam do projeto, uma role de serviço do Glue é criada com policies específicas e pré configuradas de modo a proporcionar todos os acessos necessários de execução de um job Glue na conta alvo de implantação. |
| `glue` | Por fim, o módulo glue comporta toda a parametrização e declaração do recurso responsável por implantar um job Glue na AWS considerando todas as boas práticas de uso. |

___


## Utilizando o projeto

Visando dispor de um lugar específico para detalhar o tutorial de utilização do projeto, todas as etapas estão devidamente exemplificadas no arquivo [GETTINGSTARTED.md](https://github.com/ThiagoPanini/terraglue/blob/develop/GETTINGSTARTED.md)

___

## Exemplos práticos de funcionalidades

E assim, visando proporcionar ao usuário alguns exemplos das principais funcionalidades embutidas no **terraglue**, esta seção consolida detalhes técnicos sobre os cenários práticos de aplicação.

Considerando a essência do projeto, os insumos a serem detalhados se fazem presente após a execução do comando `terraform apply` para implantação dos recursos e serviços declarados em seu código fonte.

### Buckets SoR, SoT, Spec e outros

O primeiro ponto a ser destacado no *kit* de funcionalidades está relacionado à criação automática de buckets S3 na conta AWS alvo de implantação para simular toda uma organização de **Data Lake** presente em grandes corporações. A imagem abaixo representa todos os buckets criados e, no menu *dropdown*, será possível visualizar detalhes adicionais sobre os mesmos.

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-buckets-s3.png?raw=true" alt="terraglue-practical-buckets-s3">
</div>

<details>
  <summary>Clique para ver detalhes de cada bucket</summary>

  | **Bucket** | **Descrição** |
  | :-- | :-- |
  | `terraglue-athena-query-results` | Bucket criado para armazenar os resultados de query do Athena |
  | `terraglue-glue-assets` | Bucket responsável por armazenar todos os *assets* do Glue, incluindo o script Python utilizado como alvo do job e demais logs |
  | `terraglue-sor-data` | Armazenamento de dados SoR do projeto de acordo com a organização local presente no diretório `./data` |
  | `terraglue-sot-data` | Bucket responsável por armazenar possíveis dados gerados a partir de jobs do Glue caracterizados na camada SoT |
  | `terraglue-spec-data` | Bucket responsável por armazenar possíveis dados gerados a partir de jobs do Glue caracterizados na camada Spec |

</details>

___

### Dados na camada SoR

Além da criação automática de buckets s3 simulando uma organização de Data Lake, o **terraglue** também considera a inserção de dados presentes no diretório `./data` na raíz do repositório respeitando a organização local considerada. Isto significa que, ao posicionar um arquivo de qualquer extensão em uma hierarquia de pastas adequada para representar tal arquivo em uma estrutura de Data Lake, este será automaticamente ingerido no bucket `terraglue-sor-data` da conta.

Para visualizar melhor esta funcionalidade, considere o seguinte arquivo presente na raíz do repositório do projeto:

```./data/ra8/customers/olist_customers_dataset.csv```

Ao executar o comando terraform para implantação dos recursos, este mesmo arquivo estará presente no bucket SoR no seguinte caminho:

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-data-customers.png?raw=true" alt="terraglue-practical-buckets-s3">
</div>

<details>
  <summary>Clique para ver detalhes de cada arquivo bruto</summary>

  | **Caminho local** | **ARN de objeto na AWS** |
  | :-- | :-- |
  | | |
  | |

</details>


### Catalogação no Data Catalog

### Athena workgroup

### IAM policies e roles

### Glue job

### Dados na camada SoT