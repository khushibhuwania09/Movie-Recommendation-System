pipeline {
    agent any

    stages {
        stage('Initialization') {
            steps {
                script {
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Build') {
            steps {
                echo 'This is the build code'
            }
        }

        stage('Test') {
            steps {
                echo 'This is the Test code. Running Unit Tests. Generating Coverage'
                script {
                    sh 'coverage run --omit="/usr/*" -m pytest tests'
                    sh "coverage report"
                }
            }
        }

        stage('Deploy Service') {
            steps {
                script {
                    // Prompt for user choice
                    def userChoice = input(
                        id: 'userChoice', 
                        message: 'Select the pipeline to run:', 
                        parameters: [
                            choice(
                                name: 'CHOICE', 
                                choices: ['data-generation-service', 'online-evaluation-service', 'prediction-service', 'train-model'], 
                                description: 'Choose your pipeline'
                            )
                        ]
                    )
                    // Set the choice as an environment variable
                    env.PIPELINE_CHOICE = userChoice

                }
            }
        }

        stage('Train Model') {
            when {
                // Run this stage only if the user chose Option1
                expression { env.PIPELINE_CHOICE == 'train-model' }
            }
            steps {
                script {
                    def deploy_path = '/home/team05/Documents/Westworld/Project/deploy'
                    echo 'Training the model'
                    sh "cp model_build/train.py ${deploy_path}/model_build/"
                    sh "cp model_build/prepare_data.py ${deploy_path}/model_build/"
                    sh "cp model_build/model.py ${deploy_path}/model_build/"
                    def trainModel = input(
                        id: 'trainModel', 
                        message: 'Do you want to re-train model:?', 
                        parameters: [
                            choice(
                                name: 'CHOICE', 
                                choices: ['Yes', 'No'], 
                                description: 'Model re-train'
                            )
                        ]
                    )
                    if (trainModel == 'Yes') {
                        sh "python3 ${deploy_path}/model_build/train.py"
                        sh "cp saved_models/updated_best_model.pkl ${deploy_path}/saved_models/"
                        sh "cp saved_models/updated_all_movies_list.pkl ${deploy_path}/saved_models/"
                        sh "cp saved_models/updated_user_movie_list.pkl ${deploy_path}/saved_models/"
                        sh "chmod 777 ${deploy_path}/saved_models/*"
                    }
                }
            }
        }

        stage('Data Generation Service Pipeline') {
            when {
                // Run this stage only if the user chose Option1
                expression { env.PIPELINE_CHOICE == 'data-generation-service' }
            }
            steps {
                script{
                    def deploy_path = '/home/team05/Documents/Westworld/Project/deploy'
                    echo "Running pipeline for Data Generation Service"
                    sh "cp data_generator/data_generator.py ${deploy_path}/data_generator/"
                    sh "cp data_generator/process_log_entries.py ${deploy_path}/data_generator/"
                    sh "cp data_validation/data_validator.py ${deploy_path}/data_validation/"
                    sh "cp scripts/data_generator.sh ${deploy_path}/scripts/"
                    sh "cp utils/file_utils.py ${deploy_path}/utils/"
                    sh "chmod 777 ${deploy_path}/data_generator/*.py"
                    sh "chmod 777 ${deploy_path}/data_validation/*.py"
                    sh "chmod 777 ${deploy_path}/server/*.py"
                    sh "chmod 777 ${deploy_path}/utils/*.py"
                    sh "chmod 777 ${deploy_path}/scripts/*.sh"
                }
            }
        }
        
        stage('Online Evaluation Service Pipeline') {
            when {
                // Run this stage only if the user chose Option2
                expression { env.PIPELINE_CHOICE == 'online-evaluation-service' }
            }
            steps {
                // Steps for Option 2
                script{
                    def deploy_path = '/home/team05/Documents/Westworld/Project/deploy'
                    echo "Running pipeline for Online Evaluation Service"
                    sh "cp evaluation/online_evaluation.py ${deploy_path}/evaluation/"
                    sh "cp utils/file_utils.py ${deploy_path}/utils/"
                    sh "cp server/evaluation_server.py ${deploy_path}/server/"
                    sh "cp server/templates/evaluation_dashboard.html ${deploy_path}/server/templates/"
                    sh "cp scripts/evaluation_service.sh ${deploy_path}/scripts/"
                    sh "chmod 777 ${deploy_path}/evaluation/*.py"
                    sh "chmod 777 ${deploy_path}/server/*.py"
                    sh "chmod 777 ${deploy_path}/utils/*.py"
                    sh "chmod 777 ${deploy_path}/scripts/*.sh"
                }
            }
        }
        
        stage('Prediction Service Pipeline') {
            when {
                expression { env.PIPELINE_CHOICE == 'prediction-service' }
            }
            steps {
                script {
                    echo "Running pipeline for Prediction Service"
                    def deploy_path = '/home/team05/Documents/Westworld/Project/deploy'
                    sh "cp saved_models/updated_best_model.pkl ${deploy_path}/saved_models/"
                    sh "cp saved_models/updated_all_movies_list.pkl ${deploy_path}/saved_models/"
                    sh "cp saved_models/updated_user_movie_list.pkl ${deploy_path}/saved_models/"
                    sh "cp scripts/prediction_service.sh ${deploy_path}/scripts/"
                    sh "cp server/templates/dashboard.html ${deploy_path}/server/templates/"
                    sh "cp server/server.py ${deploy_path}/server/"
                    sh "cp utils/file_utils.py ${deploy_path}/utils/"
                    sh "chmod 777 ${deploy_path}/saved_models/*"
                    sh "chmod 777 ${deploy_path}/server/*.py"
                    sh "chmod 777 ${deploy_path}/utils/*.py"
                    sh "chmod 777 ${deploy_path}/scripts/*.sh"
                }
            }
        }
    }
    post {
        always {
            echo "The pipeline has completed"
        }
    }
}
