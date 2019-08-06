#!/usr/bin/python
import datarobot as dr
import numpy as np
import random
import time
import sys
import os

#################################################################################
# RUN A SERIES OF DATAROBOT AUTOML PROJECTS TO PREDICT MULTIPLE TARGETS IN A
#  DATASET. DEPLOY AND STORE THE WINNING MODEL IN A CONFIG FILE.
# PARAMETERS
# - PROJECT NAME
# - PATH TO DATASET
# - LIST OF TARGETS
# - MODE OF AUTOML EXECUTION
# - USERNAME 
# - API TOKEN 
# - API KEY (OPTIONAL)
#################################################################################
def main():
    if len(sys.argv) < 5:
        print("ERROR: MISSING ARGUMENTS")
        print_usage(sys.argv)
        exit(1)
    else:
        project_name = sys.argv[1]
        path_to_data = sys.argv[2]
        target_cols = sys.argv[3]
        dr_mode = sys.argv[4]
        config_file = sys.argv[5]
        #api_token = sys.argv[6]
        #if len(sys.argv) > 6:
        #    api_key = sys.argv[7]
        #else:
        #    api_key = ""

    run_multi_target_model_factory(project_name, path_to_data, target_cols, dr_mode, config_file)

#################################################################################
def print_usage(args):
    print("USAGE ")
    print(args[0], "<PROJECT_NAME> <DATASET> <TARGET_COLS> <DR_MODE> <DR_USERNAME> <DR_CONFIG_FILE>" )


#################################################################################
# CREATE RESULTS DIRECTORY IF NEEDED
#################################################################################
def ensure_results_dir(results_dir):
    print("Testing for directory: ", results_dir)
    directory = os.path.abspath(results_dir)
    print(directory)
    if not os.path.exists(directory):
        print("Directory does not exist... creating")
        os.makedirs(directory)

########################################################################################
# FILE WRITING UTILITIES
########################################################################################
def start_results_file(results_dir):
    results_file_path = results_dir + "/model_list.tsv"
    results_file = open(results_file_path, 'w')
    results_file.write("Target" + "\t" + "ProjectID" + "\t" + "ModelID" + "\t" + "DeploymentID" + "\t" + "Metric" + "\t" + "HoldoutScore" +"\r\n")
    return results_file

def write_model_results( results_file, target, project_id, model_id, deployment_id, metric, holdout_score ):
    results_file.write(target + "\t" + project_id + "\t" + model_id + "\t" + deployment_id + "\t" + metric + "\t" + str(holdout_score) +"\r\n")
    results_file.flush()

def close_results(results_file):
    results_file.close()


#################################################################################
# TRAIN THE MODELS
#################################################################################

def run_multi_target_model_factory(project_name, path_to_data, target_cols, dr_mode, config_file) : 
    ensure_results_dir(project_name)

    results_file = start_results_file(project_name)

    target_list = target_cols.split(',')
    mode_config = dr_mode.split(':')
    # TODO: Need to force DR Login with supplied credentials

    for targ in target_list :
        temp_name = project_name + "_" + targ
        project = dr.Project.create(sourcedata=path_to_data, project_name=temp_name)
        if( mode_config[0]=='OTV' ) :

            if( len(mode_config)>2 ):
                partition = dr.DatetimePartitioningSpecification( datetime_partition_column = mode_config[1], gap_duration = mode_config[2])
            else :
                partition = dr.DatetimePartitioningSpecification( datetime_partition_column = mode_config[1] )
            project.set_target( target = targ, partitioning_method = partition )
            project.set_worker_count(20)
            project.wait_for_autopilot()

        elif( mode_config[0]=='GRPD' ) :
 
            partition = dr.GroupCV( holdout_pct = 10, reps = 5, partition_key_cols = [mode_config[1]] )
            project.set_target( target = targ, partitioning_method = partition )
            project.set_worker_count(20)
            project.wait_for_autopilot()

        elif( mode_config[0]=='QUICK' ) :
            project.set_target( target = targ, mode = 'Quick' )
            project.set_worker_count(20)
            project.wait_for_autopilot()
        else :
            project.set_target( target = targ )
            project.set_worker_count(20)
            project.wait_for_autopilot()

        # ONCE THE PROJECT COMPLETES WE NEED TO CHOOSE THE MODEL, DEPLOY IT AND STORE THE RESULTS
        project.unlock_holdout()
        metric = project.metric
        model = dr.models.ModelRecommendation.get( project.id ).get_model()
        # THE OLD WAY JUST TOOK THE MODEL AT THE TOP OF THE LEADERBOARD LIST
        #model = project.get_models()[0]
        holdout_score =  model.metrics[ project.metric ]['holdout']
        prediction_server = dr.PredictionServer.list()[0]
        deployment_title = project_name + " - " + targ
        deployment = dr.Deployment.create_from_learning_model( 
            model.id, 
            label=deployment_title, 
            description='Dashboard Factory Model for '+targ,
            default_prediction_server_id=prediction_server.id
        )

        write_model_results( results_file, targ, project.id, model.id, deployment.id, metric, holdout_score )

    close_results(results_file)

    #print("BASE MODE: ",   mode_config[0])
    #print("BASE TARGET: ", target_list[0])
    print("\nrun_multi_target_model_factory Completed")

if __name__ == "__main__": main()

