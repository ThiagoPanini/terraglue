# Project Story

For everyone reading this page, I ask a poetic licence to tell you a story about the challenges I faced on my analytics learning journey using AWS Glue and what I've done to overcome them.

🪄 This is a story of launching *terraglue* for improve everyone's experience on learning AWS Glue.

![Snoopy reading a book](https://i.giphy.com/media/9X6OGGZ2SNyQ8/giphy.webp)

## How it All Started

First of all, It's important to provide some context on how it all started. I'm an Analytics Engineer working for a financial company who have a lot of data and a number even higher of oportunities on using those data. The company adopted the Data Mesh architecture for giving more autonomy to the data teams for building and sharing their own data through three different layers: SoR (System of Record), SoT (Source of Truth) and Spec (Specialized).

???+ info "Know more about SoR, SoT and Spec"
    There are a lot of arcticles explaining on Data Mesh architecture and the differences between layers SoR, SoT and Spec for storing and sharing data. In fact, this is a really useful way to improve analytics on organizations.

    If you want to know a little bit more about it, there are some links that can help you on this mission:

    - 🔗 [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html)
    - 🔗 [Building a System of Record vs. a Source of Truth](https://www.integrify.com/blog/posts/system-of-record-vs-source-of-truth/)
    - 🔗 [The Difference Between System of Record and Source of Truth](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/)

So, the company decided to mainly use AWS services for all this journey. For an analytics perspective, services like Glue, EMR, Athena and Quicksight just popped up as really good options to solve some real problems in the company.

And that's how the story begins: an Analytics Engineer trying his best to deep dive into those services in his personal environment for learning everything he can.

## First Steps

Well, after deciding to start it all on learning more about AWS Glue for developing ETL jobs, I searched for documentation pages, watched some videos for prepearing myself and talked with other developers to collect thoughts and experiences about the whole thing.

After a little while, I found myself ready to start building something useful. In my hands, I had an AWS sandbox account and a noble desire to learn.

![Michael B. Jordan on Creed movie](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzBhZjAxNjY0ODUzMmVhYzI4MmJlM2IxYjQ4NzRjMzU2ZGIzNzQyYiZjdD1n/WldnJerxYdPC8/giphy.gif)

## Creating the Storage Layers

The hands on started by creating S3 buckets to replicate something next to a Data Lake storage architecture in a Data Mesh approach. So, one day I just logged in my AWS sandbox account and create the following buckets:

- A bucket for storing SoR data
- A bucket for storing SoT data
- A bucket for storing Spec data
- A bucket for storing Glue assets
- A bucket for storing Athena query results

[![Storage resources](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-storage.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-storage.png)

???+ tip "That was just the beginning and a lot of things needed to be done"
    The image above shows the start of the journey. I will use the same image and approach to add pieces and componentes as long as they show up on story.

    Let's keep going!

## Uploading Files on Buckets

Once the storage structures was created, I started to search for public datasets do be part of my learning path. The idea was to upload some data into the buckets to open de possibility of doing some analytics, like creating ETL jobs or even querying it with Athena.

So, I found the excellent [Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) on Kaggle and it fitted perfectly. I was now able to download the data and upload it on the SoR bucket to simulate some raw data that was available for further analysis in an ETL pipeline.

And now my diagram was like:

[![Storage resources with data](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-data.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-data.png)

## Cataloging Data

Upload data on S3 buckets wasn't enough to have a complete experience on applying analytics. It was important to catalog its metadata on Data Catalog to make them visible on services like Glue and Athena.

So, the next step made embraced the input of Brazilian Ecommerce dataset (which was made for a bunch of different files/tables) on Data Catalog. For this task, I tested two different approaches:

1. Building and running `CREATE TABLE` queries on Athena based on file schema
2. Manually inputting fields and table properties on Data Catalog

By the way, as Athena proved to be a good service do start looking at catalogged data, I took the oportunity to create a workgroup will all appropriate sets for storing the query results.

And now my diagram was like:

[![Catalog process using Data Catalog and Athena](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-catalog.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-catalog.png)

## Craeting IAM Roles and Policies

A huge milestone was reached at that moment. I had a storage structured, I had data to be used and I had all needed metadata information already catalogged on Data Catalog.

???+ question "What was missing to start creating Glue jobs?"
    IAM roles and policies. Simple as that.

Here I must tell you that that wasn't an easy step to be completed. First of all, it was a little bit difficult to understand all the permission actions needed for running Glue jobs on AWS, logging steps on CloudWatch and all other things.

But nothing as a good study and research couldn't solve. And that was the case: I started looking at docs and I was finally able to create a set of policies for a good IAM role to be assumed by my future and first Glue job on AWS.

And, once again, I could add more pieces on my diagram:

[![IAM role and policies](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-iam.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-iam.png)

## Creating a Glue Job

Well, after all those manual setup I was finally able to create my first Glue job on AWS to create ETL pipelines using public datasets available on S3 and on Data Catalog.

I was really excited at that moment and the big idea was to simulate a data pipeline that read data from a SoR layer, transform it and put the curated dataset in a SoT layer. After learning a lot about `awsglue` library and elements like `GlueContext` and `DynamicFrame`, I was able to create a Spark application using pyspark that had enough features to reach the aforementioned goal.

[![Final diagram with Glue job](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/project-story/terraglue-diagram-resources-glue.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/terraglue-diagram-resources-glue.png)

And now my diagram was complete!

![Thanos resting on the end of Infinity War movie](https://media.tenor.com/s89PZe54F4IAAAAd/renuu-thanos.gif)