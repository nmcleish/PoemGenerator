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

In the command line, run this commands:

```
pip install -r requirements.txt
```

### Run Locally  
You should be able to run the Poem Generator locally now. From the command line, run this command:
```
python app.py
```
In your browser, navigate to localhost:8080 or click [here](http://localhost:8080).

A new table will be created and lines will be imported

## Deploy to Bluemix

Choose your API endpoint
```
cf api <API-endpoint>
```

Replace the *API-endpoint* in the command with an API endpoint from the following list.

|URL                             |Region          |
|:-------------------------------|:---------------|
| https://api.ng.bluemix.net     | US South       |
| https://api.eu-de.bluemix.net  | Germany        |
| https://api.eu-gb.bluemix.net  | United Kingdom |
| https://api.au-syd.bluemix.net | Sydney         |

Login to your Bluemix account
```
cf login
```


From within the PoemGenerator directory push your app to Bluemix

```
cf push
```

This can take a minute. If there is an error in the deployment process you can use the command cf logs <Your-App-Name> --recent to troubleshoot.

Your app should fail.

Go to the app's page on Bluemix. From there, navigate to *something -> Environment Variables*

Add your environment varibles that you put in your *.env* file. Make sure they are correct. 

Go back to your application's homepage and press run.

You should be able to navigate to your application's site and see the Poem Generator.


