# Quickstart: A Basic Tutorial

As an IaC project written mainly in Terraform, *terraglue* doesn't have complex prerequisites. You will just need the following to start using it:

- ☁️ [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) available for use
- 🔑 [Programatic access](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html) on the account with an `access_key_id` and a `secret_access_key`
- ⛏ [Terraform](https://www.terraform.io/) installed (version >=1.0)

## First Steps

It all starts by cloning the source repository using the following code:

```bash
git clone https://github.com/ThiagoPanini/terraglue.git
```

After the cloning, go to the local repository folder created and run the Terraform commands to initialize the modules and deploy all infrastructure in your AWS account.

```bash
# Changing the directory
cd terraglue/infra

# Initializing terraform modules and applying the deploy
terraform init
terraform apply
```

That's it! After successfully running the commands above, you will have a bunch of pre configured services ready to use in your analytics journey. There are many possibilities available!

???+ warning "Couldn' deploy the infrastructure?"
    If you couldn't, for any reason, reach the success on this setup tutorial, please check the [detailed tutorial](detailed-tutorial.md) with a guided step by step for start using *terraglue*.