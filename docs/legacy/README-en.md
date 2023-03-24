<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/readme/01-header-readme.png?raw=true" alt="terraglue-logo">
</div>

<div align="center">
  <br>
  
  ![GitHub release (latest by date)](https://img.shields.io/github/v/release/ThiagoPanini/terraglue?color=purple)
  ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ThiagoPanini/terraglue?color=blue)
  ![CI workflow](https://img.shields.io/github/actions/workflow/status/ThiagoPanini/terraglue/ci-terraglue-main.yml?label=ci)
  [![codecov](https://codecov.io/github/ThiagoPanini/terraglue/branch/main/graph/badge.svg?token=7HI1YGS4AA)](https://codecov.io/github/ThiagoPanini/terraglue)

</div>

## Table of Contents
- [Table of Contents](#table-of-contents)
- [What is terraglue?](#what-is-terraglue)
  - [Who can use terraglue?](#who-can-use-terraglue)
  - [What do I need to start?](#what-do-i-need-to-start)
  - [First steps](#first-steps)
- [Project architecture and repository organization](#project-architecture-and-repository-organization)
- [Are you interested and want to know more?](#are-you-interested-and-want-to-know-more)
  - [The story behind the creation](#the-story-behind-the-creation)
  - [A complete journey of use](#a-complete-journey-of-use)
  - [Contributing](#contributing)
  - [FAQ](#faq)
- [Contact me](#contact-me)
- [References](#references)

___

## What is terraglue?

**terraglue** is a product created to facilitate the journey of learning, using and optimizing Glue Jobs on AWS. For making it cleaner, it is possible to divide its functionalities in two major groups:

- 🛠️ **Infra:** with terraglue, users can deploy all infrastructure needed to launch and run Glue jobs in their AWS sandbox environment, including s3 buckets, IAM roles and tables in Data Catalog.
- 🚀 **Aplicação:** furthermore, a Spark application model is available with a series of classes, methods and functions providing an extra level of abstraction for common operations on the AWS Glue and simplifying the user overhead on building its own Glue job.


### Who can use terraglue?

Are you looking to b using Glue on AWS and don't know where to begin? Are you already using the service and want to optimize your job with thousands of lines of code? Would you like to use ready-made data transformation functions and methods with Spark? Are you stuck trying to learn about unit tests and need a direction?

If your answear was "yes" for at least one of the questions above, so **terraglue** is the deal for you!


### What do I need to start?

Start using **terraglue** is simple and fast. You will ned:

- ☁️ [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) available for use
- 🔑 [Programatic access](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html) on the account with an `access_key_id` and a `secret_access_key`
- ⛏ [Terraform](https://www.terraform.io/) installed (version >=1.0)


### First steps

It all starts with cloning the repository:

```bash
git clone https://github.com/ThiagoPanini/terraglue.git
```

So, go to the repository folder and run the Terraform commands below to initialize the modules, show the deploy plan and execute the deploy planned:

```bash
# Changing the directory
cd terraglue/infra

# Initializing terraform modules and applying the deploy
terraform init
terraform plan
terraform apply
```

That's it! Now you have applied on your AWS account all the elements needed to start your learning journey on AWS Glue the best way possible! For a more detailed tutorial with extra explanation on the infrastructure provided, see [getting started link](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md). If you want to know more about the project architecture, just keep going on this documentation.

___

## Project architecture and repository organization

Now that you know better about the project, it's time to show all the architecture behind the features introduced before. At the end of the day, **terraglue** is a IaC (Infrastructure as Code) project built with [Terraform](https://www.terraform.io/) runtime and divided into modules used for deploying different AWS services that, together, form the whole project consumption idea.

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/readme/diagram-user-view.png?raw=true" alt="terraglue-user-view">
</div>
<br>

In summary, the resourced in the Terraform modules are represented by:

- 🧺 S3 buckets for storing data and *assets*
- 🚨 IAM policies and role for managing access
- 🎲 Databases and tables in the Data Catalog according to the local data provided
- 🪄 A Glue job already configured with a practical example

By fulfilling the requirements, users will have in hands their own "portable AWS environment" with the following resources:

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/imgs/readme/diagram-product-view.png?raw=true" alt="terraglue-resources">
</div>
<br>

Considering the architecture showed above, the **terraglue** repo is organized on the following way:

| 📂 **Folder** | ⚙️ **Desceiption** |
| :-- | :-- |
| `./app` | Here you can find the Python script available as standard for deploying a Glue job on AWS following the best code and documentation practices. The script considers a scenario of creating a base in [SoT](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/) (*Source of Truth*) layer using a public dataset called [BR ECommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). |
| `./data` | In this directory, you will be able to identify all data sources available as an example for running a Glue job. The data is present and organized in order to simulate a standard Data Lake structure in distributed environments, where the database, table name and parent directories are defined in relation to the files themselves. (i.e `db/table/file.ext`). |
| `./docs` | Here the user will be able to find all the diagrams and images used in the project documentation. |
| `./infra` | In this directory, it will be possible to find all Terraform declarations responsible for the implementation of the necessary infrastructure to use the project on AWS. A specific section on this part will be detailed below. |

___


## Are you interested and want to know more?

After defining what **terraglue** is and providing a macro view of its solution architecture, it is time to provide some inputs and fundamental routes to materialize all the intrinsic value of the initiative.

### The story behind the creation

> **Note**
> This section is for curiosity purposes only. If you are interested in knowing a little more about the solution's conception history, click on the dropdown and have a good read 🤓

<details>
  <summary>🪄 Once upon a time there was an Analytics Engineer...</summary>

  > ...who was starting his learning journey on Glue. He didn't know where to start, so he looked up some videos, read some documentation, and finally got ready to run something more practical in his personal environment. In his hands, that Engineer had an AWS sandbox account and a lot of desire to learn.
  
  > At first, he started by simulating some storage structures close to what he found in his work environment, such as s3 buckets responsible for storing data in different layers (SoR, SoT and Spec). As his sandbox account was ephemeral and automatically deleted within a few hours, every day the Engineer logged into a new account and manually created buckets to serve as a repository for the files. Speaking of which, obtaining public data and subsequent ingestion in the aforementioned environment was also part of the manual tasks performed on a daily basis.
  
  > Uploading the files was not enough because, in the dynamics of using s3 as a Data Lake, it is also necessary to catalog the data in the AWS Data Catalog, adding even more operational effort to the Engineer's routine (and we haven't even gotten to Glue yet) .

  > Continuing with the preparation of the environment, the Engineer was now faced with an extremely challenging task: IAM roles. Which permissions to use? Will it be necessary to create specific policies? What does Glue need to work? After much study, the Engineer was able to arrive at a set of policies defined in a timely manner to allow Glue jobs to run in his environment. Now, every day, in addition to creating buckets, ingesting and cataloging files, the Engineer should also create policies and at least one IAM role to be able to start his journey in Glue.

  > Finally, after a lot of operational effort and many broken stones, the Engineer was able to prepare his entire environment to be able to create his Glue job and learn to use it with cataloged public data. If the obstacles so far weren't enough, the Engineer was now faced with an extremely complex challenge involving the dynamics of creating Spark applications within Glue. GlueContext? DynamicFrame? SparkSession? What does it all mean and how can I simply read, transform and catalog my data?

  > Well, at this moment the story of our protagonist begins to turn. As in great movies or renowned anime, it is from this point that the hero begins to be born and all challenges begin to be overcome. Gradually, the Engineer realized that the environment preparation processes, which were hard to replicate daily in his environment, could, extraordinarily, be automated using an IaC tool.
  
  > And so he starts to develop pieces of code that automatically create s3 buckets whenever he goes on his daily learning journey. In addition to buckets, it also encodes an automatic way to upload and catalog ready-to-use files. Policies and the IAM role also enter this package and are instantly created in your new infrastructure automation project. Finally, the creation of the Glue job is also automated and, at this moment, the Engineer has in his hands all the necessary infrastructure to use the Glue service on AWS at the touch of a single command. However, the icing on the cake was still missing.

  > Once the infrastructure was automated, the Engineer realized some Spark application code patterns that could facilitate the development journey of users in Glue jobs. Does the user really need to instantiate a GlueContext in the main job script? Could some additional module abstract this step? And so, the Engineer started working on a series of relevant functionalities encapsulated in an additional module capable of being imported into the application's main script, allowing users to focus exclusively on their respective data transformation methods.

  > With that, now not only an entire infrastructure would be provisioned, but also an entire reference model in the development of Spark applications in Glue jobs would be delivered to the end user. The terraglue MVP was ready.
</details>

...and lived happily ever after with no *issues* in the repository!

___

### A complete journey of use

If everything is still a bit abstract so far, don't worry! There is a massive set of highly detailed documentation so that the full power of **terraglue** can be extracted from its users. The set of links below promises to guide the reader to all the journeys present in the dynamics of using the solution.


- 👉 [1. Main project documentation](https://github.com/ThiagoPanini/terraglue/tree/main) *You are here!*
- [2. Deploying and knowing the infrastructure](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md) 
- [3. A proposal for standardizing Glue jobs](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/APP.md) 
- [4. Practical examples of using the solution](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/EXAMPLES.md)
- [5. Unit testing Glue jobs on AWS](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/TESTS.md)

___

### Contributing

Everyone is very welcome to contribute with evolutions and new features of this project lovingly made available to the community. For more details on this process, visit the file [CONTRIBUTING.md](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/CONTRIBUTING.md)

___

### FAQ

<details>
  <summary>📌 "I found out about terraglue by chance. How do I know if he can help me with something?"</summary>

  > 💡 *Basically, terraglue has different candidate user profiles ranging from beginners to the most experienced. If you want to take your first steps on AWS using Glue, here you can have a tool capable of providing an end to end journey at the touch of a command. If you are already immersed in this journey and have technical questions about Spark applications, unit tests, Python modules or Terraform, this is also your place!*
</details>

<details>
  <summary>📌 "I want to activate a <i>toolkit</i> in my AWS account to learn how the dynamics of using Glue work in practice. Which way should I go?"</summary>

  > 💡 *To achieve this goal, just follow the steps in the documentation [Deploying and knowing the infrastructure](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/INFRA.md). In it, you will find all the necessary details to have in your hands, at the touch of a few commands, an entire infrastructure ready to contemplate your journey of using Glue on AWS.*
</details>

<details>
  <summary>📌 "I'm not interested in the infrastructure itself, but the Spark application model and the ready-to-use functions in my Glue job. Where do I collect more information about it and how can I use these ready-made code blocks in my application?"</summary>

  > 💡 *For this scenario, the documentation [A proposed standardization of Glue jobs](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/APP.md) can guide you through all the steps necessary to understand the developed Spark application model and how to use it in your own projects. Additionally, the documentation [Practical examples of using the solution](https://github.com/ThiagoPanini/terraglue/blob/main/docs/markdown/EXAMPLES.md) can be an excellent complement to analyze, step by step, the entire the process of obtaining and adapting the Spark application model.*
</details>

<details>
  <summary>📌 "I already have a Glue job running in production, but I have difficulty maintaining it due to the complexity of the application and the number of lines of code. How can I use terraglue to optimize this process?"</summary>

  > 💡 *terraglue has an additional Python module present in <code>app/terraglue.py</code> with NUMEROUS functionalities encapsulated and ready to use. You can adapt your code to use this module and use classes and methods specially created to ease your Spark application development journey with the best code development practices. With this dynamic, you can only worry about programming the necessary data transformations for your ETL process. For the rest, rely on the ready methods of the <code>terraglue.py</code> module.*
</details>

<details>
  <summary>📌 "Are there any costs involved for using terraglue?"</summary>

  > 💡 *This is a very interesting and important question. There are no costs to use terraglue as it is an open source solution shared with the entire community. HOWEVER, it is essential to mention that the resources created by terraglue in your AWS environment may eventually incur costs. Therefore, it is critical that terraglue users understand the potential fees involved with related services before utilizing the solution.*
</details>

___

## Contact me

- [Thiago Panini - LinkedIn](https://www.linkedin.com/in/thiago-panini/)
- [paninitechlab @ hashnode](https://panini.hashnode.dev/)

## References

**_AWS Glue_**
- [AWS - Glue Official Page](https://aws.amazon.com/glue/)
- [AWS - Jobs Parameters Used by AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html)
- [AWS - GlueContext Class](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html#aws-glue-api-crawler-pyspark-extensions-glue-context-create_dynamic_frame_from_catalog)
- [AWS - DynamicFrame Class](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
- [Stack Overflow - Job Failing by Job Bookmark Issue - Empty DataFrame](https://stackoverflow.com/questions/50992655/etl-job-failing-with-pyspark-sql-utils-analysisexception-in-aws-glue)
- [AWS - Calling AWS Glue APIs in Python](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html)
- [AWS - Using Python Libraries with AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#aws-glue-programming-python-libraries-zipping)
- [Spark Temporary Tables in Glue Jobs](https://stackoverflow.com/questions/53718221/aws-glue-data-catalog-temporary-tables-and-apache-spark-createorreplacetempview)
- [Medium - Understanding All AWS Glue Import Statements and Why We Need Them](https://aws.plainenglish.io/understanding-all-aws-glue-import-statements-and-why-we-need-them-59279c402224)
- [AWS - Develop and test AWS Glue jobs Locally using Docker](https://aws.amazon.com/blogs/big-data/develop-and-test-aws-glue-version-3-0-jobs-locally-using-a-docker-container/)
- [AWS - Creating OpenID Connect (OIDC) identity providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)

**_Terraform_**
- [Terraform - Hashicorp Terraform](https://www.terraform.io/)
- [Terraform - Conditional Expressions](https://developer.hashicorp.com/terraform/language/expressions/conditionals)
- [Stack Overflow - combine "count" and "for_each" on Terraform](https://stackoverflow.com/questions/68911814/combine-count-and-for-each-is-not-possible)

**_Apache Spark_**
- [SparkByExamples - Pyspark Date Functions](https://sparkbyexamples.com/pyspark/pyspark-sql-date-and-timestamp-functions/)
- [Spark - Configuration Properties](https://spark.apache.org/docs/latest/configuration.html)
- [Stack Overflow - repartition() vs coalesce()](https://stackoverflow.com/questions/31610971/spark-repartition-vs-coalesce)
  
**_GitHub_**
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- [Semantic Release](https://semver.org/)
- [GitHub - Angular Commit Message Format](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#-commit-message-format)
- [GitHub - commitlint](https://github.com/conventional-changelog/commitlint)
- [shields.io](https://shields.io/)
- [Codecoverage - docs](https://docs.codecov.com/docs)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Continuous Integration with GitHub Actions](https://endjin.com/blog/2022/09/continuous-integration-with-github-actions)
- [GitHub - About security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [GitHub - Securing deployments to AWS from GitHub Actions with OpenID Connect](https://www.eliasbrange.dev/posts/secure-aws-deploys-from-github-actions-with-oidc/#:~:text=To%20be%20able%20to%20authenticate,Provider%20type%2C%20select%20OpenID%20Connect.)
- [GitHub - Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Eduardo Mendes - Live de Python #170 - GitHub Actions](https://www.youtube.com/watch?v=L1f6N6NcgPw&t=3043s&ab_channel=EduardoMendes)

**_Docker_**
- [GitHub Docker Run Action](https://github.com/marketplace/actions/docker-run-action)
- [Using Docker Run inside of GitHub Actions](https://aschmelyun.com/blog/using-docker-run-inside-of-github-actions/)
- [Stack Overflow - Unable to find region when running docker locally](https://stackoverflow.com/questions/62546743/running-aws-glue-jobs-in-docker-container-outputs-com-amazonaws-sdkclientexcep)

**_Testes_**
- [Eduardo Mendes - Live de Python #167 - Pytest: Uma Introdução](https://www.youtube.com/watch?v=MjQCvJmc31A&)
- [Eduardo Mendes - Live de Python #168 - Pytest Fixtures](https://www.youtube.com/watch?v=sidi9Z_IkLU&t)
- [Databricks - Data + AI Summit 2022 - Learn to Efficiently Test ETL Pipelines](https://www.youtube.com/watch?v=uzVewG8M6r0&t=1127s)
- [Real Python - Getting Started with Testing in Python](https://realpython.com/python-testing/)
- [Inspired Python - Five Advanced Pytest Fixture Patterns](https://www.inspiredpython.com/article/five-advanced-pytest-fixture-patterns)
- [getmoto/moto - mock inputs](https://github.com/getmoto/moto/blob/master/tests/test_glue/fixtures/datacatalog.py)
- [Codecov - Do test files belong in code coverage calculations?](https://about.codecov.io/blog/should-i-include-test-files-in-code-coverage-calculations/)
- [Jenkins Issue: Endpoint does not contain a valid host name](https://issues.jenkins.io/browse/JENKINS-63177)

**_Others_**
- [Differences between System of Record and Source of Truth](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/)
- [Olist Brazilian E-Commerce Data](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [Stack Overflow - @staticmethod](https://stackoverflow.com/questions/6843549/are-there-any-benefits-from-using-a-staticmethod)

