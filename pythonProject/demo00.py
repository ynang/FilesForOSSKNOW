import airflow_client.client
from pprint import pprint
from airflow_client.client.api import config_api, dag_api, dag_run_api, variable_api, task_instance_api

from dateutil.parser import parser
import time
import json
from airflow_client.client.model.variable import Variable
from airflow_client.client.model.dag_run import DAGRun
from datetime import datetime, timezone

# Configure HTTP basic authorization: Basic
configuration = airflow_client.client.Configuration(
    host="http://192.168.8.108:8080/api/v1",
    username='airflow',
    password='airflow'
)


with airflow_client.client.ApiClient(configuration) as api_client:
    dag_id = 'github_init_profile_v1'
    api_dag_run_api = dag_run_api.DAGRunApi(api_client)
    dag_run_id = dag_id + datetime.now(timezone.utc).isoformat()
    github_dict = [
        {"owner": "oss-know", "repo": "airflow-jobs"},
        {"owner": "oss-know", "repo": "github_sync"},
        {"owner": "oss-know", "repo": "dashboard"}
    ]
    variable = {"need_init_github_profiles_repos": github_dict}
    dag_run = DAGRun(
        dag_run_id=dag_run_id,
        conf=variable,
    )
    try:
        # Trigger a new DAG run
        api_response = api_dag_run_api.post_dag_run(
            dag_id=dag_id,
            dag_run=dag_run,
        )
        print(f"api_response:{api_response}")
    except airflow_client.client.ApiException as e:
        print("Exception when calling DAGRunApi->get_dag_run: %s\n" % e)
    api_variable_api = variable_api.VariableApi(api_client)
    variable = api_variable_api.get_variable("need_init_github_profiles_repos")
    print(variable)
