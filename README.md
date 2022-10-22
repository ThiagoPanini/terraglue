# terraglue
*Auxiliando desenvolvedores, engenheiros e analistas a implantar e testar jobs do Glue na AWS*


## Table of Contents
- [terraglue](#terraglue)
  - [Table of Contents](#table-of-contents)
  - [O que é o terraglue?](#o-que-é-o-terraglue)
  - [Motivadores e principais desafios](#motivadores-e-principais-desafios)
  - [Quem pode utilizar o terraglue?](#quem-pode-utilizar-o-terraglue)
  - [Visão de arquitetura](#visão-de-arquitetura)
  - [Fontes de Dados Utilizadas](#fontes-de-dados-utilizadas)
  - [Detalhes Técnicos de Construção](#detalhes-técnicos-de-construção)

___

## O que é o terraglue?

Imagine o seguinte cenário: você é alguém da área de dados com o desejo de aprender e explorar soluções envolvendo o processamento de dados na AWS, em especial o serviço [AWS Glue](https://aws.amazon.com/glue/) e todos os seus componentes relacionado.

Nessa jornada, você procura por documentações, pesquisa em fóruns, assiste vídeos nas mais variadas plataformas mas, ainda sim, não sente a confiança necessária para entender e aplicar, de fato, todas as etapas de construção de um job de processamento de dados *end to end* na nuvem. Seria ótimo ter um ambiente próprio, totalmente configurado e de fácil implantação, não é mesmo?

E assim, para sanar essa e outras dificuldades, nasce o **terraglue** como um projeto desenvolvido exclusivamente para facilitar e acelerar o aprendizado em serviços como AWS Glue, [Athena](https://aws.amazon.com/athena/) e [Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html) em toda a dinâmica de obtenção, processamento e escrita de dados (ETL) na nuvem. Embarque nesta jornada e tenha em mãos um ferramental extremamente rico e de fácil utilização para se especializar no universo analítico da AWS.

___

## Motivadores e principais desafios

Uma vez apresentado o projeto, é importante destacar que o **terraglue** possui uma essência altamente dinâmica, isto é, suas funcionalidades abrem margem para uma série de possibilidades e ganhos. Para que se tenha uma ideia de todas as suas possíveis aplicações, as perguntas abaixo representam alguns obstáculos, dores e desafios reais que podem ser devidamente solucionadas pelo **terraglue**:

- 💡 *"Como consigo criar um job do Glue no console AWS e quais as configurações adequadas?"*
- 💡 *"Mesmo que eu consiga criar um job, quais dados de exemplo posso utilizar para meu processo de ETL?"*
- 💡 *"GlueContext? DynamicFrame? Como todos esses elementos se encaixam na dinâmica de um job do Glue?"*
- 💡 *"Será que não há nenhum exemplo prático disponível para servir de base?"*
- 💡 *"No final de tudo, eu consigo automatizar toda a infraestrutura necessária para implantar um job do Glue na AWS?"*

Ansioso para conhecer mais sobre o projeto? Ainda nesta documentação, toda sua arquitetura será apresentada e um completo tutorial de utilização será fornecido. Continue acompanhando!
___

## Quem pode utilizar o terraglue?

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

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-diagram-resources.png?raw=true" alt="terraglue-resources">
</div>


___

## Fontes de Dados Utilizadas

Falar sobre BR Ecommerce (link Kaggle)

___

## Detalhes Técnicos de Construção

Falar sobre módulos terraform