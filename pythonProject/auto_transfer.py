import airflow_client.client
from pprint import pprint
from airflow_client.client.api import config_api, dag_api, dag_run_api, variable_api, task_instance_api
import json
from airflow_client.client.model.variable import Variable
from airflow_client.client.model.dag_run import DAGRun
from datetime import datetime, timezone

#
# In case of the basic authentication below. Make sure:
#  - Airflow is configured with the basic_auth as backend:
#     auth_backend = airflow.api.auth.backend.basic_auth
#  - Make sure that the client has been generated with securitySchema Basic.

# Configure HTTP basic authorization: Basic
configuration = airflow_client.client.Configuration(
    host="http://192.168.8.108:8080/api/v1",
    username='airflow',
    password='airflow'
)
with airflow_client.client.ApiClient(configuration) as api_client:
    # todo: distribute variables
    api_variable_api = variable_api.VariableApi(api_client)
    variable_key = 'project_list'
    try:
        variable = api_variable_api.get_variable(variable_key)
        project_list = json.loads(variable["value"])
    except airflow_client.client.ApiException as e:
        print("Exception when calling VariableApi->get_variable: %s\n" % e)

    variables = {"repo_list": []}

    for project in project_list:
        owner_and_repo = project[19:].split("/")
        owner = owner_and_repo[0]
        repo = owner_and_repo[1]
        github_dict = {"owner": owner, "repo": repo}
        for key in variables.keys():
            if key == 'repo_list':
                variables[key].append(github_dict)
    for variable_key in variables:
        print(variables[variable_key])
        print(type(variables[variable_key]))
        value = json.dumps(variables.get(variable_key))
        variable_object = Variable(key=variable_key, value=value)
        print("------------------", variable_object)
        print("==================", variable_key)
        api_variable_api.patch_variable(variable_key=variable_key, variable=variable_object)
        variable_get = api_variable_api.get_variable(variable_key)
        print(variable_get["value"])

    # todo: Trigger a dag
    dag_id = 'init_ck_transfer_data_by_repo'
    api_dag_run_api = dag_run_api.DAGRunApi(api_client)
    dag_run_id = dag_id + datetime.now(timezone.utc).isoformat()
    dag_run = DAGRun(
        dag_run_id=dag_run_id,
        conf={},
    )
    try:
        # Trigger a new DAG run
        api_response = api_dag_run_api.post_dag_run(dag_id=dag_id, dag_run=dag_run)
        print(api_response)
    except airflow_client.client.ApiException as e:
        print("Exception when calling DAGRunApi->get_dag_run: %s\n" % e)
