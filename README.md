# Tarot Card Project

This is the readme for our Tarot Card Project. This project is written in Python (flask) and React. For installation check the instructions mentioned below:

## Requirements

Make sure you have python and npm installed. If you do not have this stuff downloaded and installed, I would just google how to install python as well as npm. If you are downloading python and would like an IDE suggestion, I would recommend using Pycharm. 

## Installing all dependencies

Since the project is broken down into two halves I will explain how to get all needed packages for each half seperately. For your frontend, you should navigate to /frontend/ and then run the following command: 
````
npm install
````
This command should install all of the packages used for our frontend. All required packages should be written in the package.json file.

As for the python side, you can individually install all of the files used a 
````
pip install <package>
````
command or use your IDE to handle your packages. 

## Getting a local instance running

If you have a copy of the database, you can skip to further below in the instructions. If not, follow these steps:
Run the python script called **database.py**. This should generate a sqlite database. This is currently being used to deal with login stuff. 

Now, you should be ready to run your servers. Notice that the backend and frontend are not directly related, so you do have to run both instances seperately. I would suggest you do the following:

  1. Run the python file called **apiExample.py**
  2. Take note of the port this application is running on. For example, a sample output of running this file looks like:
 ````
  Running on http://127.0.0.1:5002
  Running on http://192.168.86.121:5002
 ````
  3. Go to the file ```/frontend/src/service/localhostSettings.js```
  4. Change the ```getBackendIP()``` and ```getPort()``` function as necessary to match your backend url and port.
  5. Navigate to ```/frontend/``` in a terminal window and run the command
````
npm start
````
This should start up the application and it should function properly. Make sure to add to your .gitignore file when you add some local change that you do not wish to push.



