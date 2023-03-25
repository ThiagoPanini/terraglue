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

I've got 


Well, I must tell you that everything started a little time ago when 

There ain't another way to start this story but telling you that the main challenge was learning AWS Glue for 


🪄 Once upon a time there was an Analytics Engineer who was starting his learning journey on AWS Glue.

He didn't know where to start, so he looked up for learning. He watched some some videos and read some documentation. After a little while, he finally got ready to get his hands dirty by doing something more practical on his personal environment. He had an AWS sandbox account and a noble desire to learn.

At first, the Engineer started by building some storage structures on S3 based on the Data Mesh architecture. So, to reach that goal, he created three buckets on his account, one for SoR (System of Records) data, another for SoT (Source of Truth) data and the last one for Spec (Specialized) data.

In the end, that approach was a big deal for improving his learning skills but the Engineer found out some troubles. He was using an AWS sandbox account that was ephemeral. It meant that the account was automatically shutted off after a few hours and all his progress was erased with it. Well, that didn't sound good but it wasn't a heavy rock to break, so everyday the Engineer launched a new sandbox account and created three new buckets for starting his learning.

Once the buckets were created, the Engineer uploaded public datasets to be part of his study (and that was also part of his daily manually job). But upload data on buckets, for an analytics perspective, was not enough. That's because he needed to input the metadata for the public datasets into the Data Catalog, adding even more manual effort on his daily basis tasks.