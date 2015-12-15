#Sample Bluemix Python Web application

The sample is using [Flask microframework](http://flask.pocoo.org/) and is intented to test the Python support on [IBM's Bluemix](https://bluemix.net/) environment which is based on Cloud Foundry.

IBM Bluemix contains the Python buildpack from [Cloud Foundry](https://github.com/cloudfoundry/python-buildpack) and so will be auto-detected as long as a requirements.txt or a setup.py is located in the root of your application.

If you just wish to automatically deploy this sample to Bluemix then just click the 'Deploy to Bluemix' button and see this sample deployed into your space.

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/IBM-Bluemix/bluemix-python-flask-sample)

Alternatively follow the steps below to get the sample code and see how to deploy manually.

##Get this sample
From a terminal navigate to a location where you want this application code to be downloaded to and issue:
```bash
git clone https://github.com/IBM-Bluemix/bluemix-python-flask-sample
```
or download the zip file containing this sample code.

##Deploy to Bluemix manually
From a terminal login into Bluemix and set the api endpoint to the Bluemix region you wish to deploy to:
```script
cf login -a api.ng.bluemix.net
```
or for the UK region:
```script
cf login -a api.eu-gb.bluemix.net
```
The login will ask you for you `email`(username) and `password`, plus the `organisation` and `space` if there is more than one to choose from.

From the root directory of the application code execute the following to deploy the application to Bluemix. (By default the `route` (application URL) will be based on your application name so make sure your application name is unique or use the -n option on the cf push command to define your hostname)
```script
cf push <YOUR_APP_NAME> -m 128M 
```
to deploy when you don't have a requirements.txt or setup.py then use:
```script
cf push <YOUR_APP_NAME> -m 128M -b https://github.com/cloudfoundry/python-buildpack
```
to deploy with a different hostname to the app name:
```script
cf push <YOUR_APP_NAME> -m 128M -n <YOUR_HOST_NAME>
```

##View App
Once the application is deployed and started open a web browser and point to the application route defined at the end of the `cf push` command i.e. http://bluemix-python-flask-sample.eu-gb.mybluemix.net/. This will execute the code under the `/` app route defined in the `welcome.py` file. Navigate to http://bluemix-python-flask-sample.eu-gb.mybluemix.net/myapp to see the other `/myapp` route.

##Structure of application
**Procfile** - Contains the command to run when you application starts on Bluemix. It is represented in the form `web: <command>` where `<command>` in this sample case is to run the `py` command and passing in the the `welcome.py` script.

**requirements.txt** - Contains the external python packages that are required by the application. These will be downloaded from the [python package index](https://pypi.python.org/pypi/) and installed via the python package installer (pip) during the buildpack's compile stage when you execute the cf push command. In this sample case we wish to download the [Flask package](https://pypi.python.org/pypi/Flask) at version 0.10.1

**runtime.txt** - Controls which python runtime to use. In this case we want to use 2.7.9. 

**README.md** - this readme.

**welcome.py** - the python application script. This is implemented as a simple [Flask](http://flask.pocoo.org/) application. The routes are defined in the application using the @app.route() calls. This application has a / route and a /myapp route defined. The application deployed to Bluemix needs to listen to the port defined by the VCAP_APP_PORT environment variable as seen here:
```python
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
```

This is the port given to your application so that http requests can be routed to it. If the property is not defined then it falls back to port 5000 allowing you to run this sample appliction locally.