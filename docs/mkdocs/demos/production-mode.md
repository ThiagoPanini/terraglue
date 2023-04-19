# Production Mode

So, let's take a deep dive on how an user can call the terraglue module to deploy it's own Glue job in AWS.

## Setting Up the Project

By essence, the first step to be done is to set up a Terraform project. For this task, it's important to mention that everyone is free to structure a Terraform project the best way they want. To make things as simple as possible, the Terraform project structure below considers the following:

- A `app/` folder to store the Spark application, additional python files and unit tests
- A `policy/` folder to store a JSON file that will be used to create an IAM role for the job
- A `variables.tf` Terraform file to handle some project variables
- And finally a `main.tf` file to call terraglue module (and eventually declare other resources)

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
│   variables.tf
```

???+ question "Do I need to follow this exactly project structure to make terraglue work?"
    No, you don't and that's one of the coolest features of terraglue. You can take any Terraform project in any structure and call terraglue from it without any worries.

    You will just need to pay attention to the module variables you pass during the call.