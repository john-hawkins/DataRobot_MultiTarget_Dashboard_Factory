#!/bin/bash

# #########################################################################
#  MULTI-TARGET DASHBOARD FACTORY
#   THIS SCRIPT WILL BUILD AN APPLICATION THAT DISPLAYS MULTIPLE PREDICTED
#   TARGETS FOR A RECORD. IT WILL RUN THE REQUIRED NUMBER OF DATAROBOT
#   PROJECTS AS A BACKEND AND STICH THEM TOGETHER IN A FLASK APP DASHBOARD
#   INSIDE A DOCKER CONTAINER.
# 
#   WE NEED AT LEAST 6 PARAMETERS
# #########################################################################
if [ $# -ne 5 ]; then
    echo $0: "usage: RUN.sh <PROJECT_NAME> <DATASET> <TARGET_COLS> <DR_MODE> <CONFIG_FILE> "
    echo "PROJECT_NAME: Unique name for the project. Will be used as a prefix for DataRobot Projects and the local directory."
    echo "              NOTE: Cannot contain spaces or punctuation. Letters and Underscores only."
    echo "DATASET:      Path to the dataset containing all features and target columns"
    echo "TARGET_COLS:  A comma separated list of the target column names"
    echo "              NOTE: These will be placed on the dashboard in the order they are listed."
    echo "DR_MODE:      How to run DataRobot."
    echo "              Options: AUTO, QUICK, GRPD:<GROUP_COL>, OTV:<DT_COL>:<GAP_DURATION>"
    echo "CONFIG_FILE   This is a YAML config file that tells us the account to use to build and deploy the models."
    echo "              It will need to contain:"
    echo "      API_TOKEN: Your DataRobot API TOKEN "
    echo "      USERNAME: Your DataRobot username" 
    echo "      DR_KEY: Your DataRobot API Key (OPTIONAL) - Not needed for on-premise installations. " 
    echo ""
    echo ""
    echo ""
    exit 1
fi

project=$1
dataset=$2
target_cols=$3
dr_mode=$4
config=$5

# #############################################################################################
# SET UP THE PROJECT DIRECTORY AND RUN THE MODEL FACTORY
#
mkdir $project

python multi_target_model_factory.py $project $dataset $target_cols $dr_mode $config 

# NOW COPY IN THE REQUIRED FILES 
cp app.py $project
cp Dockerfile $project
cp requirements.txt $project

# AND SET UP THE CONFIG 
#cd $project
#echo "API_TOKEN: $token" > api_config.yml
#echo "USERNAME: $username" >> api_config.yml
#echo "DR_KEY: $apikey" >> api_config.yml

cp $config "$project/api_config.yaml"

#dockerimage=$(echo "$project" | awk '{print tolower($0)}')

# BUILD THE DOCKER IMAGE
#docker build -t $dockerimage .

# RUN IT
#docker run -d -p 5000:5000 $dockerimage

