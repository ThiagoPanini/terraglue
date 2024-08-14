# Variáveis do Módulo

Em geral, módulos Terraform encapsulam declarações de recursos e regras específicas de modo a fornecer um "pacote pronto de funcionalidades" capaz de ser parametrizado pelos usuários. Essa parametrização (ou customização de regras) é feita através de [variáveis de entrada](https://developer.hashicorp.com/terraform/language/values/variables).

No caso do módulo `datadelivery`, usuários podem passar variáveis capazes de modificar, adaptar e customizar os recursos e regras encapsuladas no módulo, habilitando funcionalidades adicionais ou simplesmente modificando o comportamento do módulo de acordo com algumas necessidades específicas.

A tabela abaixo contempla todas as variáveis atualmente aceitas pelo módulo:

| **Variável** | **Tipo** | **Descrição** | **Default** |
| :-- | :-- | :-- | :-- |
| bucket_names_map | map(string) | Dicionário de definição de todos os nomes de buckets a serem criados na conta AWS alvo. Este dicionário deve possuir chaves identificadoras (ex: 'sor', 'sot', 'spec') cujos valores representam os nomes para os buckets a serem criados para cada contexto identificador. E obrigatório que exista, pelo menos, uma chave identificadora definida como 'sor' com o respectivo nome de bucket para armazenar dados na camada SoR. Qualquer outro identificador de chave e nome de bucket é opcional. Ao final de cada valor desse dicionário, processos automáticos do módulo irão adicionar um sufixo definido por '-<region_name>-<account_id>', onde <region_name> identifica o nome da região alvo da chamada e <account_id> o ID da conta AWS alvo da chamada. | [Ver abaixo](#bucket_names_map) |
| raw_data_key_on_bucket_names_map | string | Referência relacionada à chave do dicionário (map) da variável var.bucket_names_map do módulo utilizada para referenciar o bucket usado para armazenar dados brutos (sor, bronze, etc). | `"sor"` |
| flag_block_public_access_from_buckets | bool | Flag booleano para configurar o bloqueio de acesso público aos buckets criados pelo módulo. O valor 'True' indica o bloqueio do acesso público através do recurso Terraform `aws_s3_bucket_public_access_block`. | `true` |
| flag_upload_public_datasets | bool | Flag que habilita o upload automático de datasets públicos previamente presentes e disponibilizados na estrutura interna do módulo. | `true` |
| flag_upload_custom_datasets | bool | Flag que habilita o upload de datasets customizados fornecidos pelo próprio usuário no bucket criado pelo módulo datadelivery para o armazenamento de dados brutos (sor, bronze, etc). Se var.flag_upload_custom_datasets=true, então o usuário deve fornecer um caminho de diretório onde os dados estão armazenados através da variável var.custom_datasets_dir. | `false` |
| custom_dataset_dir | string | Diretório onde os arquivos dos datasets do usuário estão armazenados para que estes sejam coletados e enviados para o bucket de armazenamento de dados brutos no S3. É obrigatório que o usuário forneça um valor para esta variável caso var.flag_upload_custom_datasets=true. | `" "` |
| flag_create_glue_crawler | bool | Flag booleano para habilitar a criação de recursos IAM (policies e roles) relacionados a execução de um Glue Crawler pré configurado pelo no módulo datadelivery. | `true` |
| flag_create_glue_databases | bool | Flag booleano para habilitar a criação de databases no Glue Data Catalog para armazenar os resultados do processo de execução do Glue Crawler. | `true` |
| glue_databases_names_map | map(string) | Dicionário de definição de todos os nomes de databases a serem criados na conta AWS alvo. Este dicionário deve possuir chaves identificadoras (ex: 'sor', 'sot', 'spec') cujos valores representam os nomes para os databases a serem criados para cada contexto identificador. É obrigatório que exista, pelo menos, uma chave que identifique um nome de dadatabase para armazenar dados brutos (ex: 'sor' ou 'bronze'). Outros identificadores de chave e nome de bucket são opcionais (ex: 'sot', 'spec', 'silver', 'gold'). | [Ver abaixo](#glue_databases_names_map) |
| raw_data_key_on_databases_names_map | string | Referência relacionada à chave do dicionário (map) da variável var.glue_databases_names_map do módulo utilizada para referenciar o database usado para armazenar dados brutos (sor, bronze, etc). | `"sor"` |
| delay_to_run_crawler | string | Referência de tempo em segundos (s), minutos (m) ou horas (h) representando o delay para execução do Glue Crawler após a execução do módulo e implantação dos recursos. Por exemplo, var.delay_to_run_crawler = '2m' indica que o Glue Crawler será executado 2 minutos após a implantação dos recursos do módulo datadelivery. | `"2m"` |
| flag_create_athena_workgroup | bool | Flag booleano para habilitar a criação de um workgroup pré configurado do Athena para permitir a execução de consultas. | `false` |
| athena_workgroup_name | string | Nome para workgroup do Athena criado pelo módulo datadelivery | `"datadelivery-workgroup"` |
| athena_output_key_on_bucket_names_map | string | Referência relacionada à chave do dicionário (map) da variável var.bucket_names_map do módulo utilizada para referenciar o bucket usado para armazenar resultados de queries do Athena. Para criação de um workgroup do Athena pelo módulo datadelivery, espera-se que o usuário defina também a criação de um bucket S3 específico para este propósito. | `"athena"` |

## Valores Default

Para facilitar a visualização, alguns valores padrão de variáveis serão consolidados no bloco abaixo:

### bucket_names_map

```python
{
    "sor"    = "datadelivery-sor"
    "sot"    = "datadelivery-sot"
    "spec"   = "datadelivery-spec"
    "athena" = "datadelivery-athena-query-results"
    "glue"   = "datadelivery-glue-assets"
    "temp"   = "datadelivery-temp"
}
```

### glue_databases_names_map

```python
{
    "sor"  = "db_datadelivery_sor"
    "sot"  = "db_datadelivery_sot"
    "spec" = "db_datadelivery_spec"
}
```