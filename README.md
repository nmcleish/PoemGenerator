# Poem Generator
The Poem Generator generates poems based on the emotional content of the user input by using Watson Tone Analyzer. This application features:
1. Word replacement
2. Deploy to Bluemix
3. Multi-user support
4. Poetgresql integration

## Getting Started
Before you get started, read my blog post to understand how the Poem Generator works. Follow the instructions below after coloning the repo to set up the Poem Generator.

## Prerequisites
1. A Bluemix account.
2. A Watson Tone Analyzer Service.
3. A Watson Language Understanding Service.
4. A Postgresql service.

To run locally, you will need Python 2 and pip.
To push your application to Bluemix from your local development environment you will need the Bluemix CLI and Dev Tools.

### Local Development Environment

You can install Python by following the instructions here.

You can install pip by following the instructions here.

If you do not have a Bluemix account, you can sign up here.

You will need to create a Watson Tone Analyzer service and a Watson Natural Language Understanding service.

You will also need a Postgres service. 

Copy your credentials to the .env file.

You will need to install the following packages using pip. In the command line, run these commands:

```
pip install watson-developer-cloud
```
 
```
pip install psycopg2
```

```
pip install flask
```

```
pip install dotenv
```

### Run Locally  
You should be able to run the Poem Generator locally now. From the command line, run this command:
```
python app.py
```

Deploy to Bluemix...
