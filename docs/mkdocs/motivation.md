# The History of Library Creation

## Learning Challenges

Processing large volumes of data is undoubtedly a highly challenging task in the analytics context. In the middle of the high number of tools and frameworks available today, [Spark](https://spark.apache.org/) has a special highlight for delivering a huge range of possibilities in terms of developing scalable solutions.

???+ tip "Frameworks and analytics services in cloud providers"
    Today, the state-of-the-art on developing resilient and scalable applications revolves around cloud providers that are able to delivery a large range of services for all almost every need. In the analytics industry, AWS services such as [AWS Glue](https://aws.amazon.com/glue/) and [Amazon EMR](https://aws.amazon.com/emr/) are some of the most used cloud services for developing applications that handle all the Big Data challenges in the modern world. Both of them use Apache Spark as the engine for processing data and this is the starting point around the motivation behind the creation of the *sparksnake* library.

:material-alert-decagram:{ .mdx-pulse .warning } No matter how big are the facilities delivered by these and other analytical frameworks and services, there is still a learning curve that requires its users to understand some important technical details before diving into it and extracting all the potential delivered by such tools.

In some cases, the rapid need to build ETL process to obtain results goes over the understanding of fundamental theoretical concepts of the tools used. This prevents the users of having a holistic understanding of the process. After all, not everyone knows in depth terms, such as `SparkSession`, `SparkContext`, `GlueContext`, `DynamicFrame` that exist when you want to deploy a Glue job on AWS.

???+ quote "So the question are:"
    *"How to deliver an easy and low-complexity solution that can be used to develop Spark applications inside AWS services allowing users to focus much more on applying their data transformation rules and much less on the 'bureaucratic' service setup?"*


## A Mindset Change on Spark Job Development

Given the above scenario, *sparksnake* is born as an attempt to provide users a way to standardize their jobs created on services such as Glue and EMR on AWS. The library aim to achieve its goal through deliverying users a built in way to apply code best practices, a huge set of methods with the most common Spark transformations and many other advantages  that revolve around code simplification and efficiency.

To get an idea about a practical application of the *sparksnake* library proposal, imagine the following block of code commonly found in Glue jobs initiation boilerplates on AWS:

???+ example "Standard boilerplate of a Glue Job on AWS"

    ```python
    import sys
    from awsglue.transforms import *
    from awsglue.utils import getResolvedOptions
    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from awsglue.job import Job

    ## @params: [JOB_NAME]
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])

    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    ```

    ??? question "What's all this?"
        In the above code, you can view a number of different classes (`awsglue`) and objects never seen in other scenarios external to Glue.

        - What the function `getResolvedOptions` is doing?
        - What's a `GlueContext`?
        - What is this class of type `Job` that receives the `GlueContext` as a parameter?

There are so many questions in a first contact that users may be a little bit scared at the beginning.

On the other hand, power users who know every detail of these Glue classes and objects should ask themselves: *"Every time I start a Glue job on AWS I must define this initial block of code. Would it be possible to simplify it by calling a single function?"*

:star:{ .heart } And here you can see the *sparksnake* proposal materializing. For this simple example, there is a library feature that lets you get all the elements needed to run a Glue job (eg: context and session elements) with just a single line of code!

???+ example "Initializing a Glue job on AWS with sparksnake"

    ```python
    # Importing the main class
    from sparksnake.manager import SparkETLManager

    # Initializing a class object and a Glue job
    spark_manager = SparkETLManager(mode="glue", argv_list=["JOB_NAME"], data_dict={})
    spark_manager.init_job()
    ```

Easy, isn't it? This is just one of a number of features specially created to facilitate the development journey of Spark applications integrated (or not) into Glue. Be sure to browse the documentation to absorb all this sea of possibilities and improve, once and for all, the process of creating jobs!
