*Auxiliando usuários à contribuírem com o projeto*

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Considerações iniciais](#considerações-iniciais)
- [Abrindo PRs](#abrindo-prs)
- [Issues](#issues)
- [Considerações finais](#considerações-finais)

___

## Considerações iniciais

Este é um repositório *open source* criado e desenvolvido como um projeto pessoal disponibilizado integralmente para a comunidade. Qualquer usuário pode utilizar suas funcionalidades e, obviamente, contribuir com novas melhorias que façam sentido.

Visando proporcionar uma maior organização no processo de contribuição, o modelo de [feature branch](https://launchdarkly.com/blog/dos-and-donts-of-feature-branching/?utm_source=google&utm_medium=cpc&utm_campaign=NA_-_Search_-_Dynamic&utm_term=&utm_content=&obility_id=126914704794-529046860555&_bt=529046860555&_bm=&_bn=g) foi adotado e, assim sendo, para cada nova contribuição, os usuários devem criar uma nova *branch* a partir da *branch* `develop` de preferência seguindo a sintaxe `feature/<funcionalidade>`.

```bash
# Navegando até a branch develop
git checkout develop

# Criando nova branch
git checkout -b feature/nova-funcionalidade
```

Uma vez desenvolvida a nova funcionalidade, basta realizar os *commits* para atualização do repositório remoto seguida da abertura de um *pull request*.

___

## Abrindo PRs

Neste repositório, será possível encontrar um modelo pronto para documentação dos *pull requests* abertos. Isso facilita análises e decisões relacionadas à integração do novo código nas *branches* alvo.

- 📝 [Template de PRs](https://github.com/ThiagoPanini/terraglue/blob/main/.github/PULL_REQUEST_TEMPLATE/default.md)

___

## Issues

Issues são uma forma de abrir algum tipo de comunicado importante com os desenvolvedores do projeto. Dessa forma, também visando garantir uma boa organização das relações envolvidas, *templates* de *issues* foram disponibilizados aos usuários de acordo com algumas categorias mapeadas.

- :lady_beetle: [Template de issue: bug report](https://github.com/ThiagoPanini/terraglue/blob/main/.github/ISSUE_TEMPLATE/bug-report.md)
- :books: [Template de issue: documentation](https://github.com/ThiagoPanini/terraglue/blob/main/.github/ISSUE_TEMPLATE/documentation.md)
- :package: [Template de issue: feature request](https://github.com/ThiagoPanini/terraglue/blob/main/.github/ISSUE_TEMPLATE/feature-request.md)
- :pray: [Template de issue: help needed](https://github.com/ThiagoPanini/terraglue/blob/main/.github/ISSUE_TEMPLATE/help-needed.md)
- :question: [Template de issue: question](https://github.com/ThiagoPanini/terraglue/blob/main/.github/ISSUE_TEMPLATE/question.md)

___

## Considerações finais

Simplesmente clone, use, contribua e seja feliz! :)