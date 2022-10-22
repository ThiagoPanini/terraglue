# terraglue
*Auxiliando desenvolvedores, engenheiros e analistas a implantar e testar jobs do Glue na AWS*


## Table of Contents
- [terraglue](#terraglue)
  - [Table of Contents](#table-of-contents)
  - [O que é o terraglue?](#o-que-é-o-terraglue)
    - [Motivadores e principais desafios](#motivadores-e-principais-desafios)
    - [Quem pode utilizar o terraglue?](#quem-pode-utilizar-o-terraglue)
  - [Visão de arquitetura](#visão-de-arquitetura)
  - [Detalhes Técnicos de Construção](#detalhes-técnicos-de-construção)
  - [Sobre as fontes de dados utilizadas](#sobre-as-fontes-de-dados-utilizadas)
  - [Detalhes Técnicos de Construção](#detalhes-técnicos-de-construção-1)
  - [Passo a passo de utilização do projeto](#passo-a-passo-de-utilização-do-projeto)

___

## O que é o terraglue?

Imagine o seguinte cenário: você é alguém da área de dados com o desejo de aprender e explorar soluções envolvendo o processamento de dados na AWS, em especial o serviço [AWS Glue](https://aws.amazon.com/glue/) e todos os seus componentes relacionado.

Nessa jornada, você procura por documentações, pesquisa em fóruns, assiste vídeos nas mais variadas plataformas mas, ainda sim, não sente a confiança necessária para entender e aplicar, de fato, todas as etapas de construção de um job de processamento de dados *end to end* na nuvem. Seria ótimo ter um ambiente próprio, totalmente configurado e de fácil implantação, não é mesmo?

E assim, para sanar essa e outras dificuldades, nasce o **terraglue** como um projeto desenvolvido exclusivamente para facilitar e acelerar o aprendizado em serviços como AWS Glue, [Athena](https://aws.amazon.com/athena/) e [Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html) em toda a dinâmica de obtenção, processamento e escrita de dados (ETL) na nuvem. Embarque nesta jornada e tenha em mãos um ferramental extremamente rico e de fácil utilização para se especializar no universo analítico da AWS.

___

### Motivadores e principais desafios

Uma vez apresentado o projeto, é importante destacar que o **terraglue** possui uma essência altamente dinâmica, isto é, suas funcionalidades abrem margem para uma série de possibilidades e ganhos. Para que se tenha uma ideia de todas as suas possíveis aplicações, as perguntas abaixo representam alguns obstáculos, dores e desafios reais que podem ser devidamente solucionados pelo **terraglue**:

> *"Como consigo criar um job do Glue no console AWS e quais as configurações adequadas?"*

- 💡 Com o terraglue, os usuários podem implantar toda a infraestrutura necessária para a criação de um job do Glue com a execução de apenas um comando.

> *"Mesmo que eu consiga criar um job, quais dados de exemplo posso utilizar para meu processo de ETL?"*

- 💡 No projeto, diferentes arquivos da base de dados [Brazilian E-Commerce]() são utilizados para servirem de exemplos de execução de um job responsável por simular um processo de especialização de dados.

> *"GlueContext? DynamicFrame? Como todos esses elementos se encaixam na dinâmica de um job do Glue?"*

- 💡 No script de aplicação do repositório, é possível encontrar toda a lógica de implementação de um job Glue com todas as documentações necessárias para um claro entendimento de como os elementos de contexto e sessão se relacionam em um processo de ETL.

> *"No final de tudo, eu consigo automatizar toda a infraestrutura necessária para implantar um job do Glue na AWS?"*

- 💡 Ao ter em mãos as funcionalidades do terraglue, o usuário poderá implantar toda a infraestrutura necessária para a execução de um job de ETL responsável pela especialização de um conjunto de dados na AWS através de **um único comando**.

Ansioso para conhecer mais sobre o projeto? Ainda nesta documentação, toda sua arquitetura será apresentada e um completo tutorial de utilização será fornecido. Continue acompanhando!
___

### Quem pode utilizar o terraglue?

De maneira clara e objetiva: o **terraglue** pode ser utilizado por toda e qualquer pessoa que tenha algum tipo de necessidade específica de aprender sobre jobs Glue na AWS. Sua construção tem como base o fornecimento de um ambiente dinâmico e totalmente reprodutível para implantação de um job Glue adaptável às necessidades dos usuários.

___

## Visão de arquitetura

Agora que você já conhece um pouco mais sobre o projeto, é chegado o momento de apresentar toda a arquitetura que está por trás das funcionalidades exemplificadas. Em essência, o **terraglue** é um projeto de IaC (*Infrastructure as Code*) construído com o *runtime* [Terraform](https://www.terraform.io/) e dividido em módulos responsáveis por implantar diferentes serviços AWS que, juntos, formam toda a dinâmica de consumo do projeto.

pelas implantações de serviços AWS como:
  - Buckets S3 para armazenamento de dados e *assets*
  - Policies e role IAM para gerenciamento de acessos
  - Catalogação de dados e workgroup do Athena
  - Job do Glue parametrizado com exemplo prático de uso

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-diagram-user-view.png" alt="terraglue-user-view">
</div>

Em uma visão mais técnica, os serviços declarados nos módulos Terraform são representados por:

  - Buckets S3 para armazenamento de dados e *assets*
  - Policies e role IAM para gerenciamento de acessos
  - Catalogação de dados e workgroup do Athena
  - Job do Glue parametrizado com exemplo prático de uso

Assim, ao cumprir os requisitos e as ações evidenciadas pela imagem de arquitetura acima, o usuário poderá ter em mãos, em seu próprio ambiente AWS, os seguintes recursos:

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-diagram-resources.png?raw=true" alt="terraglue-resources">
</div>

Como ponto de destaque da imagem acima, é possível visualizar que o **terraglue** comporta também a "ingestão" (ou simplesmente o *upload*) de alguns dados na conta alvo AWS para servirem de insumos de execução de um job Glue também implementado como exemplo. Trata-se de alguns arquivos do conjunto de dados [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) o qual será detalhado logo a seguir.

___

## Detalhes Técnicos de Construção

Falar sobre módulos terraform

___

## Sobre as fontes de dados utilizadas

Falar sobre BR Ecommerce (link Kaggle)

___

## Detalhes Técnicos de Construção

Falar sobre módulos terraform

___

## Passo a passo de utilização do projeto

Finalmente...