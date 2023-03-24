# Quickstart: A Detailed Tutorial

This section will presente a more detailed setup tutorial with screenshots and a guided step by step to start using *terraglue* and all its features.

## Configuring AWS Credentials

As said [here](basic-tutorial.md#quickstart-a-basic-tutorial), one of the prerequisites of *terraglue* is the existance of an AWS account and an user with programatic access through `access_key_id` and `secret_access_key`. That's how Terraform will try do the AWS calls needed to deploy the infrastructure declared.

So, assuming users will have the keys mentioned above, the command below is needed to configure AWS credentials in a local environment:

```bash
aws configure
```

???+ example "Configuring AWS Credentials"
    ![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/01-aws-configure.png)

## Cloning the Source Repository

## Instaling Terraform Modules

## Planning Deploy

## Deploying the Infrastructure