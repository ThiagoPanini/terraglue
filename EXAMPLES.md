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
- [Cenário 2: uma proposta de padronização de jobs do Glue](#cenário-2-uma-proposta-de-padronização-de-jobs-do-glue)
  - [O script main-terraglue.py](#o-script-main-terragluepy)
  - [Classes GlueJobManager e GlueTransformationManager](#classes-gluejobmanager-e-gluetransformationmanager)
  - [Ações do usuário para utilizar e adaptar o script](#ações-do-usuário-para-utilizar-e-adaptar-o-script)
- [Cenário 3: implementando seu próprio conjunto de dados](#cenário-3-implementando-seu-próprio-conjunto-de-dados)
  - [Sobre os dados de exemplo (Brazilian E-Commerce)](#sobre-os-dados-de-exemplo-brazilian-e-commerce)
  - [Utilizando dados próprios](#utilizando-dados-próprios)
  - [Visualizando efeitos na conta AWS](#visualizando-efeitos-na-conta-aws)
- [Cenário 4: implementando seu próprio job do Glue](#cenário-4-implementando-seu-próprio-job-do-glue)
  - [Modificando e configurando o script](#modificando-e-configurando-o-script)
  - [Codificando novas transformações](#codificando-novas-transformações)
  - [Executando jobs próprios](#executando-jobs-próprios)
___

## Antes de começar

Antes de navegarmos por exemplos práticos de consumo, é importante garantir que todas as etapas de preparação e instalação foram cumpridas. Para maiores detalhes, o arquivo [GETTINGSTARTED.md](https://github.com/ThiagoPanini/terraglue/blob/develop/GETTINGSTARTED.md) contempla todo o processo necessário de iniciação.

Adicionalmente, é válido citar que esta documentação será separada em diferentes **cenários**, cada um trazendo à tona uma possível seara de aplicação do **terraglue** de acordo com um propósito específico. É importante destacar que os cenários contemplam desafios próprios e particulares, sendo direcionados para públicos específicos que podem se beneficiar das funcionalidades deste projeto. Encontre aquele que mais faça sentido dentro de sua jornada de aprendizado e mergulhe fundo!

| 🎬 **Cenário** | **🎯 Público alvo** |
| :-- | :-- |
| [#1 Um primeiro passo na análise dos recursos](#cenário-1-um-primeiro-passo-na-análise-dos-recursos) | Todos os usuários |
| [#2 Compreendendo detalhes de um job Spark no Glue](#cenário-2-compreendendo-detalhes-de-um-job-spark-no-glue) | Usuários com conhecimentos básicos |
| [#3 Implementando seu próprio conjunto de dados](#cenário-3-implementando-seu-próprio-conjunto-de-dados) | Usuários com conhecimentos básicos |
| [#4 Implementando seu próprio job do Glue](#cenário-4-implementando-seu-próprio-job-do-glue) | Usuários com conhecimentos intermediários |

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

Considerando a lógica definida na ferramenta de IaC, o job do Glue possui todo um arcabolso de parâmetros e configuração estabelecidos de forma automática para que o usuário tenha em mãos um exemplo mais fidedigno possível de um processo de ETL na AWS sem se preocupar com definições adicionais.

Ao acessar o job através do console e navegar até o menu *Job details* (ou detalhes do job), o usuário poderá analisar todas as configurações estabelecidas, como por exemplo, a role IAM, os caminhos no s3 para armazenamento do *script* Python, *assets* e outros objetos. Ao final deste menu, o usuário também poderá verificar todo o *set* de parâmetros do job disponibilizados como padrão para a realização e execução do processo de transformação de dados.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-glue-job-02.png?raw=true" alt="terraglue-practical-glue-job-02">
</div>
</details>

___

### Dados na camada SoT

E assim, ao acessar o job do Glue criado e realizar sua execução, o usuário poderá analisar todos os detalhes de construção envolvidos, incluindo os parâmetros associados, as configurações internas do job e também os logs de execução no CloudWatch.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-sot-01.png?raw=true" alt="terraglue-practical-glue-sot-01">
</div>
</details>

Como resultado, o usuário terá disponível uma nova base de dados materializada como uma tabela já catalogada com seus dados armazenados no S3 (bucket SoT) no caminho `s3://terraglue-sot-data-503398944907-us-east-1/ra8/tbsot_ecommerce_br/anomesdia=20221111/`:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-practical-sot-02.png?raw=true" alt="terraglue-practical-glue-sot-02">
</div>
</details>

___

## Cenário 2: uma proposta de padronização de jobs do Glue

Agora que o usuário já passou pelo primeiro cenário de consumo do **terraglue** através do conhecimento geral sobre seus recursos e dinâmica de implantação, é chegado o momento de apresentar, em detalhes, a ideia de modelo padronizado de uma aplicação Spark a ser utilizada em toda e qualquer criação de *job* do Glue.

| 🎯 **Público alvo** | Usuários com conhecimentos básicos |
| :-- | :-- |

### O script main-terraglue.py

A ideia é ousada e ambiciosa: proporcionar, ao usuário final, um *template* de código muito além de um simples [*boilerplate*](https://pt.wikipedia.org/wiki/Boilerplate_code) e que permita entregar aplicações Spark implantadas como *jobs* do Glue de uma maneira muito mais fácil e ágil através de poucas modificações. Com esse objetivo, faz-se presente o script [main-terraglue.py](https://github.com/ThiagoPanini/terraglue/blob/develop/app/main-terraglue.py) ao qual será alvo da totalidade de exemplificações desta seção. Fique ligado e veja como otimizar seu processo de criação de ETLs na nuvem!

De início, é válido citar que toda a codificação presente no script `main-terraglue.py` fornecido como exemplo do projeto pode auxiliar grandemente usuários em dois perfis diferentes:

* 🤔 Usuários com pouco ou nenhum conhecimento em Spark, Python e Glue que possuem a intenção de construir processos através de uma adaptação simplória de um código já organizado e bem estruturado.
* 🤓 Usuários avançados que já possuem *jobs* Glue implantados, mas que percebem que a quantidade de linhas de código ou mesmo a organização adotada não é escalável, prejudicando assim a manutenção de suas aplicações.

No mais, a proposta de padronização de um *job* Glue no script `main-terraglue.py` tem como base a estruturação de duas classes Python codificadas exclusivamente para facilitar o trabalho do usuário final em meio as etapas de construção, configuração e execução de uma aplicação Spark.

### Classes GlueJobManager e GlueTransformationManager

Como introduzido previamente, o script Python presente no projeto é composto por duas classes extremamente úteis:

| 🐍 **Classe Python** | 📌 **Atuação e Importância** |
| :-- | :-- |
| `GlueJobManager` | Utilizada para gerenciar toda a construção de um *job* Glue através da inicialização dos argumentos do processo e dos elementos que compõem o contexto (`GlueContext` e `SparkContext`) e sessão (`SparkSession`) de uma aplicação. |
| `GlueTransformationManager` | Utilizada para consolidar métodos prontos para leitura de `DynamicFrames` e `DataFrames` e transformação destes objetos no contexto de utilização do *job*. |

Para que se tenha uma noção do grande poder de utilização de ambas as classes em um cenário de construção de um *job* do Glue sustentável e com as melhores práticas de código limpo, o bloco abaixo representa a parte principal do script onde o usuário solicita a execução da aplicação com poucas instruções:

```python
if __name__ == "__main__":

    # Inicializando objeto para gerenciar o job e as transformações
    glue_manager = GlueTransformationManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    # Executando todas as lógicas mapeadas do job
    glue_manager.run()
```

De maneira intuitiva, o método `run()` atua como um grande consolidador de outros métodos de transformação presentes na classe `GlueTransformationManager`. Mesmo assim, são poucas as atuações necessárias por parte do usuário para adaptar toda a estrutura de código proporcionada para seu respectivo *job*.

### Ações do usuário para utilizar e adaptar o script

Considerando os detalhes demonstrados acima, usuários iniciantes ou experientes que desejam utilizar o template do **terraglue** para construir seus *jobs* Glue deverão, essencialmente, seguir quatro passos importantes no processo de consumo:

1. Adaptar o vetor de argumentos do *job* através da variável `ARGV_LIST`
2. Adaptar o dicionário com os dados a serem utilizados no *job* através da variável `DATA_DICT`
3. Criar os métodos de transformação dos dados na classe `GlueTransformationManager`
4. Adaptar o método `run()` com os dados a serem lidos e os novos métodos gerados

Todas as demais operações já estão inclusas nos métodos internos das classes disponibilizadas ao usuário e não necessitam de alterações. Em outras palavras, o usuário pode focar nas codificações relacionadas às suas próprias transformações de dados ao invés de se preocupar os elementos de configuração do *job*.

> 📌 Neste momento, é importante citar que ambas as classes `GlueJobManager` e `GlueTransformationManager` possuem uma vasta documentação no script Python [main-terraglue.py](https://github.com/ThiagoPanini/terraglue/blob/develop/app/main-terraglue.py) disponibilizado. Consulte o arquivo fonte para informações mais detalhadas a respeito deste vasto leque de possibilidades envolvendo a padronização da construção de um job do Glue.
___

## Cenário 3: implementando seu próprio conjunto de dados

Após uma importante jornada envolvendo um completo entendimento sobre os recursos e as funcionalidades do projeto no [cenário 1](#cenário-1-um-primeiro-passo-na-análise-dos-recursos), além do grande leque de possibilidades técnicas de codificação de aplicações Spark em *jobs* do Glue no [cenário 2](#cenário-2-uma-proposta-de-padronização-de-jobs-do-glue), é chegado o momento de entender como o **terraglue**, como solução dinâmica, pode ser adaptado de acordo com os propósitos de seus usuários.

Com isso em mente, o terceiro cenário de ilustração e exemplificação tem como princípio a substituição dos dados de exemplo, fornecidos por padrão no código fonte do repositório, por outros conjuntos próprios e específicos do usuário, permitindo assim com que o mesmo utilize todas as demais funcionalidades do **terraglue** em cenários de maior valor agregado.

| 🎯 **Público alvo** | Usuários com conhecimentos básicos |
| :-- | :-- |

### Sobre os dados de exemplo (Brazilian E-Commerce)

Antes de iniciar as discussões desta seção, é imprescindível abordar, de forma resumida, alguns detalhes sobre o conjunto de dados fornecido por padrão no repositório: trata-se de bases que contemplam o famoso dataset [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Originalmente disponível na plataforma [Kaggle](https://www.kaggle.com/), o referido conjunto contempla dados de vendas online no *e-commerce* brasileiro separados em diferentes arquivos de texto, cada um em seu respectivo domínio. Juntos, os arquivos podem ser utilizados e trabalhados para retirar os mais variados *insights* relacionados ao comércio online.

<details>
  <summary>🎲 Clique para visualizar o schema original dos dados</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/examples-cenario03-schema-br-ecommerce.png?raw=true" alt="br-ecommerce-schema">
</div>
</details>

Visando proporcionar uma maior simplicidade no exemplo de geração de SoT, apenas alguns arquivos do conjunto de dados Brazilian E-Commerce foram selecionados como SoRs do projeto, sendo eles:

| 🗂️ **Arquivo** | 📝 **Descrição** |
| :-- | :-- |
| `orders.csv` | Contempla dados de pedidos realizados online |
| `customers.csv` | Contempla dados cadastrais dos clientes que realizaram os pedidos online |
| `payments.csv` | Contempla dados dos pagamentos utilizados para quitação dos pedidos realizados |
| `reviews.csv` | Contempla dados das revisões, nota e comentários deixados por clientes para os pedidos realizados |

Assim, os conjuntos citados então são disponibilizados localmente em uma estrutura hierárquica de pastas que simula uma organização de dados em um ambiente Data Lake no formato `db/tbl/file`, sendo esta uma dinâmica **mandatória** para o sucesso de implantação de conjuntos próprios de dados.

### Utilizando dados próprios

Conhecidos os arquivos que fazem parte do repositório em seu modo natural, o usuário agora poderá adaptar todo o processo de ingestão e catalogação proporcionado no **terraglue** para seus próprios conjuntos.

Em um primeiro momento, é extremamente ressaltar algumas premissas e limitações do processo de catalogação de dados no Data Catalog da conta AWS:

1. Somente arquivos `csv` poderão ser utilizados
2. Os arquivos `csv` devem possuir o *header* na primeira linha
3. A estrutura hierárquica deve seguir o modelo `db/tbl/file` a partir do diretório `data/` do repositório

> 📌 Avaliar as premissas acima é de suma importância pois, em seus detalhes técnicos de construção, o **terraglue** considera a aplicação de funções do Terraform para iterar sobre os diretórios presentes em `data/`, realizar a leitura da primeira linha dos arquivos CSV para extração dos atributos e catalogação no Data Catalog. Sem o cumprimento das premissas, as funções do Terraform irão retornar erro e o fluxo não será implantado conforme esperado pelo usuário.

Endereçado este ponto, os exemplos ilustrados a seguir simulam a obtenção de novos conjuntos de dados a serem utilizados no processo de ingestão e catalogação em substituição aos dados originais do dataset Brazilian E-Commerce fornecidos como padrão.

Como um primeiro passo, o usuário pode navegar até o repositório do **terraglue** clonado localmente e executar o comando abaixo para remover todo o contéudo presente em `data/` no repositório do projeto. Também é possível excluir os arquivos e diretórios manualmente, se preferir.

```bash
# Removendo todos os arquivos de /data
rm -r data/*
```

Com o diretório `/data` agora vazio, basta obter os novos dados a serem utilizados e organizá-los na estrutura adequada. Como exemplo, utilizarei dados do [naufrágio do Titanic](https://www.kaggle.com/competitions/titanic/data) previamente baixados e armazenados no diretório `~/Downloads` com o nome `titanic.csv`. Antes de realizar a movimentação do arquivo, é importante criar toda a estrutura de pastas locais que simulam a organização de um Data Lake a ser replicado no S3 durante o processo de implantação do **terraglue**. O nome do *database* será escolhido aleatoriamente.

```bash
# Criando estrutura de pastas locais
mkdir -p data/tt3/tbl_titanic_data
```

Onde `tt3` é o nome fictício para o *database* e `tbl_titanic_data` o nome escolhido para a tabela. Com isso, é possível movimentar o arquivo desejado para a estrutura criada.

```bash
# Movendo arquivo
mv ~/Downloads/titanic.csv data/tt3/tbl_titanic_data/
```

Validado que o novo arquivo já consta organizado localmente na estrutura necessária, bastas executar os procedimentos de implantação do **terraglue** através do comando `terraform apply` para implementar todos os processos atrelados.

### Visualizando efeitos na conta AWS

Uma vez obtido e organizado o(s) novo(s) conjunto(s) de dado(s) a serem inseridos junto com os processos de implantação do **terraglue**, o usuário poderá acessar o S3 para avaliar o sucesso de ingestão dos novos dados dentro do bucket `terraglue-sor`. Na imagem abaixo, é possível verificar que o conjunto de dados `titanic.csv` foi inserido com sucesso com o prefixo `tt3/tbl_titanic_data`, assim como o esperado.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/examples-cenario03-titanic-data-on-s3.PNG?raw=true" alt="titanic-data-on-s3">
</div>
</details>

Além disso, é possível também acessar o serviço Glue e, dentro do menu Data Catalog, validar se o arquivo inserido no S3 também passou pelo processo de catalogação. Na imagem abaixo, é possível verificar que uma entrada no catálogo foi automaticamente criada para os dados do Titanic recém disponibilizados:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/examples-cenario03-titanic-data-on-data-catalog.PNG?raw=true" alt="titanic-data-on-data-catalog">
</div>
</details>

Ao selecionar a tabela no catálogo, será ainda possível perceber que todo o processo de obtenção de atributos pôde ser realizado com sucesso. Essa afirmação tem como base o próprio *schema* da tabela presente no catálogo:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/examples-cenario03-titanic-schema-on-catalog.PNG?raw=true" alt="titanic-schema-on-data-catalog">
</div>
</details>

Por fim, a validação final realizada envolve o acesso ao serviço Athena para execução de uma simples *query* para extração dos dados recém catalogados. A imagem abaixo exemplifica a retirada de 10 registros da base através do comando `SELECT * FROM tt3.tbl_titanic_data LIMIT 10;`:

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/examples-cenario03-titanic-data-on-athena.PNG?raw=true" alt="titanic-data-on-athena">
</div>
</details>

Com isso, é possível validar que todo o processo de adaptação do **terraglue** para uso de novas bases de dados em substituição aos dados de e-commerce fornecidos por padrão pode ser tranquilamente realizado.

A partir desta funcionalidade, os usuários poderão:

- Adaptar o uso do **terraglue** para propósitos específicos
- Ingerir e catalogar amostras de dados em um ambiente corporativo
- Acelerar o processo de desenvolvimento e testes de seus *jobs*
- Realizar consultas *ad-hoc* em dados catalogados automaticamente
___

## Cenário 4: implementando seu próprio job do Glue

E assim, garantindo que o usuário alcance este cenário com um conhecimento completo sobre o que é o `terraglue` e algumas de suas principais funcionalidades, este cenário envolve a consolidação do processo de adaptação da solução para os propósitos específicos de cada usuário. Se, no [cenário 3](#cenário-3-implementando-seu-próprio-conjunto-de-dados) o usuário pôde aprender como inserir seus próprios conjuntos de dados para ingestão e catalogação automática no ambiente AWS, o cenário exemplificado neste seção traz detalhes sobre como adaptar o script `main-terraglue.py` para incluir transformações e regras próprias de negócio em uma simulação de publicação inédita de um novo *job* Glue na AWS.

### Modificando e configurando o script

O script `main-terraglue.py` comporta uma série de funcionalidades especialmente codificadas para facilitar o esforço operacional do usuário em iniciar e configurar os elementos básicos necessários para uso e interação com o Glue. No script, será possível encontrar as classes Python `GlueJobManager` e `GlueTransformationManager`. Maiores detalhes sobre essa proposta de padronização de um *job* Glue podem ser encontradas nesta mesma documentação no [Cenário 2 - Uma proposta de padronização de jobs Glue](#cenário-2-uma-proposta-de-padronização-de-jobs-do-glue).

Para o usuário que inseriu novos dados e deseja codificar suas próprias transformações para testar, validar ou simplesmente entender como um *job* Glue funciona, a lista de tópicos abaixo pode servir como um simples resumo das operações necessárias:

1. Analisar e modificar, se necessário, a variável `ARGV_LIST` presente no script principal para mapear e coletar possíveis novos parâmetros do *job* inseridos pelo usuário

> O processo de inclusão de novos parâmetros pode ser feito através da variável Terraform `glue_job_user_arguments` presente no arquivo `./infra/variables.tf`.

2. Modificar, em caso de inclusão de novos dados, a variável `DATA_DICT` com todas as informações necessárias para leitura dos dados a serem trabalhados. 

> Para este processo, todos os argumentos do método `glueContext.create_dynamic_frame.from_catalog()` são aceitos.

3. Codificar novos métodos de transformação na classe `GlueTransformationManager` de acordo com as regras de negócio a serem aplicadas na geração das novas tabelas.

> Para fins de organização, os métodos de transformação fornecidos como padrão iniciam com o prefixo "transform_". São esses os métodos que devem ser substituídos para o novo processo de ETL codificado.

4. Modificar o método `run()` da classe `GlueTransformationManager` de acordo com a nova sequênciad e passos necessários até o alcance do objetivo final do *job*.

### Codificando novas transformações


### Executando jobs próprios
