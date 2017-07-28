# Poem Generator
The Poem Generator generates poems based on the emotional content of the user input by using Watson Tone Analyzer. This application features:

1. Watson Tone Analyzer
2. Watson Natural Language Understanding
3. Deploy to Bluemix
4. PostgreSQL

## Getting Started
Before you get started, [read my blog post](https://medium.com/@nmcleish/xxx) to learn how the Poem Generator works. to To set up the Poem Generator follow the instructions below after cloning the repo.

## Prerequisites
* [Bluemix account](https://console.ng.bluemix.net/registration/)
* [Git](https://git-scm.com/downloads)
* [Python 2](https://www.python.org/downloads/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)

In Bluemix, you will need to create a:
* Watson Tone Analyzer Service
* Watson Natural Language Understanding Service
* Compose for PostgreSQL Service (or use another PostgreSQL service of your choice)


## 1. Clone the sample application
Clone the repo and navigate to the directory where the sample app is located.
```
git clone https://github.com/ibm-watson-data-lab/PoemGenerator
cd PoemGenerator
```

## 2. Copy your credentials to the .env file
In the sample app directory, locate the __env.template_ file. Rename the file to _.env_. You will need to copy the credentials from the Bluemix services you created. To find these credentials, navigate to your Bluemix Dashboard and click on a service. Navigate to **“Service credentials”** and click **“View credentials”**. 

Copy the credentials to their corresponding variables.

### PostgreSQL
For PostgreSQL you will need to provide the username, password, host, port and database name. The default port for PostgreSQL is 5432. If you are using Compose for PostgreSQL your connection string in the Bluemix dashboard will look something like this:

`postgres://admin:MYPASSWORD@sl-us-south-1-portal.3.dblayer.com:18887/compose`

This would map to the following properties in the .env file
```
POSTGRESQL_USERNAME=admin
POSTGRESQL_PASSWORD=MYPASSWORD
POSTGRESQL_HOST=sl-us-south-1-portal.3.dblayer.com
POSTGRESQL_DBNAME=compose
POSTGRESQL_PORT=18887
```

#### Create a Database
If you are using Compose for PostgreSQL a database called `compose` will have been created for you. If you are using another PostgreSQL provider be sure to create a database and specify the database name in the _.env_ file.

## 3. Set up a Python Virtual Environment (Optional)
If you prefer to use virtual environments configure one at this step. A virtual environment is a tool to keep the dependencies required by different projects in separate places. You can create and activate a virtual environment by running the following commands:
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

You can deactivate your virtual environment by running:
`deactivate`

## 4. Install requirements
In the command line, run this command:
```
pip install -r requirements.txt
```

## 5. Run Locally
You should be able to run the Poem Generator locally now. From the command line, run this command:
```
python app.py
```

On your first run, a new database table will be created and poem lines will be imported into the database. This might take a small moment.  In the command prompt, you should see:
```
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 297-834-722
```

In your browser, you can view your app at http://localhost:8080 or click [here](http://localhost:8080).

## 5. Deploy to Bluemix
To deploy to Bluemix, it can be helpful to set up a manifest.yml file. One is provided for you. Take a moment to review it.

The manifest.yml includes basic information about your app, such as the name, how much memory to allocate for each instance and the route. Since host names must be unique, it will be created with a random word on the end. You can also change the host to  `YourChosenAppName`.

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

This can take a minute. If there is an error in the deployment process you can use the command `cf logs  --recent` to troubleshoot.

Your .env file will not be pushed to Bluemix, and the very first time your app will crash. This is expected.
You should see this in the command prompt:
```
0 of 1 instances running, 1 crashed
FAILED
Error restarting application: Start unsuccessful
```

## 6. Update Environment Variables and Start Your App
On Bluemix, you will need to navigate to your Environment Variables.

**Dashboard -> Poem-Generator -> Runtime -> Environment Variables**

Add each environment variable that is defined in your **.env** file.

Go back to your application's homepage and press run.

You should be able to navigate to your application's site and see the Poem Generator.

**For more information on how the Poem Generator works, you can read my blog post [here](https://medium.com/@nmcleish/xxx).**
