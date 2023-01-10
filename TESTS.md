*Detalhes técnicos sobre a construção e execução de testes unitários de jobs Glue*

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Antes de começar](#antes-de-começar)
- [Uma breve introdução sobre testes](#uma-breve-introdução-sobre-testes)
  - [Desafios em testar jobs do Glue](#desafios-em-testar-jobs-do-glue)
  - [Escopo e abordagem](#escopo-e-abordagem)
- [Preparando o ambiente](#preparando-o-ambiente)
  - [Instalação do Docker](#instalação-do-docker)
- [Suíte de testes já disponibilizada no terraglue](#suíte-de-testes-já-disponibilizada-no-terraglue)
___

## Antes de começar

> Antes de detalhar, de fato, os procedimentos utilizados na implementação de testes unitários de jobs Glue na AWS, é importante garantir que a jornada de aprendizado no terraglue foi concluída com êxito. Para isso, os links abaixos podem ser de grande utilidade!

- [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main)
- [2. Instalação e primeiros passos](https://github.com/ThiagoPanini/terraglue/blob/main/GETTINGSTARTED.md) 
- [3. Infraestrutura provisionada](https://github.com/ThiagoPanini/terraglue/blob/main/INFRA.md) 
- [4. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/APP.md) 
-  [5. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/EXAMPLES.md)
- 👉 [6. Testes unitários em jobs do Glue na AWS](https://github.com/ThiagoPanini/terraglue/blob/main/TESTS.md) *Você está aqui!*

___

## Uma breve introdução sobre testes

Existem diferentes formas de se testar um código e os benefícios relacionados à construção de aplicações com uma boa cobertura de testes são muitos. Sem a pretensão de ser uma verdadeira documentação de prateleira sobre testes e todas as suas vertentes, esta seção tem como principal objetivo apresentar, ao usuário, algumas formas distintas de compreender termos e etapas presentes na jornada de aprendizado sobre o assunto.

Existem diferentes categorias atreladas a testes em aplicações. Abstraindo grande parte dos detalhes técnicos por trás deste vasto universo, é importante definir, a princípio, dois tipos de testes comumente presentes no dia a dia de um desenvolvedor:

- [Testes unitários](https://machinelearningmastery.com/a-gentle-introduction-to-unit-testing-in-python/): como o próprio nome sugere, testes unitários (ou testes de unidade) são aqueles direcionados para um único componente do código, normalmente modularizado e materializado como uma função. A ideia é validar se esta pequena parte da aplicação (unidade) está funcionando como deveria
- [Testes de integração](https://www.fullstackpython.com/integration-testing.html): já os testes de integração abordam a validação de múltiplos componentes de uma aplicação, permitindo garantir que as diferentes partes do código, juntas, funcionam de maneira adequada.

> 🚨 Como mencionado previamente, abordar todos os pormenores atrelados à testagem de aplicações exigiria uma documentação exclusiva. Existem livros, blogs, vídeos e uma série de materiais com foco específico no assunto e que podem ser consumidos em caso de maior interesse por parte do leitor.

### Desafios em testar jobs do Glue

Como um serviço gerenciado da AWS para a execução de *jobs* de ETL capazes de processar grandes volumes de dados de forma paralela em múltiplos nós de um *cluster* de computadores, o Glue pode ser considerado um elemento particular no que diz respeito a codificação de testes.

Por sua própria definição, é preciso possuir uma certa maturidade para identificar exatamente os pontos e os componentes unitários a serem testados. Além disso, por possuir algumas bibliotecas próprias (`awsglue`) com módulos auxiliares (`awsglue.utils`, `awsglue.context`, `awsglue.job`, `awsglue.dynamicframe`, entre outros), existe uma certa complexidade em preparar um ambiente local para desenvolvimento e construção de testes de unidade capazes de endereçar as funcionalidades a serem validadas.

Em outras palavras, qualquer tentativa de testar *jobs* do Glue localmente sem a devida preparação do ambiente fatalmente resultará em um erro de importação de bibliotecas, como por exemplo, o `ModuleNotFoundError: No module named 'awsglue'`.

### Escopo e abordagem

Dito isso, o conteúdo aqui alocado será focado na utilização do *framework* [`pytest`](https://docs.pytest.org/en/7.1.x/contents.html) para a codificação de **testes unitários** de *jobs* do Glue a serem executados na AWS com todas as funcionalidades presentes no [terraglue](https://github.com/ThiagoPanini/terraglue) através do uso de um *container* [Docker](http://docker.com/).

Grande parte da base técnica e prática para a exemplificação dos passos aqui alocados está presente no [seguinte artigo](https://aws.amazon.com/blogs/big-data/develop-and-test-aws-glue-version-3-0-jobs-locally-using-a-docker-container/) e sua leitura é altamente recomendada para um completo entendimento sobre o procedimento adotado. Mesmo assim, esta não é uma tarefa trivial e é justamente por isto que esta documentação se faz presente.

___

## Preparando o ambiente

De forma resumida, a lista de pré requisitos abaixo precisa ser cumprida para possibilitar o desenvolvimento e a execução de testes unitários em *jobs* do Glue:

1. 🐋 Instalação do [Docker](https://www.docker.com/)
2. ⬇️ Pull da [imagem Glue](https://hub.docker.com/r/amazon/aws-glue-libs) diretamente do Docker Hub
3. 🔑 Configuração das chaves de acesso programático do usuário AWS
4. 💻 Execução do comando para execução do container de acordo com a tarefa a ser realizada

### Instalação do Docker

Para a instalação do Docker em seu sistema, basta seguir as orientações presentes no [site oficial](https://docs.docker.com/get-docker/) de acordo com seu sistema operacional de trabalho, seja ele [Mac](https://docs.docker.com/desktop/install/mac-install/), [Windows](https://docs.docker.com/desktop/install/windows-install/) ou [Linux](https://docs.docker.com/desktop/install/linux-install/).

Como exemplo prático de instalação em um ambiente Windows, após a execução do procedimento indicado, o usuário terá em mãos 

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://raw.githubusercontent.com/ThiagoPanini/terraglue/develop/docs/imgs/tests-docker-desktop.png" alt="docker-desktop-on-windows">
</div>
</details>

___

## Suíte de testes já disponibilizada no terraglue

