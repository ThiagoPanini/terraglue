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