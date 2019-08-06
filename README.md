DataRobot Multi Target Dashboard Factory
==================================================

The goal of this project is to demonstrate how you can use DataRobot
to build a series of models on the same dataset where only the target
column changes. These models are then integrated into a single dashboard
that allows you to visualse multiple predicted quantities for a given
record.

The code will allow you to build and a large number of models 
on the same dataset, where there are multiple targets that you want to
predict. 

It will allow you to do this in an automated fashion. 

It will also build an intermediate API container that demonstrates how 
you could deploy these models in a way that gives you the scores for all
targets in a single return function. 


### Assumptions

This project assumes you have a valid DataRobot account and that you
have set up your account credentials in the drconfig.yaml file so that
you can use the API.
 
We assume that you have python installed with the DataRobot package.

We assume that your data contains multiple target columns and a set of 
feature columns you want to reuse for each model.

Each model built will have a different target but use all non-target columns 
as features.

It also currently assumes that you want to run the full autopilot and 
choose the model recommended by DataRobot.



### How to use it

The script [run_example.sh](run_example.sh) shows you how to use the BASH 
script to execute the complete model factory run.

This will build all the models for each TARGET in the list of targets 
and store the results in a file inside a directory for the project.

NOTE: THE COMPLETE DASHBOARD GENERATING FUNCTIONALITY IS INCOMPLETE
 
TODO: 

-- FINISH THE GENERATION OF THE DASHBOARD WIREFRAME
-- INTEGRATE THIS INTO A DOCKER IMAGE

Ultimately this script will do the following:

* Create the directory to store results and build the application
* Copy the dockerfile and python code inside the directory
* Create the required config files
* Execute the model factory on your dataset
  - Write the results to a model config file inside your app directory 
* Execute the docker script to build your container
* Deploy the container

You can then test the container and modify it as needed.

View the running container [127.0.0.1:5000](http://127.0.0.1:5000)

Note: Currently it uses a flask server which is not recommended for production.
You will need to wok with a production team to determine the ideal webserver for
deploying the intermediate API.


