# Quickstart: A Detailed Tutorial

This section will presente a more detailed setup tutorial with screenshots and a guided step by step to start using *terraglue* and all its features.

## Configuring AWS Credentials

As said [here](basic-tutorial.md#quickstart-a-basic-tutorial), one of the prerequisites of *terraglue* is the existance of an AWS account and an user with programatic access through `access_key_id` and `secret_access_key`. That's how Terraform will try do the AWS calls needed to deploy the infrastructure declared.

So, assuming users will have the keys mentioned above, the command below is needed to configure AWS credentials in a local environment:

```bash
# Configuring aws credentials
aws configure
```

??? example "Example of configuring AWS credentials"
    ![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/quickstart/01-aws-configure.png)

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
    ![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/quickstart/02-git-clone.png)

Once cloned, the remote *terraglue* repository will be available for users in their local environment.

???+ tip "Pulling the remote repository"
    The local *terraglue* repository cloned by users is static by default. It means that it's possible that users may not have the latest features included on the remote repo. So, it could be a good practice to always run a `git pull` command to obtain the state-of-art of repository features.


## Instaling Terraform Modules

After cloning the repo, let's navigate to the `infra/` repository folder on the project directory and initialize the terraform modules through the command below:

```bash
# Initializing terraform modules
cd terraglue/infra
terraform init
```

??? example "Example of initializing terraform modules from terraglue"
    ![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/quickstart/03-terraform-init.png)

After this operation, the users will be ready to apply the infrastructure deploy at a target AWS environment. But first let's see how the deploy planning is shown.

## Planning Deploy

Before deploying the infrastructure, it's reasonable to take a look at the deploy plan. It can be reached by running the terraform command below:

```bash
# Showing the deploy plan
terraform plan
```

??? example "Example of showing the plan of infrastructure deploy"
    ![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/quickstart/04-terraform-plan.png)

## Deploying the Infrastructure

Finally, we can execute the command for deploying the infrastructure for enabling all terraglue features in an AWS account:

```bash
# Deploying infra
terraform apply
```

??? example "Example of deploying the infrastructure"
    ![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/quickstart/05-terraform-apply.png)

And that's it! This detailed tutorial embraced all steps needed to enable *terraglue* features. Keep searching on the docs to find practical examples and to deep dive into *terraglue*!