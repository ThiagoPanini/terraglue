<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/01-header-infra.png?raw=true" alt="terraglue-logo">
</div>

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Passo a passo resumido](#passo-a-passo-resumido)
- [Passo a passo detalhado](#passo-a-passo-detalhado)
  - [Configurando credenciais AWS](#configurando-credenciais-aws)
  - [Clonando o repositório](#clonando-o-repositório)
  - [Instalação dos módulos Terraform](#instalação-dos-módulos-terraform)
  - [Visualizando plano de implantação](#visualizando-plano-de-implantação)
  - [Implantando recursos no ambiente AWS](#implantando-recursos-no-ambiente-aws)
- [Conhecendo os módulos Terraform](#conhecendo-os-módulos-terraform)
- [Analisando os recursos de infra provisionados](#analisando-os-recursos-de-infra-provisionados)
  - [Buckets SoR, SoT, Spec e outros](#buckets-sor-sot-spec-e-outros)
  - [Dados na camada SoR](#dados-na-camada-sor)
  - [Catalogação no Data Catalog](#catalogação-no-data-catalog)
  - [Athena workgroup](#athena-workgroup)
  - [IAM policies e roles](#iam-policies-e-roles)
  - [Glue job](#glue-job)
  - [Dados na camada SoT](#dados-na-camada-sot)
- [Continue navegando nas documentações](#continue-navegando-nas-documentações)

___

## Passo a passo resumido

Visando proporcionar uma versão ágil de utilização, o consumo do **terraglue** pode ser resumido às seguintes etapas:

1. Configuração das credenciais AWS via `aws configure`
2. Clonagem do repositório para o ambiente local
3. Instalação dos módulos terraform via `terraform init` no diretório `./infra`
4. Planejamento e visualização das implantações via `terraform plan`
5. Implantação dos recursos na conta AWS alvo via `terraform apply`

Pronto! Com essas etapas será possível navegar e explorar toda a infraestrutura implantada automaticamente na AWS de acordo com os objetivos de aprendizado estabelecidos.

Tem dúvidas sobre como realizar alguma das etapas acima? Siga o passo a passo detalhado abaixo para explicações mais aprofundada sobre cada processo envolvido.

## Passo a passo detalhado

Nesta seção, as etapas de instalação e uso do **terraglue** serão exemplificadas em uma maior riqueza de detalhes, garantindo assim que todos os usuários, experientes ou não, consigam aproveitar de todo esse conjunto extremamente útil de funcionalidades.

### Configurando credenciais AWS

Como o **terraglue** possui a AWS como principal *provider*, é natural garantir que o ambiente está acessível e existem permissões básicas para a criação dos recursos declarados. Neste momento, o primeiro e o segundo pré requisitos se fazem presentes: além da conta alvo de implantação, é preciso possuir acesso a um usuário com acesso programático suficiente para a realização das chamadas necessárias.

Dessa forma, com as chaves `access_key_id` e `secret_access_key` em mãos, execute o comando abaixo no terminal e siga os passos solicitados para que a [configuração do AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) seja concluída com sucesso.

```bash
# Configurando credenciais do AWS CLI
aws configure
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/install-aws-configure.png?raw=true" alt="terraglue-aws-configure">
    </div>
</details>
<br>

**Obs:** as configurações demonstradas pela imagem acima funcionam apenas como um exemplo. O usuário deve informar suas próprias configurações de acordo com as especificidades de seu próprio ambiente. Caso o usuário já tenha realizado as etapas de configuração do AWS CLI, este passo pode tranquilamente ser ignorado.

É importante também citar que, em alguns ambientes, é preciso informar também o AWS Session Token. Dessa forma, ao invés de configurar as credenciais utilizando o comando `aws configure`, o usuário poderia, em posse das chaves e do token, alterar manualmente o arquivo de credenciais utilizando um editor de texto (ex: `nano ~/.aws/credentials`).

___

### Clonando o repositório

Uma vez garantida a configuração do AWS CLI para as devidas chamadas de implantação na AWS, o repositório com o código fonte do projeto **terraglue** pode devidamente ser clonado para o repositório local através do comando:

```bash
# Clonando repositório via SSH
git clone git@github.com:ThiagoPanini/terraglue.git
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/install-git-clone.png" alt="terraglue-git-clone">
  </div>
</details>
<br>

Com isso, todos os códigos alocados no projeto, em sua versão mais recente, poderão ser acessados da forma mais cômoda para o usuário, seja através da própria linha de comando ou até mesmo utilizando uma IDE.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/install-ls-repo.png" alt="terraglue-ls">
  </div>
</details>

___

### Instalação dos módulos Terraform

Como parte do processo de utilização do Terraform como ferramenta de IaC, é preciso inicializar os módulos presentes no projeto em um primeiro uso. Para isso, basta navegar até o diretório de infra do projeto e executar o comando próprio para a inicialização e obtenção dos insumos necessários do Terraform:

```bash
# Navegando até o diretório de infra
cd infra/

# Inicializando os módulos
terraform init
```

Com isso, para validar o sucesso da operação, uma mensagem próxima à exemplificada pela imagem à seguir é esperada:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/install-terraform-init.png" alt="terraglue-terraform-init">
  </div>
</details>

___

### Visualizando plano de implantação

Após a inicialização dos módulos do projeto e a obtenção dos insumos necessários para a plena utilização do Terraform, é possível executar o comando abaixo para visualizar todo o plano de implantação considerado dentro das funcionalidades do **terraglue**:

```bash
# Visualizando plano de implantação
terraform plan
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/install-terraform-plan.png" alt="terraglue-terraform-plan">
  </div>
</details>
<br>

> ⚠️ Como o **terraglue** comporta uma série de declaração de recursos, o *output* do comando `terraform plan` comporta uma série de detalhes. Se julgar necessário, analise com cuidado todas as implantações a serem realizadas em sua conta alvo. Ter controle sobre este passo garante uma total autonomia sobre tudo o que está sendo realizado, incluindo possíveis gastos na provedora cloud. Em caso de dúvidas, verifique a [documentação](https://github.com/ThiagoPanini/terraglue/blob/docs/visual-and-docs-refactorREADME.md) do projeto.

___

### Implantando recursos no ambiente AWS

Por fim, ao visualizar e concordar com o plano de implantação proporcionado pelo Terraform, o usuário pode finalmente executar o comando abaixo para realizar todo o processo de preparação de infraestrutura direto na conta AWS alvo:

```bash
# Implantando recursos terraglue
terraform apply
```

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/install-terraform-apply.png" alt="terraglue-terraform-apply">
  </div>
</details>
<br>

Após um determinado período, espera-se que uma mensagem de sucesso seja entregue ao usuário, garantindo assim que todas as inclusões e todos os recursos foram devidamente implantados no ambiente AWS. A partir deste ponto, o usuário terá em mãos todas as funcionalidades do **terraglue** disponíveis para uso!

___

## Conhecendo os módulos Terraform

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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-buckets-s3.png?raw=true" alt="infra-buckets-s3">
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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-data-customers.png?raw=true" alt="infra-buckets-s3">
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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-data-catalog-01.png?raw=true" alt="infra-data-catalog-01">
</div>
</details>

Entrando em maiores detalhes e utilizando a tabela `customers` como exemplo, a imagem abaixo exemplifica os detalhes técnicos catalogados e permite analisar atributos como *location*, *input format*, *output format* e propriedades *SerDe*:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-data-catalog-02.png?raw=true" alt="infra-data-catalog-02">
</div>
</details>

Por fim, reforçando de uma vez por todas o poder dessa funcionalidade de catalogação do projeto, a imagem abaixo traz as colunas obtidas automaticamente através de funções Terraform dos arquivos brutos e inseridos automaticamente no Data Catalog como atributos da tabela:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-data-catalog-03.png?raw=true" alt="infra-data-catalog-03">
</div>
</details>

___

### Athena workgroup

Provavelmente uma das primeiras ações realizadas por usuários após a inserção de dados em um bucket e sua posterior catalogação é a **execução de queries no Athena**. Visando alcançar este público, o `terraglue` considera a criação automática de um [Athena workgroup](https://docs.aws.amazon.com/athena/latest/ug/user-created-workgroups.html) já configurado para uso.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-athena-workgroup.png?raw=true" alt="infra-athena-workgroup">
</div>
</details>

Com isso, os usuários já podem iniciar o consumo de dados no Athena sem a necessidade de realizar configurações prévias ou adicionais na conta alvo.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-athena-query.png?raw=true" alt="infra-athena-query">
</div>
</details>

___

### IAM policies e roles

Neste momento, estamos aproximando do objetivo do projeto que diz respeito a implementação de um job do Glue totalmente configurado. Uma etapa crucial que antecede a criação de um job no Glue está relacionada à definição e criação dos elementos capazes de fornecer os acessos necessários para o job. Aqui, estamos falando de *policies* e *roles* do IAM.

Dessa forma, o `terraglue` considera, em seus detalhes internos de implantação de recursos, a criação de **2 policies** e **1 role** do IAM a ser vinculada ao job do Glue já com todos os acessos necessários de execução e catalogação de dados.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-iam-role.png?raw=true" alt="infra-iam-role">
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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-glue-job-01.png?raw=true" alt="infra-glue-job-01">
</div>
</details>

Considerando a lógica definida na ferramenta de IaC, o job do Glue possui todo um arcabouço de parâmetros e configuração estabelecidos de forma automática para que o usuário tenha em mãos um exemplo mais fidedigno possível de um processo de ETL na AWS sem se preocupar com definições adicionais.

Ao acessar o job através do console e navegar até o menu *Job details* (ou detalhes do job), o usuário poderá analisar todas as configurações estabelecidas, como por exemplo, a role IAM, os caminhos no s3 para armazenamento do *script* Python, *assets* e outros objetos. Ao final deste menu, o usuário também poderá verificar todo o *set* de parâmetros do job disponibilizados como padrão para a realização e execução do processo de transformação de dados.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-glue-job-02.png?raw=true" alt="infra-glue-job-02">
</div>
</details>

Além disso, no menu *Schedules*, será possível visualizar um agendamento criado automaticamente via Terraform para execução do *job* Glue com uma expressão cron fornecida como exemplo (`cron(0 21 ? * 6 *)`) simulando o gatilho de execução todas às sextas-feiras às 21h00m. Para maiores detalhes, o usuário poderá consultar o [recurso `aws_glue_trigger`](https://github.com/ThiagoPanini/terraglue/blob/main/infra/modules/glue/main.tf#L49) no módulo glue presente no diretório de infra.

___

### Dados na camada SoT

E assim, ao acessar o job do Glue criado e realizar sua execução, o usuário poderá analisar todos os detalhes de construção envolvidos, incluindo os parâmetros associados, as configurações internas do job e também os logs de execução no CloudWatch.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-sot-01.png?raw=true" alt="infra-glue-sot-01">
</div>
</details>

Como resultado, o usuário terá disponível uma nova base de dados materializada como uma tabela já catalogada com seus dados armazenados no S3 (bucket SoT) no caminho `s3://terraglue-sot-data-<accountid>-<region>/ra8/tbsot_ecommerce_br/anomesdia=<anomesdia>/`:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/infra/infra-sot-02.png?raw=true" alt="infra-glue-sot-02">
</div>
</details>

___

## Continue navegando nas documentações

- [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main)
- 👉 [2. Implantando e conhecendo a infraestrutura](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md) *Você está aqui!*
- [3. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/APP.md) 
- [4. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/EXAMPLES.md)
- [5. Testes unitários em jobs do Glue na AWS](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/TESTS.md)
