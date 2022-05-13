import airflow_client.client
from pprint import pprint
from airflow_client.client.api import config_api, dag_api, dag_run_api, variable_api, task_instance_api

from dateutil.parser import parser
import time
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
    # todo: Judge task state
    api_task_instance_api = task_instance_api.TaskInstanceApi(api_client)
    dag_id = "init_ck_transfer_data_by_repo"  # str | The DAG ID.
    dag_run_id = "manual__2022-04-29T11:58:31.533524+00:00"  # str | The DAG run ID.
    dag_ids = []
    # example passing only required values which don't have defaults set
    failed_tasks = []
    failed_task_urls = []
    failed_task_ids = []
    try:
        # List task instances
        api_response = api_task_instance_api.get_task_instances(dag_id, dag_run_id)
        # pprint(api_response['task_instances'])
    except airflow_client.client.ApiException as e:
        print("Exception when calling TaskInstanceApi->get_task_instances: %s\n" % e)
    task_instances = api_response['task_instances']
    print("任务的个数有：", len(task_instances))
    for task_instance in task_instances:
        state = str(task_instance.state)
        if state == 'failed':
            dag_ids.append(dag_id)
            task_id_strs = task_instance.task_id.split('_')
            failed_task_url = "https://github.com/" + task_id_strs[-2] + "/" + task_id_strs[-1]
            failed_task_urls.append(failed_task_url)
            failed_tasks.append({"owner": task_id_strs[-2], "repo": task_id_strs[-1]})
            failed_task_ids.append(task_instance.task_id)
    print(failed_tasks)
    print(failed_task_ids)
    print(failed_task_urls)
    # variable_key=dag_id_variable_key_pair[dag_id]
    # value = json.dumps(failed_tasks)
    # variable_object = Variable(key=variable_key,value = value)
    # api_variable_api.patch_variable(vatiable_key=variable_key,variable=variable_object)
    # dag_run_id = dag_id + datetime.now(timezone.utc).isoformat()
    # dag_run = DAGRun(
    #         dag_run_id=dag_run_id,
    #         conf={},
    #     )
    # api_response = api_dag_run_api.post_dag_run(dag_id=dag_id, dag_run=dag_run)

    # example passing only required values which don't have defaults set
    # and optional values
    # try:
    #     # List task instances
    #     api_response = api_task_instance_api.get_task_instances(dag_id, dag_run_id, execution_date_gte=execution_date_gte,
    #                                                    execution_date_lte=execution_date_lte,
    #                                                    start_date_gte=start_date_gte, start_date_lte=start_date_lte,
    #                                                    end_date_gte=end_date_gte, end_date_lte=end_date_lte,
    #                                                    duration_gte=duration_gte, duration_lte=duration_lte,
    #                                                    state=state, pool=pool, queue=queue, limit=limit, offset=offset)
    #     pprint(api_response)
    # except airflow_client.client.ApiException as e:
    #     print("Exception when calling TaskInstanceApi->get_task_instances: %s\n" % e)

    # dag_id = 'github_init_profile_v1'
    # api_dag_run_api = dag_run_api.DAGRunApi(api_client)
    # dag_run_id = dag_id + datetime.now(timezone.utc).isoformat()
    # github_dict = {"owner": "adg", "repo": "sadfg"}
    # variable = {"need_init_github_profiles_repos": github_dict}
    # dag_run = DAGRun(
    #     dag_run_id=dag_run_id,
    #     conf=variable,
    # )
    # try:
    #     # Trigger a new DAG run
    #     api_response = api_dag_run_api.post_dag_run(dag_id=dag_id, dag_run=dag_run)
    #     print(api_response)
    # except airflow_client.client.ApiException as e:
    #     print("Exception when calling DAGRunApi->get_dag_run: %s\n" % e)
    # api_variable_api = variable_api.VariableApi(api_client)
    # variable = api_variable_api.get_variable("need_init_github_profiles_repos")
    # print(variable)
