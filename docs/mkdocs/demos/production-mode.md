# Production Mode

So, let's take a deep dive on how an user can call the terraglue module to deploy it's own Glue job in AWS.

For this task, let's suppose we want to:

1. Deploy a Glue job using a Spark application already available
2. Create and associate an IAM role to the job
3. Use an already available KMS key from the AWS account to create a Security Configuration
4. Define some custom job arguments

## Setting Up The Project

By essence, the first step to be done is to set up a Terraform project. For this task, it's important to mention that everyone is free to structure a Terraform project the best way they want. To make things as simple as possible, the Terraform project structure below considers the following:

- A `app/` folder to store the Spark application, additional python files and unit tests
- A `policy/` folder to store a JSON file that will be used to create an IAM role for the job
- A `main.tf` Terraform file to call terraglue module

Let's see it in a tree?

```bash
├───app
│   ├───src
│   │       main.py
│   │       utils.py
│   │
│   └───tests
│           test_main.py
│
├───policy
│       glue-job-policy.json
│
│   main.tf
```

???+ question "Do I need to follow this exactly project structure work with terraglue?"
    No, you don't and that's one of the coolest terraglue features. You can take any Terraform project in any structure and call terraglue without any worries.

    You will just need to pay attention to the module variables you pass during the call. To see a full list of all acceptable variables, check the [Variables](../variables/variables.md) section. The [Validations](../variables/validations.md) section is also a good page to read in order to be aware of some input variable conditions based on specific scenarios.


## Starting The Project

Once we structured the Terraform project, let's start by collecting some Terraform data sources that will be used along the project definition. This is not a required step to use terraglue, but it can be considered a good practice in any Terraform project depending on what has been declared.

???+ warning "Work in progress"
    Content will be updated here as soon as possible!