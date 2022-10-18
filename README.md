# terraglue
*Auxiliando desenvolvedores, engenheiros e analistas a implantar e testar jobs do Glue na AWS*

___

## Table of Contents
- [terraglue](#terraglue)
  - [Table of Contents](#table-of-contents)
  - [Sobre o Repositório](#sobre-o-repositório)
  - [Visão de Arquitetura](#visão-de-arquitetura)
  - [Fontes de Dados Utilizadas](#fontes-de-dados-utilizadas)
  - [Detalhes Técnicos de Construção](#detalhes-técnicos-de-construção)

___

## Sobre o Repositório

Imagine o seguinte cenário: você é alguém da área de dados que pretende aprender mais sobre o AWS Glue através da criação de *jobs* exploratórios criados para fins de aprendizado. Com este propósito, você se vê em muitos cenários de dúvidas, envolvendo não apenas a parte técnica em si, mas também tudo o que engloba a infraestrutura necessária para que sua jornada de aprendizado possa, finalmente, ter início. Algumas perguntas surgem nesse caminho:

- *"Como consigo criar um job do Glue no console AWS e quais as configurações adequadas?"*
- *"Mesmo que eu consiga criar um job, quais dados de exemplo posso utilizar?"*
- *"Mesmo que eu tenha os dados, como eu consigo codificar um job considerando as bibliotecas do Glue?"*
- *"Será que não há nenhum exemplo prático disponível para servir de exemplo?"*

Para fornecer as respostas para as perguntas acima e solucionar os problemas que eventualmente possam surgir durante a longa e complexa jornada de aprendizado envolvendo o serviço AWS Glue, o projeto **terraglue** surge! Sua concepção basea-se no simples fato de fornecer uma forma automática e replicável de implantação de todos os recursos necessárias para implantação de um job do Glue que pode ser utilizado para fins de aprendizado.

| | |
| :-- | :-- |
| 🛠 **IaC Runtime**| Terraform |
| ☁️ **Cloud Provider** | AWS |
| 📦 **Cloud Services** | S3, IAM, Glue, Data Catalog, Athena |
| | |

Clone, observe, aprenda, implante e modifique as práticas aqui estabelecidas para **acelerar** sua jornada de aprendizado no ambiente analítico da AWS!

___

## Visão de Arquitetura

Considerando os objetivos acima exemplificados, o projeto **terraglue** possui uma arquitetura repleta de elementos. Até que seu lançamento pudesse ser consolidado, muitos foram os testes realizados e muitas as adequações propostas. Na visão do usuário, o consumo das funcionalidades do projeto pode ser consolidado da seguinte forma:


<div align="center">
    <br><img src=" alt="terraglue-user-view">
</div>

Detalhando ainda mais os recursos a serem implantad

___

## Fontes de Dados Utilizadas

Falar sobre BR Ecommerce (link Kaggle)

___

## Detalhes Técnicos de Construção

Falar sobre módulos terraform