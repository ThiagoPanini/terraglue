# Project Story

For everyone reading this page, I ask a poetic licence to tell you a story about the challenges I faced on my analytics learning journey using AWS Glue and what I've done to overcome them.

🪄 This is a story of launching *terraglue* for improving everyone's experience on learning AWS Glue.

![Snoopy reading a book](https://i.giphy.com/media/9X6OGGZ2SNyQ8/giphy.webp)

## How it All Started

First of all, It's important to provide some context on how it all started. I'm an Analytics Engineer working for a financial company who have a lot of data and a number even higher of opportunities on using it. The company adopted the Data Mesh architecture for giving more autonomy to the data teams for building and sharing their own datasets through three different layers: SoR (System of Record), SoT (Source of Truth) and Spec (Specialized).

???+ info "Know more about SoR, SoT and Spec"
    There are a lot of articles explaining the Data Mesh architecture and the differences between layers SoR, SoT and Spec for storing and sharing data. In fact, this is a really useful way to improve analytics on organizations.

    If you want to know a little bit more about it, there are some links that can help you on this mission:

    - 🔗 [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html)
    - 🔗 [Building a System of Record vs. a Source of Truth](https://www.integrify.com/blog/posts/system-of-record-vs-source-of-truth/)
    - 🔗 [The Difference Between System of Record and Source of Truth](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/)

So, the company decided to mainly use AWS services for all this journey. From analytics perspective, services like Glue, EMR, Athena and Quicksight just popped up as really good options to solve some real problems in the company.

And that's how the story begins: an Analytics Engineer trying his best to deep dive into those services in his personal environment for learning everything he can.

## First Steps

Well, after deciding to start it on learning more about AWS Glue for developing ETL jobs, I searched for documentation pages, watched some videos for preparing myself and talked with other developers to collect thoughts and experiences about the whole thing.

After a little while, I found myself ready to start building something useful. In my hands, I had an AWS sandbox account and a noble desire to learn.

![Michael B. Jordan on Creed movie](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzBhZjAxNjY0ODUzMmVhYzI4MmJlM2IxYjQ4NzRjMzU2ZGIzNzQyYiZjdD1n/WldnJerxYdPC8/giphy.gif)

???+ info "An important information about this AWS sandbox account"
    The use of an AWS sandbox account can be explained by a subscription that I had in a learning platform. The learning platform allowed subscribers to use an AWS environment for learning purposes and that was really nice. Still, it was an ephemeral environment with an automatic shut off mechanism after a few hours. This behavior is one of the key points of the story. Keep that in mind. You will know why.

## Creating the Storage Layers

I started to get my hands dirty by creating S3 buckets to replicate something next to a Data Lake storage architecture in a Data Mesh approach. So, one day I just logged in my AWS sandbox account and create the following buckets:

- A bucket for storing SoR data
- A bucket for storing SoT data
- A bucket for storing Spec data
- A bucket for storing Glue assets
- A bucket for storing Athena query results

[![Storage resources](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-storage.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-storage.png)


## Uploading Files on Buckets

Once the storage structures was created, I started to search for public datasets do be part of my learning path. The idea was to upload some data into the buckets to make it possible to do some analytics, such as creating ETL jobs or even querying with Athena.

So, I found the excellent [Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) on Kaggle and it fitted perfectly. I was now able to download the data and upload it on the SoR bucket to simulate some raw data that was available for further analysis in an ETL pipeline.

And now my diagram was like:

[![Storage resources with data](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-data.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-data.png)

## Cataloging Data

Upload data on S3 buckets wasn't enough to have a complete experience on applying analytics. It was important to catalog its metadata on Data Catalog to make them visible for services like Glue and Athena.

So, the next step embraced the input of all the files of Brazilian Ecommerce dataset as tables on Data Catalog. For this task, I tested two different approaches:

1. Building and running `CREATE TABLE` queries on Athena based on file schema
2. Manually inputting fields and table properties on Data Catalog

By the way, as Athena proved itself to be a good service do start looking at cataloged data, I took the opportunity to create a workgroup with all appropriate parameters for storing query results.

And now my diagram was like:

[![Catalog process using Data Catalog and Athena](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-catalog.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-catalog.png)

## Creating IAM Roles and Policies

A huge milestone was reached at that moment. I had a storage structure, I had data to be used and I had all metadata information already cataloged on Data Catalog.

???+ question "What was missing to start creating Glue jobs?"
    IAM roles and policies. Simple as that.

At this point I must tell you that creating IAM roles wasn't an easy step to be completed. First of all, it was a little bit difficult to understand all the permissions needed for running Glue jobs on AWS, logging steps on CloudWatch and all other things.

Suddenly I found myself searching a lot on docs pages and studying about Glue's actions to be included in my policy. After a while, I was able to create a set of policies for a good IAM role to be assumed by my future and first Glue job on AWS.

And, once again, I added more pieces on my diagram:

[![IAM role and policies](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-iam.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-iam.png)

## Creating a Glue Job

Well, after all those manual setup I was finally able to create my first Glue job on AWS to create ETL pipelines using public datasets available on Data Catalog.

I was really excited at that moment and the big idea was to simulate a data pipeline that read data from a SoR layer, transform it and put the curated dataset in a SoT layer. After learning a lot about `awsglue` library and elements like `GlueContext` and `DynamicFrame`, I was able to create a Spark application using pyspark that had enough features to reach the aforementioned goal.

[![Final diagram with Glue job](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-glue.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-glue.png)

And now my diagram was complete!

![Thanos resting on the end of Infinity War movie](https://media.tenor.com/s89PZe54F4IAAAAd/renuu-thanos.gif)

___

## Not Yet: A Real Big Problem

As much as this is happy ending story, it doesn't happen just now.

???+ danger "The AWS sandbox account problem"
    Well, remember as a said at the beginning of the story that I had in my hands an AWS sandbox account? By sandbox account I mean a temporary environment that shuts down after a few hours.

    And that's was the first big problem: I needed to recreate ALL components of the final diagram every single day.

???+ danger "The huge manual effort"
    As you can imagine, I spent almost one hour setting up things every time I wanted to practice with Glue. It was a huge manual effort and that was just almost half of the sandbox life time.

    Something needed to be done.

Of course you can aske me:

???+ question "Why not to build that architecture in your personal account?"
    That was a nice option but the charges was a problem. I was just trying to learn Glue and running jobs multiple times (that's the expectation when you are learning) may incur some unpredictable costs.

Ok, so now I think everyone is trying to figure it out what I did to solve those problems.

Yes, I found a way!

If you came to here I think you would like to know it.

## Terraglue: Rising of a Project

Well, the problems were shown and I needed to think in a solution to just make my life easier for that simple learning task.

The answer was right on my face all the time. If my main problem was spending time recreating infrastructure, why not to **automate** the infrastructure creation with an IaC tool? So every time my sandbox environment shutted down, I could create all again with much less overhead.

That was a fantastic idea and I started to use [Terraform](https://www.terraform.io/) to declare resources used in my architecture. I splitted things into modules and suddenly I had enough code to create buckets, upload data, catalog things, create IAM roles, policies and a preconfigured Glue job!

While creating all this, I just felt that everyone who had the same learning challenges that made me come to this point would enjoy the project. So I prepared it, documented it and called it **terraglue**.

<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/feature/terraglue-refactor/docs/assets/imgs/logo.png?raw=true" alt="terraglue-logo" width=200 height=200>
</div>

It was really impressive on how I could deploy all the components with just a couple of commands. If I used spent about 1 hour by creating and configuring every service manually, after *terraglue* that time was reduced to just seconds!

[![Terraglue diagram with IaC modules](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/diagram-user-view.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/diagram-user-view.png)

And before finish this story, I just want to show you a little bit of the Terraform code extracted from *terraglue* project to light up the solution.

### Storage Module

The [storage module](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/storage) holds buckets declaration and object upload on S3. I made it by defining local variables on Terraform for dynamic creating bucket names regardless on the AWS target account.

```json
locals {
  account_id  = data.aws_caller_identity.current.account_id
  region_name = data.aws_region.current.name

  bucket_names_map = {
    "sor"    = "terraglue-sor-data-${local.account_id}-${local.region_name}"
    "sot"    = "terraglue-sot-data-${local.account_id}-${local.region_name}"
    "spec"   = "terraglue-spec-data-${local.account_id}-${local.region_name}"
    "athena" = "terraglue-athena-query-results-${local.account_id}-${local.region_name}"
    "glue"   = "terraglue-glue-assets-${local.account_id}-${local.region_name}"
  }
}

resource "aws_s3_bucket" "this" {
  for_each      = local.bucket_names_map
  bucket        = each.value
  force_destroy = true
}
```

### Catalog Module

The [catalog module](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/catalog) handles the step of cataloging CSV files stored on the `data/` project folder. I made it by defining a local variable that maps all data information extracted from local repo, such as database, table name, s3 location and columns.

```json
# [...] more options was defined above
glue_catalog_map = {
    for i in range(length(local.data_files)) :
    local.tbl_keys[i] => {
        "database"   = local.db_names[i]
        "table_name" = local.tbl_names[i]
        "location"   = local.s3_locations[i]
        "columns"    = local.column_names[i]
    }
}

resource "aws_glue_catalog_table" "all" {
  for_each      = var.glue_catalog_map
  database_name = each.value.database
  name          = each.value.table_name
  
  # [...] more options was defined below
```

### IAM Module

The [IAM module](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/iam) enables users for defining policies and a role to be used to set permissions for a Glue job. The things is to create JSON files inside a `policy/` folder and iterate over it to create the resources.

```json
# Defining a trust policy for AWS Glue to assume the role
data "aws_iam_policy_document" "glue_trust" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

# Creating a policy for each JSON file in policy/ folder
resource "aws_iam_policy" "glue_policies" {
  for_each = fileset(var.iam_policies_path, "**")
  name     = split(".", each.value)[0]
  policy   = file("${var.iam_policies_path}/${each.value}")
}

# Creating an IAM role with policies created
resource "aws_iam_role" "glue_role" {
  name               = var.iam_glue_role_name
  assume_role_policy = data.aws_iam_policy_document.glue_trust.json
  managed_policy_arns = [
    for p in aws_iam_policy.glue_policies : p.arn
  ]
}
```

### KMS Module

The [KMS module](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/kms) showed up just after the first *terraglue* MVP was released. I just needed to include some new features to make the job more secure and that was the trigger to create KMS keys along the project. I made it by defining a key policy and using it to define the KMS resource on Terraform.

```json
# Defining the KMS key resource
resource "aws_kms_key" "glue_cmk" {
  description              = "KMS key used for S3 data and CloudWatch logs"
  key_usage                = var.kms_key_usage
  customer_master_key_spec = var.kms_customer_master_key_spec
  is_enabled               = var.kms_is_enabled
  enable_key_rotation      = var.kms_enable_key_rotation
  policy                   = var.kms_policy
}

# Defining an alias for the key
resource "aws_kms_alias" "glue_cmk" {
  name          = "alias/kms-glue-s3"
  target_key_id = aws_kms_key.glue_cmk.key_id
}
```

### Glue Module

Finally, the [glue module](https://github.com/ThiagoPanini/terraglue/tree/main/infra/modules/glue) enables the creation of a Glue job with all best configuration practices. The steps taken for reaching this was:

1. Uploading all scripts (`.py` files) on `app/` dir to S3
2. Defining a `aws_glue_security_configuration` resource with encryption configs
3. Defining the glue job itself
4. Defining a schedules trigger for the job

```json
# Uploading all script files found in an app project dir
resource "aws_s3_object" "glue_app" {
  for_each = fileset(var.glue_app_src_dir, "**.py")
  bucket   = var.glue_job_bucket_name
  key      = "jobs/${var.glue_job_name}/src/${each.value}"
  source   = "${var.glue_app_src_dir}/${each.value}"
}
# [...]
# Creating a new job with all parameters needed
resource "aws_glue_job" "this" {
  name              = var.glue_job_name
  role_arn          = var.glue_job_role_arn
  description       = var.glue_job_description
  glue_version      = var.glue_job_version
  max_retries       = var.glue_job_max_retries
  timeout           = var.glue_job_timeout
  worker_type       = var.glue_job_worker_type
  number_of_workers = var.glue_job_number_of_workers
  # [...]
```

___

## Conclusion

If we would summarize this story in a few topics, I think the best sequence would be:

- 🤔 An Analytics Engineer wanted to learn AWS Glue and other analytics services on AWS
- 🤪 He started to build a complete infrastructure in his AWS sandbox account manually
- 🥲 Every time this AWS sandbox account was shut off, he did it all again
- 😮‍💨 He was tired of doing this all the time so he started to think on how to solve this problem
- 😉 He started to apply Terraform to declare all infrastructure
- 🤩 He created a pocket AWS environment for learning analytics and called it *terraglue*

And that's the real story about how I faced a huge problem on my learning journey and used Terraform and AWS components do take my experience to the next level.

I really hope *terraglue* proves itself useful for everyone who needs to learning more about analytics services on AWS. If you don't know where to start or even if you want a pocket environment for exploring things, maybe the *terraglue* is the best fit for you. Give it a try!