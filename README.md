# Poem Generator
The Poem Generator generates poems based on the emotional content of the user input by using Watson Tone Analyzer. This application features:

1. Watson Tone Analyzer
2. Watson Natural Language Understanding
3. Deploy to Bluemix
4. Postgresql management

## Getting Started
Before you get started, read my blog post to understand how the Poem Generator works. Follow the instructions below after coloning the repo to set up the Poem Generator.

## Prerequisites
* [Bluemix account](https://console.ng.bluemix.net/registration/)
* [Git](https://git-scm.com/downloads)
* [Python 2](https://www.python.org/downloads/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)

In Bluemix, you will need to create a:
* Watson Tone Analyzer Service
* Watson Natural Language Understanding Service
* Postgresql Service - This can be created with Compose for Postgresql or ElephantSQL


## 1. Clone the sample application
Clone the repo and navigate to the directory where the sample app is located.
```
git clone https://github.com/nmcleish/poemgenerator
cd get-started-python
```

## 2. Copy your credentials to the .env file
In the sample app directory, locate the __env.template_ file. Rename the file to _.env_.You will need to copy the credentials from the Bluemix services you created. To find these credentials, navigate to your Bluemix Dashboard and click on a service. Navigate to **“Service credentials”** and click **“View credentials”**. 

Copy the credentials to their corresponding variables. Be sure to surround them with quotes.

### Postgres
You should be able to view your credentials on Bluemix or on a dashboard, depending on which service you created. The Postgres host is also the server. If you have a `:#####` at the end of your host/server, that is your port. Remove that from the end of your host and put the numbers for your port. If you don’t have a port, try using `5432`.

## 3. Install requirements
In the command line, run this commands:
```
pip install -r requirements.txt
```

## 4. Run Locally
You should be able to run the Poem Generator locally now. From the command line, run this command:
```
python app.py
```

On your first run, a new table will be created and lines will be imported. This might take a small moment.  In the command prompt, you should see
```
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 297-834-722
```

In your browser, you can view your app at http://localhost:8080 or click [here](http://localhost:8080).

## 5. Deploy to Bluemix
To deploy to Bluemix, it can be helpful to set up a manifest.yml file. One is provided for you. Take a moment to review it.

The manifest.yml includes basic information about your app, such as the name, how much memory to allocate for each instance and the route. Since host names must be unique, it will be created with a random work on the end. You can also change the host to  `YourChosenAppName`.

Choose your API endpoint
```
cf api <API-endpoint>
```

Replace the **API-endpoint/** in the command with an API endpoint from the following list.

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

From within the **PoemGenerator** directory push your app to Bluemix

```
cf push
```

This can take a minute. If there is an error in the deployment process you can use the command cf logs  --recent to troubleshoot.

Your .env file will not be pushed to Bluemix, which will cause your app to crash.
You should see this in the command prompt:
```
0 of 1 instances running, 1 crashed
FAILED
Error restarting application: Start unsuccessful
```

## 6. Update Environment Variables and Start Your App
On Bluemix, you will need to navigate to your Environment Variables.

**Dashboard -> Poem-Generator -> Runtime -> Environment Variables**

You will be able to add your environment variables that you put in your **.env** file. You won’t need quotes. Make sure they are correct.

Go back to your application's homepage and press run.

You should be able to navigate to your application's site and see the Poem Generator.

**For more information on how the Poem Generator works, you can read my blog post here.**
