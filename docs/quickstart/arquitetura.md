# Arquitetura de Solução

Em uma visão de arquitetura, o módulo `datadelivery` poderia ser representado pelo desenho abaixo.

![Desenho de arquitetura](./_assets/imgs/arquitetura-v1.svg)

O desenho traz uma visão simplificada sobre algumas das funcionalidades do módulo `datadelivery`, sendo estas representadas em 4 grandes etapas:

???+ tip "Etapas de execução do módulo datadelivery"
    1. Na configuração padrão, o módulo cria *buckets* no S3 e realiza o upload automático de alguns arquivos físicos separados em diferentes prefixos, um para cada dataset/tabela
    2. Uma *policy* e uma *role* IAM são criadas automaticamente para serem assumidas por um Crawler do Glue
    3. A variável `delay_to_run_crawler` do módulo é utilizada para definir um *delay* de execução do Crawler com base no timestamp de implantação dentro de uma expressão cron
    4. Um Crawler do Glue criado pelo módulo coleta os metadados dos arquivos físicos armazenados na etapa 1 de modo a criar as tabelas necessárias no Glue Data Catalog

Continue navegando por esta página de documentação para desvendar mais detalhes sobre este módulo capaz de aprimorar seus primeiros passos na exploração de dados utilizando serviços AWS.