<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/01-header-tests.png?raw=true" alt="terraglue-logo">
</div>


## Table of Contents
- [Table of Contents](#table-of-contents)
- [Uma breve introdução sobre testes](#uma-breve-introdução-sobre-testes)
  - [Desafios em testar jobs do Glue](#desafios-em-testar-jobs-do-glue)
  - [Escopo e abordagem](#escopo-e-abordagem)
- [Preparando o ambiente](#preparando-o-ambiente)
  - [Instalação do Docker](#instalação-do-docker)
  - [Obtenção da imagem do Glue para uso local](#obtenção-da-imagem-do-glue-para-uso-local)
  - [Configurando credenciais da AWS](#configurando-credenciais-da-aws)
  - [Extensão para conexão remota via VSCode](#extensão-para-conexão-remota-via-vscode)
  - [Inicializando o container](#inicializando-o-container)
  - [Utilizando VSCode para conexão com o container](#utilizando-vscode-para-conexão-com-o-container)
  - [Executando a primeira rodada de testes no container](#executando-a-primeira-rodada-de-testes-no-container)
- [Suíte de testes já disponibilizada no terraglue](#suíte-de-testes-já-disponibilizada-no-terraglue)
  - [Testando entradas do usuário](#testando-entradas-do-usuário)
  - [Testando funcionalidades da classe GlueJobManager](#testando-funcionalidades-da-classe-gluejobmanager)
  - [Testando funcionalidades da classe GlueETLManager](#testando-funcionalidades-da-classe-glueetlmanager)
  - [Testando funcionalidades da classe GlueTransformationManager](#testando-funcionalidades-da-classe-gluetransformationmanager)
- [Continue navegando nas documentações](#continue-navegando-nas-documentações)

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

Como exemplo prático de instalação em um ambiente Windows, após a execução do procedimento indicado, o usuário terá em mãos o Docker Desktop instalado e pronto para a uso.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-docker-desktop.png?raw=true" alt="docker-desktop-on-windows">
</div>
</details>

Também é possível executar o comando `docker --version` no terminal ou prompt de comando para validar a correta instalação da ferramenta.

### Obtenção da imagem do Glue para uso local

Após o *download* e a instalação do Docker, é preciso obter a imagem reponsável por alocar todas as dependências necessárias para a execução local de *jobs* do Glue. No decorrer do tempo, diferentes imagens de diferentes versões do Glue foram lançadas, cada uma contendo os requisitos necessários e adequados à respectiva versão designada. No atual período de desenvolvimento desta documentação, a imagem que simula as dependências do Glue 3.0 será utilizada. Para maiores informações sobre imagens de versões anteriores, é possível consultar o [github oficial da awslabs](https://github.com/awslabs/aws-glue-libs).

Assim, para obter a imagem acima referenciada, basta abrir o terminal e digitar o seguinte comando:

```bash
docker pull amazon/aws-glue-libs:glue_libs_3.0.0_image_01
```

A nova imagem estará, então, disponível para uso.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-docker-desktop-images.png?raw=true" alt="docker-glue-images">
</div>
</details>

Alternativamente, é possível analisar se a imagem foi obtido com sucesso através da execução do comando `docker image ls` no terminal.

### Configurando credenciais da AWS

Para que seja possível realizar chamadas de API na AWS através do *container*, é preciso configurar as chaves de acesso do usuário. Dessa forma, com a ACCESS_KEY_ID e a SECRET_ACCESS_KEY em mãos, basta digitar o seguinte comando no terminal e seguir as orientações solicitadas na própria tela:

```bash
aws configure
```

### Extensão para conexão remota via VSCode

Para facilitar o desenvolvimento de código e a execução de testes, o uso de uma IDE é altamente indicado. Considerando o VS Code como uma forma de exemplificar este processo, basta instalar a extensão [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers#:~:text=The%20Visual%20Studio%20Code%20Dev,Studio%20Code's%20full%20feature%20set.).

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-vscode-dev-containers.png?raw=true" alt="vscode-dev-containers-extension">
</div>
</details>


### Inicializando o container

Antes de dar o tão aguardo primeiro passo na utilização de um container Docker para uso local do Glue, é importante repassar o *checklist* de atividades necessárias para o sucesso da operação:

  - ✅ Docker instalado
  - ✅ Imagem Glue obtida
  - ✅ Credenciais AWS configuradas
  - ✅ IDE configurada (opcional)

Assim, o comando abaixo pode ser utilizado em sistemas Windows para execução do *container* Docker com a imagem do Glue. Adaptações podem ser realizadas de acordo com o sistema operacional utilizado e a localização dos diretórios usados como alvo.

```bash
set AWS_CONFIG_PATH=C:\Users\%username%\.aws
set AWS_PROFILE_NAME=default
set REPO_PATH=C:\Users\%username%\OneDrive\dev\workspaces\terraglue

docker run -it -v %AWS_CONFIG_PATH%:/home/glue_user/.aws -v %REPO_PATH%:/home/glue_user/workspace/terraglue -e AWS_PROFILE=%AWS_PROFILE_NAME% -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 --name terraglue amazon/aws-glue-libs:glue_libs_3.0.0_image_01 pyspark
```

Para entender um pouco mais sobre o comando acima utilizado é preciso navegar brevemente na [documentação do Docker](https://docs.docker.com/engine/reference/commandline/run/) para entender alguns dos parâmetros configurados. Entre eles, é possível detalhar:

| **Parâmetro** | **Descrição** | **Aplicação no comando** |
| :-- | :-- | :-- |
| `-i` ou `--interactive` | Mantém a entrada padrão (STDIN) aberta | [Link para entendimento do comando](https://docs.docker.com/engine/reference/commandline/run/#-assign-name-and-allocate-pseudo-tty---name--it) |
| `-t` ou `--tty` | Aloca um pseudo-TTY | [Link para entendimento do comando](https://docs.docker.com/engine/reference/commandline/run/#-assign-name-and-allocate-pseudo-tty---name--it) |
| `-v` ou `--volume` | Vincula um volume local com um caminho no container | Vínculo entre o diretório de credenciais da AWS e do repositório alvo a ser utilizado com seus respectivos caminhos acessíveis via *container* |
| `-e` ou `--env` | Estabelece variáveis de ambiente | Configura o perfil de credenciais como variáveis de ambiente do *container* para facilitar as chamadas de API para a AWS |
| `-rm` | Automaticamente remove o *container* ao sair | Automaticamente remove o *container* ao sair |
| `-p` ou `--publish` | Publica portas do *container* no servidor | Vincula portas 4040 e 18080 do *container* para as mesmas portas do *local host* do usuário para acesso externo |
| `--name` | Define um nome para o *container* | Serve para identificar o *container* no Docker Desktop |

Em caso de sucesso da execução do comando acima, o usuário verá, em seu terminal, o *shell* do `pyspark` pronto para uso. Nele, uma sessão Spark se faz presente e permite com que o usuário execute códigos diretamente pelo *container*, incluindoa importação de bibliotecas do Glue que não funcionavam anteriormente no ambiente local.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-docker-glue-pyspark.png?raw=true" alt="tests-docker-glue-pyspark">
</div>
</details>

Ainda sim, é possível aprimorar a experiência de uso da imagem Glue através de um container do que simplesmente utilizar o terminal. Para isso, a próxima e derradeira seção utiliza o VS Code e a extensão Dev Containers para proporcionar uma forma dinâmica de realizar operações com o Glue localmente.

### Utilizando VSCode para conexão com o container

Com o *container* em execução, o usuário pode acessar o Visual Studio Code e abrir um diretório alvo (ex: terraglue) para conexão com o *container*. Para tal, basta acessar o menu lateral esquerdo *Remote Explorer* e visualizar o *container* alvo abaixo de "Dev Containers":

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-vscode-remote-explorer.png?raw=true" alt="tests-vscode-remote-explorer">
</div>
</details>

Assim, basta clicar com o botão direito do mouse e selecionar a opção *Attach to Container*. Com isso, uma nova janela do VSCode será aberta e o usuário terá a possibilidade de utilizar a IDE para desenvolver e executar comando de uma forma mais fácil e dinâmica.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-vscode-container-attached.png?raw=true" alt="tests-vscode-container-attached">
</div>
</details>

### Executando a primeira rodada de testes no container

O terraglue, como produto, já proporciona ao usuário uma suíte de testes minimamente relevante para uso e adaptação, a qual será explicada em detalhes na próxima seção deste material. Como uma forma de validar toda a jornada de preparação aqui estabelecida, o usuário conectado ao *container* pode executar a seguinte sequência de comandos abaixo para realizar sua primeira validação de testes unitários no Glue:

1. Atualização de bibliotecas Python para correta execução dos testes

```bash
cd terraglue/
pip install --upgrade pip -r app/requirements-container.txt
```

2. Execução de toda a suíte de testes pré programada para o usuário

```bash
pytest app/ -vv --color=yes --cov=./ --cov-report=xml
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-pytest-container.png?raw=true" alt="tests-pytest-container">
</div>
</details>

Alternativamente, o usuário pode executar o comando para execução dos testes em conjunto ao comando de inicialização do container (`docker run`). Nesse formato, caso o usuário já tenha testes unitários desenvolvidos e queira, de forma rápida e objetiva, executar a suíte sem entrar diretamente no container, o seguinte comando pode ser utilizado:

```bash
set AWS_CONFIG_PATH=C:\Users\%username%\.aws
set AWS_PROFILE_NAME=default
set REPO_PATH=C:\Users\%username%\OneDrive\dev\workspaces\terraglue

docker run -it -v %AWS_CONFIG_PATH%:/home/glue_user/.aws -v %REPO_PATH%:/home/glue_user/workspace/terraglue -e AWS_PROFILE=%AWS_PROFILE_NAME% -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 --name terraglue amazon/aws-glue-libs:glue_libs_3.0.0_image_01 -c "cd terraglue && pip install --upgrade pip -r app/requirements-container.txt && pytest app/ -vv --color=yes --cov=./ --cov-report=xml"
```

> **Note**
> Para detalhes adicionais, é possível consumir a esteira de CI construída para o repositório terraglue. Nela, um step específico para execução dos testes unitários em containers docker foi configurado para validar a aplicação a cada push nas branches develop e main.

E assim, foi possível concluir todas as etapas de preparação e primeiros passos na disponibilização de uma forma isolada de executar e testar *jobs* do Glue utilizando um *container* Docker com uma imagem personalizada com todas as dependências necessárias. Este procedimento pode acelerar grandemente todo e qualquer processo de execução e validação de funcionalidades e aplicações Spark a serem posteriormente migradas e implantadas como *jobs* do Glue.

Na próxima seção, algumas explicações teóricas sobre os testes disponibilizados para o terraglue serão forencidas para que o usuário ganhe ainda mais autonomia no processo.
___

## Suíte de testes já disponibilizada no terraglue

No início desta documentação, foi possível explorar alguns desafios extremamente importantes no que tange a construção de testes envolvendo *jobs* do Glue na AWS. Visando endereçar e solucionar grande parte dos problemas citados, o **terraglue** proporciona, por natureza, um conjunto de testes unitários prontos para serem utilizados, adaptados e aprimorados de acordo com as especifidades de cada projeto construído a partir de sua base.

Sendo um produto de prateleira com suas funcionalidades intrínsecas programadas para facilitar e acelerar o desenvolvimento de *jobs* do Glue na AWS, nada mais coerente do que testar se tais funcionalidades estão realmente de acordo com o esperado, seja validando configurações particulares do usuário em termos de definição de variáveis ou mesmo o comportamento de métodos específicos do módulo `terraglue.py`.

Com isso em mente, uma série de testes unitários foram desenvolvidos e categorizados de acordo com seus respectivos propósitos, sendo eles:

| 🌎 <br> **Universo de testagem** | 🐍 <br> **Referência de script de teste** |  🛡️ <br> **Quantidade de testes** | 📍 <br> **Descrição e aplicação** | 🛠️ <br> **Usuário precisa adaptar?**
| :--: | :--: | :--: | :--: | :--: |
| Entradas do usuário | [`test_01_user_inputs.py`](https://github.com/ThiagoPanini/terraglue/blob/main/app/tests/test_01_user_inputs.py) | 5 | Valida *inputs* do usuário relacionados à definição de variáveis no script principal da aplicação | ✅ Não |
| Classe `GlueJobManager` | [`test_02_job_manager.py`](https://github.com/ThiagoPanini/terraglue/blob/main/app/tests/test_02_job_manager.py) | 5 | Valida elementos de uma aplicação Spark e um *job* Glue criados como insumos de execução do projeto | ✅ Não |
| Classe `GlueETLManager` | [`test_03_etl_manager.py`](https://github.com/ThiagoPanini/terraglue/blob/main/app/tests/test_03_etl_manager.py) | 9 | Valida método estáticos de transformação e funcionalidades adicionais do módulo | ✅ Não |
| Script principal | [`test_04_main.py`](https://github.com/ThiagoPanini/terraglue/blob/main/app/tests/test_04_main.py) | 17 | Valida regras de negócio específicas vinculadas ao job codificado pelo usuário | 🚨 Sim |
| | | **Total: 36**

Conforme detalhado na tabela acima, além de entregar um ambiente totalmente personalizado para a execução de *jobs* do Glue e uma aplicação de exemplo utilizando uma forma altamente disruptiva de organizar uma aplicação Spark, o **terraglue** também traz consigo uma suíte completa de testes capaz de ser utilizada pelo usuário para os mais variados propósitos.

Se algum dia testar *jobs* do Glue pôde ser considerada uma tarefa obscura e de extrema complexidade, com o **terraglue** as chances de aprimorar e otimizar este processo são tremendas!


### Testando entradas do usuário

O primeiro módulo de testes a ser detalhado envolve a validação de entredas fornecidas pelo usuário, sejam estas materializadas como variáveis da aplicação principal ou até mesmo parâmetros do *job* declarados na ferramenta de IaC.

> ✅ Este módulo de testes é característico do terraglue como solução e, dessa forma, não exige qualquer adaptação por parte do usuário. As validações consolidadas no referido script consolidam situações rígidas que servem para garantir a execução das funcionalidades do próprio terraglue.

Na prática, o modelo de aplicação Spark fornecida no **terraglue** exige algumas configurações mínimas inseridas pelo usuário, sendo elas:

- Definição de parâmetros obrigatórios do *job* Glue
- Adaptação da variável `ARGV_LIST` com parâmetros do *job* a serem lidos
- Adaptação da variável `DATA_DICT` com referências às origens de dados

Cada um dos elementos acima configuram atuações onde o usuário pode criar, adaptar e configurar situações por conta própria. Dessa forma, o script `test_01_user_inputs.py` traz consigo algumas funções de testes para validar se as adaptações do usuário foram realizadas com a devida coerência esperada dentro da dinâmica de funcionamento da aplicação.

Para facilitar análises pontuais por parte do usuário, a [marker customizada](https://docs.pytest.org/en/7.1.x/example/markers.html) `user_input` foi configurada e inserida de modo a proporcionar, por exemplo, uma execução específica apenas nos testes que competem à esta categoria através do seguinte comando:

```bash
pytest app/ -vv -m user_input
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-pytest-user-input.png?raw=true" alt="tests-pytest-user-input">
</div>
</details>


### Testando funcionalidades da classe GlueJobManager

O segundo módulo de testes se faz presente como uma forma eficiente de testar a obtenção dos insumos que "fazem a magia do Glue acontecer". Nele, o grande foco de testagem está nos métodos da classe `GlueJobManager` que, por sua vez, é a responsável por assumir atributos utilizados em grande parte das operações do Glue durante o processo de ETL, como por exemplo, os elementos de contexto e sessão do Spark.

> ✅ Este módulo de testes é característico do terraglue como solução e, dessa forma, não exige qualquer adaptação por parte do usuário. As validações consolidadas no referido script consolidam situações rígidas que servem para garantir a execução das funcionalidades do próprio terraglue.

Considerando a construção da referida classe e das funcionalidades nela consolidadas, os testes alocados no script `test_02_job_manager.py` visam garantir a obtenção de todos os elementos necessários para a correta execução do *job* Glue.

Para visualizar e testar apenas esta parcela da aplicação, o usuário pode executar o comando abaixo filtrando a [marker customizada](https://docs.pytest.org/en/7.1.x/example/markers.html) `job_manager` disponibilizada para esta finalidade.

```bash
pytest app/ -vv -m job_manager
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-pytest-job-manager.png?raw=true" alt="tests-pytest-job-manager">
</div>
</details>

### Testando funcionalidades da classe GlueETLManager

Em sequência aos módulos de teste, é chegado o momento de validar algumas das funcionalidades de prateleira disponibilizadas como métodos da classe `GlueETLManager` no módulo `terraglue.py`. Como se sabe, é nesta classe onde alguns métodos estáticos de transformação de dados estão alocados e disponibilizados para auxiliar o usuário em algumas operações comumente realizadas em aplicações Spark, como por exemplo, a adição de partições em DataFrames, o reparticionamento de DataFrames, entre outras. Validar tais funcionalidades é essencial para garantir que o usuário terá em mãos métodos de transformação consistentes para adicionar em suas *pipelines*.

> ✅ Este módulo de testes é característico do terraglue como solução e, dessa forma, não exige qualquer adaptação por parte do usuário. As validações consolidadas no referido script consolidam situações rígidas que servem para garantir a execução das funcionalidades do próprio terraglue.

Neste script de testes, o usuário poderá encontrar validações associadas aos resultados esperados de alguns métodos de transformação agnósticos criados para proporcionar um maior leque de possibilidades para usuários que querem codificar seus próprios *jobs* do Glue e utilizar funcionalidades prontas para as mais variadas atuações.

Para visualizar e testar apenas esta parcela da aplicação, o usuário pode executar o comando abaixo filtrando a [marker customizada](https://docs.pytest.org/en/7.1.x/example/markers.html) `etl_manager` disponibilizada para esta finalidade.

```bash
pytest app/ -vv -m etl_manager
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/docker-tests/tests-pytest-etl-manager.png?raw=true" alt="tests-pytest-etl-manager">
</div>
</details>

### Testando funcionalidades da classe GlueTransformationManager

Por fim, o último e derradeiro script de testes disponibilizado para o usuário como uma das funcionalidades do **terraglue** envolve a construção de funções de testes relacionadas às regras de negócio da aplicação Spark submetida como um Glue *job* na AWS. Em linhas gerais, é aqui onde o usuário focará seus esforços de adaptação das funções de acordo com suas próprias regras de validações codificadas nos métodos de transformação da classe `GlueTransformationManager`.

> 🚨 Este módulo de testes é construído com base em transformações específicas codificadas pelo usuário de acordo com as regras de negócio a serem implementadas em seu processo de ETL. Assim sendo, este script precisa obrigatoriamente ser alterado e adaptado pelo usuário que utilizar o terraglue como uma forma de padronizar sua aplicação Spark submetida como job do Glue.

As funcionalidades testadas neste script competem ao que se tem programado no script principal da aplicação envolvendo a construção de uma tabela na camada SoT contendo dados do e-commerce brasileiro. Dessa forma, a dinâmica de testes implementada teve como premissa a execução dos seguintes passos:

1. Extração de amostras para cada uma das origens do processo de ETL
2. Construção de testes de quantidade de registros para cada origem
3. Construção de testes de *schema* resultante para cada origem

Existem, ainda, diferentes testes que podem ser implementados pelo usuário, como por exemplo, a validação da existência de dados nulos, duplicidades, regras específicas de negócio e muito mais. Cabe ao mesmo decidir quais funcionalidades testar e como implementá-las.

___

## Continue navegando nas documentações

- [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main)
- [2. Implantando e conhecendo a infraestrutura](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md)
- [3. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/APP.md)
- [4. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/EXAMPLES.md)
- 👉 [5. Testes unitários em jobs do Glue na AWS](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/TESTS.md) *Você está aqui!*

