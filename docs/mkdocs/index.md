# Terraglue: A Poweful Tool for Learning Glue

## Overview

Hi everyone! Welcome to the official documentation page for **terraglue**, an open source Terraform module developed in order to provide an easy way to deploy a Glue job in any AWS account.

- Are you using Glue for the first time and want to see an end to end ETL example in AWS?
- Do you already have a Spark application and want to deploy it as a Glue job in AWS?
- Do you want to automate the Glue job setup using an IaC tool such as Terraform?
- Have you ever wanted to go the next level on developing Glue jobs?

🌖 Try *terraglue*!

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/raw/main/docs/assets/imgs/header-readme.png?raw=true" alt="terraglue-logo">
</div>

<div align="center">  
  <br>

  <img src="https://img.shields.io/github/v/release/ThiagoPanini/terraglue?color=purple" alt="Shield github release version">
  
  <img src="https://img.shields.io/github/last-commit/ThiagoPanini/terraglue?color=purple" alt="Shield github last commit">
  
  <img src="https://img.shields.io/github/actions/workflow/status/ThiagoPanini/terraglue/ci-main.yml?label=ci" alt="Shield github CI workflow">

  <a href='https://terraglue.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/terraglue/badge/?version=latest' alt='Documentation Status' />
  </a>

  <a href="https://codecov.io/gh/ThiagoPanini/terraglue" > 
  <img src="https://codecov.io/gh/ThiagoPanini/terraglue/branch/main/graph/badge.svg?token=7HI1YGS4AA"/> 
  </a>

  <a href="https://codecov.io/gh/ThiagoPanini/terraglue" > 
    <img src="https://codecov.io/github/ThiagoPanini/terraglue/branch/main/graph/badge.svg?token=7HI1YGS4AA"/> 
  </a>

</div>

___

## Features

- ✌️ Available in two different operation modes: "learning" and "production"
- 🤖 Enable users to deploy a preconfigured Glue job with a complete end-to-end ETL example when using "learning" mode
- 🚀 Enable users to deploy a custom Glue job according to user needs when using "production" mode
- 👉 Have your Glue job ready and running at the touch of a Terraform module call


## How Does it Work?

When **terraglue** module is called in a Terraform project, an operation mode must be chosen. There are two options: *"learning"* mode and *"production"* mode. According to this decision, different things can happen in the target AWS account.

The *learning* mode helps users to understand more about Glue jobs on AWS by providing a complete example with all resources needed to start exploring Glue. It works as following:

???+ info "🤖 Learning mode"
    1. A sample pyspark application is uploaded in a given S3 bucket to be the main script for the Glue job
    2. An auxiliar python file is also uploaded in S3 with useful transformation functions for the job
    3. An IAM role is created with basic permissions to run a Glue job
    4. A KMS key is created to be used in the job security configuration
    5. Finally, a preconfigured Glue job is deployed in order to provide users a example of a SoT table creation using Brazilian E-Commerce data from [datadelivery](https://datadelivery.readthedocs.io/en/latest/)

By the other hand, the *production* mode enables users to configure and deploy their own Glue jobs in AWS. The under the hood operation depends on how users configure variables on module call. In summary, it works as following:

???+ info "🚀 Production mode"
    1. In this mode, users have the chance to use all the terraglue module variables to customize the deploy
    2. A custom Glue job is deployed in the target AWS account using the variables passed by users on module call


## Combining Solutions

The *terraglue* Terraform module isn't alone. There are other complementary open source solutions that can be put together to enable the full power of learning analytics on AWS. [Check it out](https://github.com/ThiagoPanini) if you think they could be useful for you!

![A diagram showing how its possible to use other solutions such as datadelivery, terraglue and sparksnake](https://github.com/ThiagoPanini/datadelivery/blob/main/docs/assets/imgs/products-overview-v2.png?raw=true)


## Read the Docs

- If you like stories, check out the [Project Story](story.md) to see how terraglue was born
- To take the first steps on terraglue, don't forget to check the [Quickstart](./quickstart/gettingstarted.md) section
- Everyone likes demos, right? Check the [Demos](./demos/about.md) section to see terraglue in practice
- Don't forget to check the [Variables](./variables/variables.md) section to see different ways to customize terraglue


## Contacts

- :fontawesome-brands-github: [@ThiagoPanini](https://github.com/ThiagoPanini)
- :fontawesome-brands-linkedin: [Thiago Panini](https://www.linkedin.com/in/thiago-panini/)
- :fontawesome-brands-hashnode: [panini-tech-lab](https://panini.hashnode.dev/)
