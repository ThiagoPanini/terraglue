# Frequently Asked Questions

> :fontawesome-solid-circle-question:{ .mdx-pulse .question } *I've just found out terraglue by chance. How do I know if it can help me?*

Basically, *terraglue* has different user profiles ranging from beginners to the most experienced ones.If you want to take your first steps on AWS using Glue, here you can have a tool capable of providing an end to end journey at the touch of a command. If you are already immersed in this journey and have technical questions about Spark applications, unit tests, Python modules or Terraform, this is also your place!

___

> :fontawesome-solid-circle-question:{ .mdx-pulse .question } *Can I customize the baseline infrastructure provided by terraglue?*

Sure! You can clone the source repository, input your changes, modify or add new modules and, finally, apply it on your AWS target account. The sky is the limit!

___

> :fontawesome-solid-circle-question:{ .mdx-pulse .question } *Will I be charged for using terraglue in my AWS account?*

This is a very interesting and important question. There are no costs to use terraglue as it is an open source solution shared with the entire community. HOWEVER, it is essential to mention that the resources created by terraglue in your AWS environment may eventually incur costs. Therefore, it is critical that terraglue users understand the potential fees involved with related services before utilizing the solution.

???+ warning "How do you mean there are costs?"
    Well, *terraglue* is an IaC project that deploys some infrastructure in an AWS target account. By deploying it, users will probably be charged for:

    - S3 data storage
    - Queries executed on Athena
    - Jobs executed on Glue
    
    The final message is: ALWAYS be aware of services costs on AWS and read all the documentation you judge necessary to have a clear view of the situation BEFORE doing anything.