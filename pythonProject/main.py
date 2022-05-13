import airflow_client.client
from pprint import pprint
from airflow_client.client.api import config_api
from airflow_client.client.api import dag_api
from airflow_client.client.api import task_instance_api
from airflow_client.client.model.task_instance import TaskInstance

#
# In case of the basic authentication below. Make sure:
#  - Airflow is configured with the basic_auth as backend:
#     auth_backend = airflow.api.auth.backend.basic_auth
#  - Make sure that the client has been generated with securitySchema Basic.

# Configure HTTP basic authorization: Basic
configuration = airflow_client.client.Configuration(
    host="http://localhost:8080/api/v1",
    username='airflow',
    password='airflow'
)

# Enter a context with an instance of the API client
with airflow_client.client.ApiClient(configuration) as api_client:
    try:
        api_instance = task_instance_api.TaskInstanceApi(api_client)
        dag_id = "github_init_issues_v1"  # str | The DAG ID.
        dag_run_id = "github_init_issues_v12022-04-25T03:59:45.082357+00:00"  # str | The DAG run ID.
        task_id = "do_init_github_issues_AdaptiveVC_SRVC"  # str | The task ID.

        api_response = api_instance.get_task_instance(dag_id, dag_run_id, task_id)
        pprint(api_response)
    except airflow_client.client.ApiException as e:
        print("Exception when calling ConfigApi->get_config: %s\n" % e)
