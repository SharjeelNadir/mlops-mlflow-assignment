import mlflow
from src.pipeline_components import *

if __name__ == "__main__":
    mlflow.set_experiment("mlops_assignment_pipeline")

    with mlflow.start_run(run_name="full_pipeline"):

        extracted = step_data_extraction()
        train_path, test_path = step_data_preprocessing(extracted)
        model_path = step_model_training(train_path)
        metrics_path = step_model_evaluation(model_path, test_path)

        print("Pipeline completed successfully!")
