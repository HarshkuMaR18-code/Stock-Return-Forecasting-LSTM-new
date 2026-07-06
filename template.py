#import module
import os
from pathlib import Path

project_name = "src"

#list of file/folder that have to create
list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/aws_connection.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/estimator.py",
    f"{project_name}/entity/s3_estimator.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipline/__init__.py",
    f"{project_name}/pipline/training_pipeline.py",
    f"{project_name}/pipline/prediction_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    f"{project_name}/aws_storage/__init__.py",
    f"{project_name}/aws_storage/aws_storage.py",
    "config/schema.yaml",
    "config/model.yaml",
    "static/style.css",
    "templates/index.html",
    "app.py",
    "demo.py",
    "setup.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    ".github/workflows/aws.yaml",
]


def create_project_structure():
    for file in list_of_files:

        folder, filename = os.path.split(file)

        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(file):
            open(file, "w").close()
            print(f"Created: {file}")
        else:
            print(f"Already exists: {file}")


if __name__ == "__main__":
    create_project_structure()