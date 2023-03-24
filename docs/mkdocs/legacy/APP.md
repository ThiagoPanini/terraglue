<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/app/01-header-app.png?raw=true" alt="terraglue-logo">
</div>


## Table of Contents
- [Table of Contents](#table-of-contents)
- [Desafios de desenvolvimento de um job Glue](#desafios-de-desenvolvimento-de-um-job-glue)
- [Uma proposta de padronização de jobs do Glue](#uma-proposta-de-padronização-de-jobs-do-glue)
  - [Módulos e scripts entregues ao usuário](#módulos-e-scripts-entregues-ao-usuário)
  - [Público alvo](#público-alvo)
- [O módulo terraglue.py](#o-módulo-terragluepy)
  - [A classe GlueJobManager](#a-classe-gluejobmanager)
  - [A classe GlueETLManager](#a-classe-glueetlmanager)
- [O script main.py](#o-script-mainpy)
  - [A classe GlueTransformationManager](#a-classe-gluetransformationmanager)
- [Adaptando a aplicação para finalidades próprias](#adaptando-a-aplicação-para-finalidades-próprias)
- [Continue navegando nas documentações](#continue-navegando-nas-documentações)

___

## Desafios de desenvolvimento de um job Glue

A dinâmica de processamento de grandes volumes de dados é, sem dúvidas, uma vertente altamente desafiadora no mundo analítico. Em meio às inúmeras ferramentas e *frameworks* que se fazem presentes hoje em dia no mercado, o [Spark](https://spark.apache.org/) possui um destaque especial por, entre outros fatores, entregar uma gigantesca gama de possibilidades em termos de desenvolvimento de soluções escaláveis. Em uma seara gerenciada, o [AWS Glue](https://aws.amazon.com/glue/) também pode ser considerado um serviço atualmente presente no gosto da grande massa de Engenheiros, Analistas e até Cientistas de Dados que desejam uma forma fácil, rápida e eficiente para implementar jobs de ETL capazes de comportar grandes volumes de dados.

Por maiores que sejam as facilidades entregues por estes e outros *frameworks* e serviços analíticos, ainda existe um fator de aprendizado que exige, de seus usuários, entender alguns detalhes técnicos importantes antes de mergulhar à fundo e extrair todo o potencial entregue por tais ferramentas.

Em alguns casos, a necessidade rápida em codificar transformações e obter resultados atravessa o entendimento de conceitos teóricos fundamentais para uma compreensão holística do processo. Afinal, nem todos sabem a fundo o significado de termos como, por exemplo, `SparkSession`, `SparkContext`, `GlueContext`, `DynamicFrame`. Ainda assim, alguns métodos e objetos espeíficos do Glue precisam ser endereçados antes e durante o desenvolvimento de jobs, trazendo uma complexidade a mais neste processo, principalmente para usuários iniciantes.

💡 Com tudo isso em mente, a principal pergunta que se faz é: *"como entregar ao usuário uma forma rápida, fácil e de baixa complexidade para que o mesmo possa desenvolver e codificar um job Glue na AWS sem se preocupar com definições 'burocráticas' e focando apenas na aplicação das regras de transformações de dados?*".

___

## Uma proposta de padronização de jobs do Glue

Entendidos alguns dos principais desafios envolvendo a criação de scripts e códigos dentro da dinâmica de usabilidade do Glue, é chegado o momento de apresentar, com extremo entusiasmo, o modelo idealizado de desenvolvimento de uma aplicação Spark proporcionado pelo **terraglue**. Aqui, o usuário conhecerá todos os detalhes técnicos de construção da proposta e todos os benefícios de se ter funcionalidades pré programadas de acordo com as melhores práticas de desenvolvimento de código envolvendo `pyspark` e Glue.

### Módulos e scripts entregues ao usuário

A ideia é ousada e ambiciosa: proporcionar, ao usuário final, um *template* de código muito além de um simples [*boilerplate*](https://pt.wikipedia.org/wiki/Boilerplate_code) e que permita entregar aplicações Spark implantadas como *jobs* do Glue de uma maneira muito mais fácil e ágil através de poucas modificações. Um tanto quanto desafiador, não?

Para isso, o repositório fonte foi configurado para que, dentro do diretório `./app/src`, dois *scripts* Python altamente importantes se façam presentes:

- 🐍 [main.py](https://github.com/ThiagoPanini/terraglue/blob/main/app/src/main.py) - Script principal contendo toda a lógica de transformação dos dados a serem submetidas como uma aplicação Spark em um job Glue na AWS. É aqui que o usuário focará seus esforços de desenvolvimento, adaptação e validação dos resultados.
- 🐍 [terraglue.py](https://github.com/ThiagoPanini/terraglue/blob/main/app/src/terraglue.py) - Módulo auxiliar criado para comportar tudo aquilo que pode ficar *invisível* aos olhos do usuário como uma forma de facilitar toda a jornada de obtenção de insumos "burocráticos" de um job Glue como, por exemplo, elementos de sessão, contexto, logs, argumentos ou até mesmo métodos estáticos utilizados em transformações comumente utilizadas em grande parte dos jobs.

Os *scripts* são, essencialmente, compostos por classes Python capazes de entregar todo o conjunto de funcionalidades necessárias para que os usuários tenham em mãos uma forma padronizada e organizada de desenvolver seus próprios métodos de transformação de dados. Dessa forma, a tabela abaixo traz alguns detalhes introdutórios futuramente explorados em detalhes de cada uma das classes presentes em ambos os módulos citados:

| 🐍 **Classe Python** | 🧩 **Módulo** | 📌 **Atuação e Importância** |
| :-- | :-- | :-- |
| `GlueJobManager` | `terraglue.py` | Utilizada para gerenciar toda a construção de um *job* Glue através da inicialização dos argumentos do processo e dos elementos que compõem contexto (`GlueContext` e `SparkContext`) e sessão (`SparkSession`) de uma aplicação. |
| `GlueETLManager` | `terraglue.py` | Utilizada para consolidar métodos prontos para leitura de `DynamicFrames` e `DataFrames` e transformação destes objetos no contexto de utilização do *job*. |
| `GlueTransformationManager` | `main.py` | Utilizada para receber os métodos de transformação codificados pelo usuário para aplicação das regras de negócio no job. Adicionalmente, um método `run()` pode ser utilizado para encadeamento dos processos de transformação de acordo com as necessidades específicas do usuário. |

### Público alvo

Não se preocupe, caro leitor, se algo até aqui estiver soando muito complexo. Considerando os pilares designados do **terraglue**, é possível afirmar que o conjunto de solução fornecido possui impacto relevante em dois perfis de usuários:

* 🤔 Usuários com pouco ou nenhum conhecimento em Spark, Python e Glue que possuem a intenção de construir processos através de uma adaptação simplória de um código já organizado e bem estruturado.
* 🤓 Usuários avançados que já possuem *jobs* Glue implantados, mas que percebem que a quantidade de linhas de código ou mesmo a organização adotada não é escalável, prejudicando assim a manutenção de suas aplicações.

Ao longo desta seção da documentação, todas as funcionalidades dos códigos fornecidos serão exemplificadas em uma riqueza de detalhes para que o usuário tenha total capacidade de garantir um bom uso da solução.

___

## O módulo terraglue.py

De início, iniciamos o processo de entendimento da aplicação através do script homônimo `terraglue.py` disponibilizado como um módulo adicional ao script principal. Sua proposta é consolidar uma forma fácil, rápida e transparente para coletar todos os insumos necessários para execução de um job Glue na AWS. Seu contéudo é composto pelas classes `GlueJobManager` e `GlueETLManager`, as quais serão exploradas logo a seguir.

### A classe GlueJobManager

Com introduzido, a classe `GlueJobManager` possui um papel fundamental na consolidação de métodos e atributos capazes de "fazer a coisa acontecer". É a partir dela que a execução de um job Glue pode ser possível dentro da proposta de solução do projeto. Não à toa, essa classe é herdada por outras classes ao longo do processo de codificação de métodos de leitura e transformação de dados na aplicação.

Com essa proposta em mente, os métodos existentes até o momento na classe `GlueJobManager` incluem:

| 🚀 **Método** | 📝 **Descrição** |
| :-- | :-- |
| `job_initial_log_message()` | Proporciona uma mensagem inicial de log escrita no CloudWatch contendo detalhes sobre todas as origens utilizadas no Job e seus respectivos filtros de *push down predicate* |
| `print_args()` | Informa ao usuário, através de uma *log stream* no CloudWatch todos os argumentos/parâmetros utilizados no job |
| `get_context_and_session()` | Retorna os elementos `SparkContext`, `GlueContext` e `SparkSession` como atributos da classe para serem utilizados posteriormente quando solicitados |
| `init_job()` | Consolida os métodos anteriores e fornece uma porta de entrada única para inicialização do job, escrita de logs iniciais no CloudWatch e obtenção dos elementos necessários de execução, incluindo um objeto `Job` criado a partir do `GlueContext` obtido |

### A classe GlueETLManager

Complementando a entrega das funcionalidades do módulo homônimo auxiliar, a classe `GlueETLManager` possui uma atuação crucial para a entrega de funcionalidades utilizadas especiamente nos processos de leitura e transformações de dados que podem ser replicadas de maneira agnóstica para qualquer tipo de job. Em outras palavras, é aqui onde o usuário encontrará, por exemplo, método para leitura de DynamicFrames e DataFrames, adição e remoção de partição em tabelas ou até mesmo escrita de dados e catalogação no Data Catalog.

Além disso, a classe `GlueETLManager` herda, em seu método construtor, todos os atributos e métodos da classe `GlueJobManager`, permitindo assim que as funcionalidades próprias da primeira utilizem os insumos do job previamente instanciados na segunda.

Dessa forma, entre os métodos atualmente disponíveis nessa classe, é possível citar:

| 🚀 **Método** | 📝 **Descrição** |
| :-- | :-- |
| `generate_dynamic_frames_dict()` | Proporciona uma forma fácil e eficiente de realizar a leitura de múltiplas fontes de dados referenciadas em um dicionário Python de modo a entregar objetos do tipo `DynamicFrame` para cada uma delas |
| `generate_dataframes_frames_dict()` | Possui a mesma dinâmica do método anterior, porém o resultado final é entregue ao usuário como um dicionário contendo múltiplos objetos do tipo `DataFrame` |
| `extract_date_attributes()` | Permite extrair uma série de atributos temporais de campos de data (ou strings que representam datas), como ano, quadrimestre, mês, dia, dia da semana, semana do ano ou tudo o que pode ser extraído através de funções Spark |
| `extract_aggregate_statistics()` | Permite extrair uma série de estatísticas agregadas de um DataFrame com base em uma coluna numérica e uma lista de atributos a serem agrupados. Com este método, o usuário pode extrair a média, mediana, contagem, contagem distinta, variância, desvio padrão e toda e qualquer função estatística presente no Spark com uma única chamada |
| `drop_partition()` | Recebe uma referência de nome e valor de partição para executar o processo de `purge` de dados no s3, permitindo assim que fluxos de trabalho evitem um *append* indesejado em caso de execuções simultâneas ou repetidas |
| `add_partition()` | Permite, através de um nome de partição e um valor fornecidos pelo usuário, realizar a inclusão de uma nova coluna em um objeto DataFrame via execução do método `.withColumn()` do Spark |
| `repartition_dataframe()` | Consolida regras para a correta aplicação do processo de reparticionamento de um DataFrame Spark visando a otimização do armazenamento dos dados físicos no S3 |
| `write_data_to_catalog()` | Aplica os processos de `getSink` e `setCatalogInfo` para escrever um DynamicFrame no s3 e realizar a subsequente catalogação da tabela no Data Catalog de acordo com parâmetros fornecidos pelo usuário |

___

## O script main.py

Diante da riqueza de funcionalidades presentes no módulo `terraglue.py`, o script `main.py` atua de modo a representar, de fato, a aplicação principal Spark a ser referenciada no Glue e observável, opcionalmente, através do AWS Management Console. É aqui onde todas as funcionalidade se unem para que as regras de transformação possam ser desenvolvidas e consolidadas de modo a alcançar os resultados almejados.

Garantindo que todas as etapas "burocráticas" de preparação e obtenção de insumos do job já estão encapsuladas no módulo `terraglue.py`, no script `main.py` o usuário deve apenas focar seus esforços no desenvolvimento de métodos de transformação capazes de aplicar as regras pretendidas para as origens lidas. Seu conteúdo é composto pela classe `GlueTransformationManager`, cujos detalhes serão exemplificados na sequência.

### A classe GlueTransformationManager

Como mencionado anteriormente, é aqui onde o usuário desenvolverá seus métodos de transformação capazes de alcanar a visão necessária das origens em meio às regras de negócio estabelecidas. A classe `GlueTransformationManager` herda todos os atributos da classe `GlueETLManager` (que, por sua vez, herda todos os atributos e métodos da classe `GlueJobManager`), permitindo assim com que todas as funcionalidade do módulo `terraglue.py` estejam prontamente acessíveis, caso necessário.

Em outras palavras, além de proporcionar uma forma organizada de consolidação dos métodos de transformação em Spark, o usuário também poderá executar todos os outros métodos agnósticos presentes em ambas as classes citadas.

Pela própria essência mencionada, os métodos da classe `GlueTransformationManager` dependem das próprias regras associadas pelo usuário no ato de construção do job. De toda forma, a tabela abaixo aborda uma ideia de como essa adaptação relativa pode ser feita:

| 🚀 **Método** | 📝 **Descrição** |
| :-- | :-- |
| `transform_<source>()` | Métodos de transformação podem possuir um prefixo específico e podem ser codificados para cada uma das origens onde se tenham necessidades de transformações de dados. Diversos métodos de transformação podem existir dentro da classe. |
| `transform_<sot\|spec>()` | Este pode ser um método criado após a aplicação de todas as transformações de origens, permitindo assim um método único para unificação dos resultados e geração das tabelas SoT ou Spec, conforme as necessidades do usuário. |
| `run()` | Este provavelmente é o método mais importante desta classe. Nele, o usuário deverá sequenciar todas as atividades relacionadas à execução do job. Para isso, ele deverá utilizar os métodos programados no módulo `terraglue.py` em conjunto com os métodos de transformação codificados na mesma classe, garantindo assim toda a definição da lógica de processamento do job. |

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

A seguir, detalhes sobre como o usuário pode absorver todo este mar de funcionalidades exemplificado e adaptar o *template* de código para suas próprias aplicações Spark e jobs Glue.

___

## Adaptando a aplicação para finalidades próprias

No *snippet* de código acima, é possível visualizar o objeto criado a partir da classe `GlueTransformationManager` contendo dois principais argumentos utilizados como atributos:

- `ARGV_LIST`: Lista contendo a referência nominal de todos os argumentos/parâmetros utilizados no job, sejam estes criados no console ou por alguma ferramenta de IaC (Terraform ou CloudFormation, por exemplo).
- `DATA_DICT`: Dicionário contendo todas as informações necessárias das origens de dados (tabelas do Data Catalog) a serem lidas e entregues ao usuário como objetos do tipo DynamicFrame ou DataFrame (dependendo do método de leitura executado).

Dessa forma, considerando os detalhes demonstrados até aqui, usuários iniciantes ou experientes que desejam utilizar o template do **terraglue** para construir seus *jobs* Glue deverão, essencialmente, seguir quatro passos importantes no processo de consumo:

1. Adaptar o vetor de argumentos do *job* através da variável `ARGV_LIST`
2. Adaptar o dicionário com os dados a serem utilizados no *job* através da variável `DATA_DICT`
3. Criar os métodos de transformação dos dados na classe `GlueTransformationManager`
4. Adaptar o método `run()` com os dados a serem lidos e os novos métodos gerados

Todas as demais operações já estão inclusas nos métodos internos das classes disponibilizadas ao usuário e não necessitam de alterações. Em outras palavras, o usuário pode focar nas codificações relacionadas às suas próprias transformações de dados ao invés de se preocupar os elementos de configuração do *job*.

> 📌 Neste momento, é importante citar que todas as classes disponibilizadas possuem uma vasta documentação em seus respectivos arquivos. Docstrings minucisamente escritas foram entregues para que todos possam se servir das funcionalidades e compreender, de fato, tudo o que está presente em termos de argumentos e parâmetros.

___

## Continue navegando nas documentações

- [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main)
- [2. Implantando e conhecendo a infraestrutura](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md)
- 👉 [3. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/APP.md) *Você está aqui!*
- [4. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/EXAMPLES.md)
- [5. Testes unitários em jobs do Glue na AWS](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/TESTS.md)
