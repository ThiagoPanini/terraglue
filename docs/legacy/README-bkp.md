<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/assets/imgs/header-readme.png?raw=true" alt="terraglue-logo">
</div>

<div align="center">
  <br>
  
  ![GitHub release (latest by date)](https://img.shields.io/github/v/release/ThiagoPanini/terraglue?color=purple)
  ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ThiagoPanini/terraglue?color=blue)
  ![CI workflow](https://img.shields.io/github/actions/workflow/status/ThiagoPanini/terraglue/ci-terraglue-main.yml?label=ci)
  [![codecov](https://codecov.io/github/ThiagoPanini/terraglue/branch/main/graph/badge.svg?token=7HI1YGS4AA)](https://codecov.io/github/ThiagoPanini/terraglue)

</div>

## Table of Contents
- [Table of Contents](#table-of-contents)
- [O que é o terraglue?](#o-que-é-o-terraglue)
  - [Público alvo](#público-alvo)
  - [Pré requisitos](#pré-requisitos)
  - [Primeiros passos](#primeiros-passos)
- [Arquitetura e organização do repositório](#arquitetura-e-organização-do-repositório)
- [Está interessado e quer saber mais?](#está-interessado-e-quer-saber-mais)
  - [A história por trás da criação](#a-história-por-trás-da-criação)
  - [Uma jornada completa de consumo](#uma-jornada-completa-de-consumo)
  - [Contribuindo](#contribuindo)
  - [FAQ](#faq)
- [Contatos](#contatos)
- [Referências](#referências)

___

## O que é o terraglue?

O **terraglue** é um produto criado para facilitar a jornada de aprendizado, utilização e otimização de jobs do Glue na AWS. Em essência, é possível dividir suas funcionalidades em dois grandes grupos:

- 🛠️ **Infra:** com o terraglue, o usuário pode implantar toda a infraestrutura necessária para executar jobs do Glue em seu ambiente sandbox AWS, incluindo buckets s3, roles IAM e tabelas no Data Catalog.
- 🚀 **Aplicação:** além disso, um modelo de aplicação Spark é disponibilizado com uma série de classes e métodos prontos para uso e que abstraem muitas operações comuns usadas em jobs Glue.


### Público alvo

Você pretende começar a utilizar o Glue na AWS e não sabe por onde começar? Já utiliza o serviço e quer otimizar aquele seu job com milhares de linhas de código? Gostaria de usar funções e métodos prontos de transformação de dados com Spark? Tá quebrando a cabeça com testes unitários e precisa de um norte?

Se a resposta foi "sim" para alguma das perguntas acima ou se você quer simplesmente mergulhar em alvo novo, o **terraglue** é o produto ideal pra você!

### Pré requisitos

Utilizar o **terraglue** é rápido e intuitivo. Para isso, basta ter:

- ☁️ [Conta AWS](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) disponível para uso
- 🔑 [Acesso programático](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html) à conta através das chaves `access_key_id` e `secret_access_key`
- ⛏ [Terraform](https://www.terraform.io/) instalado (versão >=1.0)

### Primeiros passos

A primeira etapa necessária para ter em mãos todas as funcionalidades do projeto é realizando o *clone* deste repositório através do comando:

```bash
git clone https://github.com/ThiagoPanini/terraglue.git
```

Após isso, basta navegar até o diretório recém clonado e executar os comandos Terraform para inicializar os módulos, planejar e realizar as implantações:

```bash
# Navegando até o diretório de infra
cd terraglue/infra

# Inicializando os módulos e realizando a implantação
terraform init
terraform plan
terraform apply
```

Pronto! Agora você tem aplicada à conta AWS todos os elementos necessários para começar sua jornada de aprendizado no Glue da melhor forma possível! Para maiores detalhes, preparei um [tutorial detalhado](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md) de primeiros passos na solução. Se quiser entender melhor toda a arquitetura por trás da iniciativa, não deixe de continuar nesta documentação.

___

## Arquitetura e organização do repositório

Agora que você já conhece um pouco mais sobre o projeto, é chegado o momento de apresentar toda a arquitetura que está por trás das funcionalidades introduzidas. No final do dia, o **terraglue** é um projeto de IaC (*Infrastructure as Code*) construído com o *runtime* [Terraform](https://www.terraform.io/) e dividido em módulos responsáveis por implantar diferentes serviços AWS que, juntos, formam toda a dinâmica de consumo do projeto. Assim, o usuário obtém o código fonte disponibilizado neste repositório e executa os comandos específicos do runtime de IaC utilizado para realizar as implantações necessárias no ambiente alvo.

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/readme/diagram-user-view.png?raw=true" alt="terraglue-user-view">
</div>
<br>

Em uma visão mais técnica, os serviços declarados nos módulos Terraform são representados por:

- 🧺 Buckets S3 para armazenamento de dados e *assets*
- 🚨 Policies e role IAM para gerenciamento de acessos
- 🎲 Referências no catálogo de dados e workgroup do Athena
- 🪄 Job do Glue parametrizado com exemplo prático de uso

Assim, ao cumprir os requisitos e as ações evidenciadas pela imagem de arquitetura acima, o usuário poderá ter em mãos seu próprio "ambiente AWS portátil" composto dos seguintes recursos:

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/readme/diagram-product-view.png?raw=true" alt="terraglue-resources">
</div>
<br>

Considerando os insumos presentes, o repositório do **terraglue** está organizado da seguinte forma:

| 📂 **Diretório** | ⚙️ **Função** |
| :-- | :-- |
| `./app` | Aqui será possível encontrar o script Python disponibilizado como padrão para implantação de um job Glue na AWS seguindo as melhores práticas de código e documentação. O script considera um cenário de criação de uma base na camada [SoT](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/) (*Source of Truth*) utilizando dados de vendas online no [e-commerce brasileiro](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). |
| `./data` | Neste diretório, será possível identificar todas as fontes de dados disponibilizadas como exemplo para a execução de um job do Glue. Os dados estão presentes e organizados de modo a simular uma estrutura padrão de Data Lake em ambientes distribuídos, onde define-se o banco de dados, nome de tabela como diretórios pais em relação aos arquivos propriamente ditos (ex: `db/table/file.ext`). |
| `./docs` | Aqui o usuário poderá encontrar todos os diagramas e imagens utilizadas na documentação do projeto. |
| `./infra` | Neste diretório, será possível encontrar todas as declarações Terraform responsáveis pela implantação da infraestrutura necessária para utilização do projeto na AWS. Uma seção específica sobre esta parte será detalhada logo a seguir. |

___


## Está interessado e quer saber mais?

Após definir o que é o **terraglue** e fornecer uma visão macro sobre sua arquitetura de solução, é chegado o momento de fornecer alguns insumos e rotas fundamentais para materializar todo o valor intrínseco da iniciativa. 

### A história por trás da criação

> **Note**
> Esta seção serve apenas para fins de curiosidade. Se você está minimamente interessado em conhecer um pouco mais sobre a história de concepção da solução, clique no dropdown e tenha uma boa leitura 🤓

<details>
  <summary>🪄 Era uma vez um Engenheiro de Analytics...</summary>

  > ...que estava iniciando sua jornada de aprendizado no Glue. Ele não sabia por onde começar e, assim sendo, procurou alguns vídeos, leu algumas documentações e, enfim, se preparou para executar algo mais prático em seu ambiente pessoal. Em suas mãos, o tal Engenheiro tinha uma conta sandbox AWS e muita vontade de aprender.
  
  > No início, ele começou simulando algumas estruturas de armazenamento próximas ao que ele encontrava em seu ambiente de trabalho, como por exemplo, buckets s3 responsáveis por armazenar dados em diferentes camadas (SoR, SoT e Spec). Como sua conta de sandbox era efêmera e automaticamente excluída em um período de algumas horas, todos os dias o Engenheiro realizava o login em uma nova conta e criava manualmente os buckets para servirem de repositório para os arquivos. Falando nisso, a obtenção de dados públicos e a posterior ingestão no ambiente citado também fazia parte das tarefas manuais realizadas diariamente.
  
  > Realizar o upload dos arquivos não bastava pois, na dinâmica de uso do s3 como Data Lake, é preciso também catalogar os dados no Data Catalog da AWS, adicionando ainda mais esforço operacional na rotina do Engenheiro (e olha que nem chegamos no Glue ainda).

  > Em continuidade à preparação do ambiente, o Engenheiro se via agora perante a uma tarefa extremamente desafiadora: roles IAM. Quais permissões utilizar? Será preciso criar políticas específicas? O que o Glue precisa para funcionar? Depois de muito estudo, o Engenheiro conseguiu alcançar um conjunto de políticas definidas pontualmente para permitir que jobs do Glue sejam executados em seu ambiente. Agora, todos os dias, além da criação dos buckets, ingestão e catalogação dos arquivos, o Engenheiro também deveria criar políticas e pelo menos uma role IAM para poder iniciar sua jornada no Glue.

  > Por fim, após muito esforço operacional e muitas pedras quebradas, o Engenheiro conseguiu preparar todo seu ambiente para poder criar seu job do Glue e aprender a usá-lo com os dados públicos catalogados. Se os obstáculos até aqui não foram suficientes, o Engenheiro agora se via perante a um desafio de extrema complexidade envolvendo a dinâmica de criação de aplicações Spark dentro do Glue. GlueContext? DynamicFrame? SparkSession? O que significa tudo isso e como eu consigo simplesmente ler, transformar e catalogar meus dados?

  > Bom, neste momento a história do nosso protagonista começa a virar. Assim como em grandes filmes ou em renomados animes, é a partir deste ponto que o herói começa a nascer e todos os desafios começam a ser superados. Aos poucos, o Engenheiro percebe que os processos de preparação de ambiente arduamente replicados diariamente em seu ambiente poderiam, extraordinariamente, serem automatizados através de uma ferramenta de IaC.
  
  > E assim ele começa a desenvolver peças de código que criam buckets s3 de maneira automática sempre que ele entra em sua jornada diária de aprendizado. Além dos buckets, ele também codifica uma forma automática de fazer o upload e a catalogação de arquivos prontos para serem utilizados. As políticas e a role IAM também entram neste pacote e passam a ser criadas de maneira instantânea em seu novo projeto de automatização de infraestrutura. Por fim, a criação do job do Glue também é automatizada e, neste momento, o Engenheiro tem em suas mãos toda a infraestrutura necessária para usar o serviço Glue na AWS ao toque de um único comando. Entretanto, ainda faltava a cereja do bolo.

  > Uma vez automatizada a infra, o Engenheiro percebeu alguns padrões de código de aplicações Spark que poderiam facilitar a jornada de desenvolvimento dos usuários em jobs do Glue. Será mesmo que o usuário precisa instanciar um GlueContext no script principal de trabalho? Será que algum módulo adicional poderia abstrair esse passo? E assim, o Engenheiro começou a trabalhar em uma série de funcionalidades relevantes encapsuladas em um módulo adicional capaz de ser importado no script principal da aplicação, permitindo que os usuários se concentrem exclusivamente em seus respectivos métodos de transformação dos dados.

  > Com isso, agora não apenas toda uma infraestrutura seria provisionada, mas também todo um modelo de referência no desenvolvimento de aplicações Spark em jobs do Glue seria entregue ao usuário final. Estava pronto o MVP do terraglue.
</details>

...e viveram felizes para sempre sem *issues* no repositório!

___

### Uma jornada completa de consumo

Se tudo ainda está meio abstrato até aqui, fique tranquilo! Existe um conjunto massivo de documentações altamente detalhadas para que todo o poder do **terraglue** possa ser extraído por parte de seus usuários. O conjunto de links abaixo promete guiar o leitor para todas as jornadas presentes na dinâmica de uso da solução.


- 👉 [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main) *Você está aqui!*
- [2. Implantando e conhecendo a infraestrutura](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md) 
- [3. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/APP.md) 
- [4. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/EXAMPLES.md)
- [5. Testes unitários em jobs do Glue na AWS](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/TESTS.md)

___

### Contribuindo

Todos são muito bem vindos a contribuírem com evoluções e novas funcionalidades deste projeto carinhosamente disponibilizado para a comunidade. Para maiores detalhes sobre esse processo, visite o arquivo [CONTRIBUTING.md](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/CONTRIBUTING.md)

___

### FAQ

<details>
  <summary>📌 "Fiquei sabendo do terraglue por acaso. Como eu sei se ele pode me ajudar em algo?"</summary>

  > 💡 *Basicamente, o terraglue possui diferentes perfis de usuários candidatos que vão desde iniciantes até os mais experientes. Se você quer dar seus primeiros passos na AWS utilizando o Glue, aqui você poderá ter em mãos uma ferramenta capaz de proporcionar uma jornada end to end ao toque de um comando. Se você já tá imerso nessa jornada e tem dúvidas técnicas sobre aplicações Spark, testes unitários, módulos Python ou Terraform, aqui também é seu lugar!*
</details>

<details>
  <summary>📌 "Quero ativar em minha conta AWS um <i>toolkit</i> para aprender como funciona a dinâmica de uso do Glue na prática. Qual caminho devo seguir?"</summary>

  > 💡 *Para alcançar esse objetivo, basta seguir os passos presentes na documentação [Implantando e conhecendo a infraestrutura](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md). Nela, você encontrará todos os detalhes necessários para ter em suas mãos, ao toque de poucos comandos, toda uma infraestrutura pronta para contemplar sua jornada de uso do Glue na AWS.*
</details>

<details>
  <summary>📌 "Não estou interessado na infraestrutura em si, mas sim no modelo de aplicação Spark e nas funções prontas para uso em meu job Glue. Onde coleto mais informações a respeito e como consigo utilizar esses blocos de código prontos em minha aplicação?"</summary>

  > 💡 *Para este cenário, a documentação [Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/APP.md) poderá te guiar em todos os passos necessários para entender o modelo de aplicação Spark desenvolvido e como utilizá-lo em seus próprios projetos. Adicionalmente, a documentação [Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/EXAMPLES.md) pode ser um excelente complemento para analisar, etapa a etapa, todo o processo de obtenção e adaptação do modelo de aplicação Spark.*
</details>

<details>
  <summary>📌 "Já tenho um job Glue rodando em produção, mas tenho dificuldade em dar manutenção no mesmo por conta da complexidade da aplicação e da quantidade de linhas de código. Como posso usar o terraglue para otimizar esse processo?"</summary>

  > 💡 *O terraglue conta com um módulo adicional Python presente em <code>app/terraglue.py</code> com INÚMERAS funcionalidades encapsuladas e prontas para uso. Você pode adpatar seu código para usar este módulo e utilizar classes e métodos criadas especialmente para facilitar a jornada de desenvolvimento de aplicações Spark com as melhores práticas de desenvolvimento de código. Com essa dinâmica, você pode se preocupar única e exclusivamente em programar as transformações de dados necessárias para seu processo de ETL. Para o restante, conte com os métodos prontos do módulo <code>terraglue.py</code>.*
</details>

<details>
  <summary>📌 "Existem custos envolvidos para usar o terraglue?"</summary>

  > 💡 *Essa é uma pergunta muito interessante e importante. Não existem custos para usar o terraglue pois trata-se de uma solução open source e compartilhada com toda a comunidade. ENTRETANTO, é imprescindível citar que os recursos criados pelo terraglue em seus ambiente AWS eventualmente podem ocasionar custos. Portanto, é fundamental que os usuários do terraglue compreendam as possíveis taxas envolvidas com os serviços relacionados antes de utilizar a solução.*
</details>

___

## Contatos

- [Thiago Panini - LinkedIn](https://www.linkedin.com/in/thiago-panini/)
- [paninitechlab @ hashnode](https://panini.hashnode.dev/)

## Referências

**_AWS Glue_**
- [AWS - Glue Official Page](https://aws.amazon.com/glue/)
- [AWS - Jobs Parameters Used by AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html)
- [AWS - GlueContext Class](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html#aws-glue-api-crawler-pyspark-extensions-glue-context-create_dynamic_frame_from_catalog)
- [AWS - DynamicFrame Class](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
- [Stack Overflow - Job Failing by Job Bookmark Issue - Empty DataFrame](https://stackoverflow.com/questions/50992655/etl-job-failing-with-pyspark-sql-utils-analysisexception-in-aws-glue)
- [AWS - Calling AWS Glue APIs in Python](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html)
- [AWS - Using Python Libraries with AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#aws-glue-programming-python-libraries-zipping)
- [Spark Temporary Tables in Glue Jobs](https://stackoverflow.com/questions/53718221/aws-glue-data-catalog-temporary-tables-and-apache-spark-createorreplacetempview)
- [Medium - Understanding All AWS Glue Import Statements and Why We Need Them](https://aws.plainenglish.io/understanding-all-aws-glue-import-statements-and-why-we-need-them-59279c402224)
- [AWS - Develop and test AWS Glue jobs Locally using Docker](https://aws.amazon.com/blogs/big-data/develop-and-test-aws-glue-version-3-0-jobs-locally-using-a-docker-container/)
- [AWS - Creating OpenID Connect (OIDC) identity providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)

**_Terraform_**
- [Terraform - Hashicorp Terraform](https://www.terraform.io/)
- [Terraform - Conditional Expressions](https://developer.hashicorp.com/terraform/language/expressions/conditionals)
- [Stack Overflow - combine "count" and "for_each" on Terraform](https://stackoverflow.com/questions/68911814/combine-count-and-for-each-is-not-possible)

**_Apache Spark_**
- [SparkByExamples - Pyspark Date Functions](https://sparkbyexamples.com/pyspark/pyspark-sql-date-and-timestamp-functions/)
- [Spark - Configuration Properties](https://spark.apache.org/docs/latest/configuration.html)
- [Stack Overflow - repartition() vs coalesce()](https://stackoverflow.com/questions/31610971/spark-repartition-vs-coalesce)
  
**_GitHub_**
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- [Semantic Release](https://semver.org/)
- [GitHub - Angular Commit Message Format](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#-commit-message-format)
- [GitHub - commitlint](https://github.com/conventional-changelog/commitlint)
- [shields.io](https://shields.io/)
- [Codecoverage - docs](https://docs.codecov.com/docs)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Continuous Integration with GitHub Actions](https://endjin.com/blog/2022/09/continuous-integration-with-github-actions)
- [GitHub - About security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [GitHub - Securing deployments to AWS from GitHub Actions with OpenID Connect](https://www.eliasbrange.dev/posts/secure-aws-deploys-from-github-actions-with-oidc/#:~:text=To%20be%20able%20to%20authenticate,Provider%20type%2C%20select%20OpenID%20Connect.)
- [GitHub - Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Eduardo Mendes - Live de Python #170 - GitHub Actions](https://www.youtube.com/watch?v=L1f6N6NcgPw&t=3043s&ab_channel=EduardoMendes)

**_Docker_**
- [GitHub Docker Run Action](https://github.com/marketplace/actions/docker-run-action)
- [Using Docker Run inside of GitHub Actions](https://aschmelyun.com/blog/using-docker-run-inside-of-github-actions/)
- [Stack Overflow - Unable to find region when running docker locally](https://stackoverflow.com/questions/62546743/running-aws-glue-jobs-in-docker-container-outputs-com-amazonaws-sdkclientexcep)

**_Testes_**
- [Eduardo Mendes - Live de Python #167 - Pytest: Uma Introdução](https://www.youtube.com/watch?v=MjQCvJmc31A&)
- [Eduardo Mendes - Live de Python #168 - Pytest Fixtures](https://www.youtube.com/watch?v=sidi9Z_IkLU&t)
- [Databricks - Data + AI Summit 2022 - Learn to Efficiently Test ETL Pipelines](https://www.youtube.com/watch?v=uzVewG8M6r0&t=1127s)
- [Real Python - Getting Started with Testing in Python](https://realpython.com/python-testing/)
- [Inspired Python - Five Advanced Pytest Fixture Patterns](https://www.inspiredpython.com/article/five-advanced-pytest-fixture-patterns)
- [getmoto/moto - mock inputs](https://github.com/getmoto/moto/blob/master/tests/test_glue/fixtures/datacatalog.py)
- [Codecov - Do test files belong in code coverage calculations?](https://about.codecov.io/blog/should-i-include-test-files-in-code-coverage-calculations/)
- [Jenkins Issue: Endpoint does not contain a valid host name](https://issues.jenkins.io/browse/JENKINS-63177)

**_Outros_**
- [Differences between System of Record and Source of Truth](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/)
- [Olist Brazilian E-Commerce Data](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [Stack Overflow - @staticmethod](https://stackoverflow.com/questions/6843549/are-there-any-benefits-from-using-a-staticmethod)

