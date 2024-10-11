import json

AIRFLOW_OUTPUT_FILE = "/airflow/xcom/return.json"


def shutdown_task(data: dict):
    """
    Write data to a JSON file.

    Parameters:
    file_name (str): The name of the JSON file to write to.
    data (dict): The data to write to the JSON file.

    Returns:
    None
    """

    file_name = AIRFLOW_OUTPUT_FILE

    with open(file_name, 'w') as file:
        json.dump(data, file)
