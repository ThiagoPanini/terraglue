# Getting Started with terraglue

## Prerequisites

For users interested in using **terraglue** to improve their journey on deploying Glue jobs in AWS, it's important to establish the following prerequisites:

- ☁️ [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) available for use
- 🔑 [Programatic access](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html) on the account with an `access_key_id` and a `secret_access_key`
- ⛏ [Terraform](https://www.terraform.io/) installed (version >=1.4.6)

## Operation Modes

As stated in the [home page](../index.md#how-does-it-work) (and it's worth to emphasize here), there are two operation modes availbe for users:

- 🤖 **Learning mode** enables users to deploy a sample Glue job with a bunch of preconfigured services, such as IAM role, KMS key and a Spark application with a complete ETL process. This operation mode is perfect for everyone interested on how Glue works and it should be combined with [datadelivery](https://datadelivery.readthedocs.io/en/latest/) features (read more on the tip below)
- 🚀 **Production mode** makes it possible to users to deploy their own Glue jobs in AWS. In essence, everything in this operation mode is guided by users. It means that users should configure their Terraform project and pass appropriate variables when calling terraglue in order to deploy their Glue jobs.

??? tip "A final tip about terraglue operation modes before going ahead"
    Well, that was a lot about operation modes in **terraglue**, right? I have no intention to get stuck in this subject but it's important to ensure that this feature really came to help and not to turn things more complex.

    The *learning* mode is worth for beginners who want to check everything that is needed in order do deploy and run a Glue job in AWS. This mode configures terraglue to deploy a Spark application in Glue that uses public datasets to create an ETL process that reads, transform and write curated data. But what about those public datasets? And here's a important point:

    :material-alert-decagram:{ .mdx-pulse .warning } The data sources used in the sample Glue job provided by terraglue when called with learning mode come from the [datadelivery](https://datadelivery.readthedocs.io/en/latest/) Terraform module. So, in order to use terraglue with learning mode, users should combine it with **datadelivery** to get the full experience. Check the **datadelivery** docs to learn more about it.
    
    By the other hand, the *production* mode in terraglue doesn't have any other project dependency as it was created to provide users the ability to deploy their own jobs with their own configuration. An important message when using this operation mode takes place on the need to look at all terraglue module variables in order to configure and call it correctly.

## Calling the Module

So, with all said, to call the latest version of **terraglue** module, users just have to adapt the following code block in their own Terraform project:

```python
# Calling terraglue module
module "terraglue" {
  source = "git::https://github.com/ThiagoPanini/terraglue?ref=main"

  mode = "learning"
  # OR mode = "production"

  # [...] optional variables to configure the module
}
```

To learn more about Terraform module sources, this [documentation](https://developer.hashicorp.com/terraform/language/modules/sources#github) can help.

## Next Steps

- To get a hands-on vision of everything that happen after calling the **terraglue** module, don't forget to check the [Demo](../demos/about.md) section
- A complete list of all **terraglue** module variables is available in the [Variables](../variables/variables.md) section