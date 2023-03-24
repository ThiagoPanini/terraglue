# Terraglue: A Poweful Tool for Learning Glue

## Overview

The *terraglue* project was created for helping people to improve their learning journey on AWS Glue service. It accomplishes that by enabling a pocket environment with all necessary componentes to start developing jobs, including S3 buckets, sample data on Data Catalog, IAM roles and policies, a pre configured Athena workgroup and finally an end to end Glue job example that reads, transform and catalog new data.

- Have you ever wanted to learn Glue but you stuck on a complex environment set up?
- Have you ever wanted to test an idea for an ETL in a pocket and disposable environment?
- Have you ever wanted to go the next level on developing Glue jobs?

:waning_gibbous_moon: Try *terraglue*!


<div align="center">
    <br><img src="https://github.com/ThiagoPanini/sparksnake/blob/main/docs/assets/imgs/logo.png?raw=true" alt="sparksnake-logo" width=200 height=200>
</div>

<div align="center">
    <i>sparksnake<br>
    Python Library</i>
</div>

<div align="center">  
  <br>
  <a href="https://pypi.org/project/sparksnake/">
    <img src="https://img.shields.io/pypi/v/sparksnake?color=purple" alt="Shield sparksnake PyPI version">
  </a>

  <a href="https://pypi.org/project/sparksnake/">
    <img src="https://img.shields.io/pypi/dm/sparksnake?color=purple" alt="Shield sparksnake PyPI downloads">
  </a>

  <a href="https://pypi.org/project/sparksnake/">
    <img src="https://img.shields.io/pypi/status/sparksnake?color=purple" alt="Shield sparksnake PyPI status">
  </a>
  
  <img src="https://img.shields.io/github/commit-activity/m/ThiagoPanini/sparksnake?color=purple" alt="Shield github commit activity">
  
  <img src="https://img.shields.io/github/last-commit/ThiagoPanini/sparksnake?color=purple" alt="Shield github last commit">

  <br>
  
  <img src="https://img.shields.io/github/actions/workflow/status/ThiagoPanini/sparksnake/ci-main.yml?label=ci" alt="Shield github CI workflow">

  <a href='https://sparksnake.readthedocs.io/pt/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/sparksnake/badge/?version=latest' alt='Documentation Status' />
  </a>

  <a href="https://codecov.io/gh/ThiagoPanini/sparksnake" > 
    <img src="https://codecov.io/gh/ThiagoPanini/sparksnake/branch/main/graph/badge.svg?token=zSdFO9jkD8"/> 
  </a>

</div>

___

## Features

- 🤖 Enhanced development experience of Spark Applications to be deployed as jobs in AWS services like Glue and EMR
- 🌟 Possibility to use common Spark operations for improving ETL steps using custom classes and methods
- ⚙️ No need to think too much into the hard and complex service setup (e.g. with *sparksnake* you can have all elements for a Glue Job on AWS with a single line of code)
- 👁️‍🗨️ Application observability improvement with detailed log messages in CloudWatch
- 🛠️ Exception handling already embedded in library methods


## Getting Started

The *sparksnake* latest version is already published in [PyPI](https://pypi.org/project/sparksnake/) and available free of charge for anyone interested in improving the creation of their Spark applications using AWS services such as Glue and EMR. To start your journey, simply perform your installation using the following command:

```bash
pip install sparksnake
```

??? tip "About Python virtual environments"
    In general, it's a good practice create a [virtual environment](https://docs.python.org/3/library/venv.html) before the start of every Python project. Creating a venv for each Python project allows, among other advantages, to have an isolated environment with more refined control over the dependencies used.
    
    ??? example "Creating virtual environments"
        To create a Python virtual environment, run the following code in a folder of your preference (maybe one you can use for organizing all your further virtual environments):

        ```bash
        python -m venv <venv_name>
        ```

        Where `<venv_name>` should be replaced by the name chosen for the virtual environment to be created. It is common to have virtual environment names associated with projects (ex: `project_venv`)


    ??? example "Accessing virtual environments"
        Once created, the environment needs to be explicitly accessed by the user to ensure that all subsequent actions related to installing libraries are actually performed inside of the isolated environment created.

        If the operating system used is Windows, then use the command below to access the Python virtual environment:

        ```bash
        # Accessing venvs on Windows
        <venv_path>/Scripts/activate
        ```

        In case of use of a Linux operating system (or Git Bash in Windows), the command has minor changes and is given by:

        ```bash
        # Accessing venvs on Linux
        source <venv_path>/Scripts/activate
        ```

        Where `<venv_path>` is the location reference of the newly created virtual environment. For example, if you created a virtual environment named *test_venv* name in your user directory, then `<venv_path>` can be replaced by `C:\Users\username\test_venv` on Windows or simply `~/test_venv` on Linux.
        
    
    For more information, this [excellent Real Python blog article](https://realpython.com/python-virtual-environments-a-primer/) may shed light on a number of questions involving the creation and use of Python virtual environments.
    

## Contacts

- :fontawesome-brands-github: [@ThiagoPanini](https://github.com/ThiagoPanini)
- :fontawesome-brands-linkedin: [Thiago Panini](https://www.linkedin.com/in/thiago-panini/)
- :fontawesome-brands-hashnode: [panini-tech-lab](https://panini.hashnode.dev/)
