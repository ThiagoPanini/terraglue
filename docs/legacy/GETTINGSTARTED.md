<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/docs/visual-and-docs-refactor/docs/imgs/gettingstarted/01-header-gettingstarted.png?raw=true" alt="terraglue-logo">

  <i>Este é um tutorial básico sobre como utilizar as funcionalidades do terraglue</i>
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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-gettingstarted-aws-configure.png" alt="terraglue-aws-configure">
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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-gettingstarted-git-clone.png" alt="terraglue-git-clone">
  </div>
</details>
<br>

Com isso, todos os códigos alocados no projeto, em sua versão mais recente, poderão ser acessados da forma mais cômoda para o usuário, seja através da própria linha de comando ou até mesmo utilizando uma IDE.

<details>
  <summary>📷 Clique para visualizar a imagem</summary>
  <div align="left">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-gettingstarted-ls-terraglue.png" alt="terraglue-ls">
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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-gettingstarted-terraform-init.png" alt="terraglue-terraform-init">
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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-gettingstarted-terraform-plan.png" alt="terraglue-terraform-plan">
  </div>
</details>
<br>

> ⚠️ Como o **terraglue** comporta uma série de declaração de recursos, o *output* do comando `terraform plan` comporta uma série de detalhes. Se julgar necessário, analise com cuidado todas as implantações a serem realizadas em sua conta alvo. Ter controle sobre este passo garante uma total autonomia sobre tudo o que está sendo realizado, incluindo possíveis gastos na provedora cloud. Em caso de dúvidas, verifique a [documentação](https://github.com/ThiagoPanini/terraglue/blob/develop/README.md) do projeto.

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
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/develop/docs/imgs/terraglue-gettingstarted-terraform-apply.png" alt="terraglue-terraform-apply">
  </div>
</details>
<br>

Após um determinado período, espera-se que uma mensagem de sucesso seja entregue ao usuário, garantindo assim que todas as inclusões e todos os recursos foram devidamente implantados no ambiente AWS. A partir deste ponto, o usuário terá em mãos todas as funcionalidades do **terraglue** disponíveis para uso!

___

## Continue navegando nas documentações

- [1. Documentação principal do projeto](https://github.com/ThiagoPanini/terraglue/tree/main)
- 👉 [2. Instalação e primeiros passos](https://github.com/ThiagoPanini/terraglue/blob/main/GETTINGSTARTED.md) *Você está aqui!*
- [3. Infraestrutura provisionada](https://github.com/ThiagoPanini/terraglue/blob/main/INFRA.md) 
- [4. Uma proposta de padronização de jobs Glue](https://github.com/ThiagoPanini/terraglue/blob/main/APP.md) 
- [5. Exemplos práticos de utilização da solução](https://github.com/ThiagoPanini/terraglue/blob/main/EXAMPLES.md)
- [6. Testes unitários em jobs do Glue na AWS](https://github.com/ThiagoPanini/terraglue/blob/main/TESTS.md)