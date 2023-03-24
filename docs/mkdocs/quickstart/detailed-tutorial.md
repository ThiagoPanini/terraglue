# Quickstart: A Detailed Tutorial

This section will presente a more detailed setup tutorial with screenshots and a guided step by step to start using *terraglue* and all its features.

## Configuring AWS Credentials

As said [here](basic-tutorial.md#quickstart-a-basic-tutorial), one of the prerequisites of *terraglue* is the existance of an AWS account and an user with programatic access through `access_key_id` and `secret_access_key`. That's how Terraform will try do the AWS calls needed to deploy the infrastructure declared.

So, assuming users will have the keys mentioned above, the command below is needed to configure AWS credentials in a local environment:

```bash
aws configure
```

??? example "Example of configuring AWS credentials"
    ![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/quickstart-tutorial/01-aws-configure.png)

It's important to mention that this AWS credentials setup is only needed once! Users should do this setup again only if their credentials change.


## Cloning the Source Repository

After successfully configuring credentials, the next step of this tutorial shows the repository cloning. It can be reached through any of the following commands:

```bash
# Cloning source repo with HTTPS
git clone https://github.com/ThiagoPanini/terraglue.git
```

```bash
# Cloning source repo with SSH
git clone git@github.com:ThiagoPanini/terraglue.git
```

??? example "Example of cloning the source repository"
    ![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/quickstart-tutorial/02-git-clone.png)

Once cloned, the remote *terraglue* repository will be available for users in their local environment.

???+ tip "Pulling the remote repository"
    The local *terraglue* repository cloned by users is static by default. Maybe new features could be added since the first time users cloned the repo, so it could be a good practice to always run a `git pull` command to obtain the state-of-art of repository features.


## Instaling Terraform Modules

## Planning Deploy

## Deploying the Infrastructure