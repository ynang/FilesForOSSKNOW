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

dag_id_variable_key_pair = {"github_init_commits_v1": "need_init_github_commits_repos",
                            "github_init_pull_requests_v1": "need_init_github_pull_requests_repos",
                            "github_init_issues_v1": "need_init_github_issues_repos",
                            "github_init_issues_timeline_v1": "need_init_github_issues_timeline_repos",
                            "github_init_issues_comments_v1": "need_init_github_issues_comments_repos",
                            "github_init_profile_v1": "need_init_github_profiles_repos"}
# todo:
# if str(valid_classes[0]) != "<class \'airflow_client.client.model.sla_miss.SLAMiss\'>":


# project_list = Variable.get("project_list", deserialize_json=True)
# print(project_list)
# Enter a context with an instance of the API client
with airflow_client.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    # api_instance = config_api.ConfigApi(api_client)

    # try:
    #     # Get current configuration
    #     api_response = api_instance.get_config()
    #     pprint(api_response)
    # except airflow_client.client.ApiException as e:
    #     print("Exception when calling ConfigApi->get_config: %s\n" % e)

    # api_instance = dag_api.DAGApi(api_client)
    # dags = api_instance.get_dags()
    # print(dags)

    # todo: distribute variables
    api_variable_api = variable_api.VariableApi(api_client)
    # variable_key = 'project_list'
    # try:
    #     variable = api_variable_api.get_variable(variable_key)
    #
    #     print(type(variable))
    #     # parse x:
    #     project_list = json.loads(variable["value"])
    #     # print(variable["value"])
    #     # value_test={"owner": "wefg", "repo": "werqtg"}
    #     # dumps = json.dumps(value_test)
    #     # variable["value"] = dumps
    #     #
    #     # api_variable_api.patch_variable(variable_key=variable_key, variable=variable)
    #     # variable = api_variable_api.get_variable(variable_key)
    #     #
    #     # print(variable["value"])
    # except airflow_client.client.ApiException as e:
    #     print("Exception when calling VariableApi->get_variable: %s\n" % e)
    # now_time = datetime.utcfromtimestamp(int(datetime.now().timestamp())).strftime(
    #     "%Y-%m-%dT%H:%M:%SZ")
    variable_keys = {"need_init_gits", "need_init_github_commits_repos", "need_init_github_pull_requests_repos",
        "need_init_github_issues_repos", "need_init_github_issues_timeline_repos",
        "need_init_github_issues_comments_repos"}
    variables = {}
    for key in variable_keys:
        variables[key] = []
    print(variables)
    # for project in project_list:
    #     owner_and_repo = project[19:].split("/")
    #     owner = owner_and_repo[0]
    #     repo = owner_and_repo[1]
    #     commits_dict = {"owner": owner, "repo": repo, "since": "1970-01-01T00:00:00Z",
    #                     "until": now_time}
    #     gits_dict = {"owner": owner, "repo": repo, "url": f"{project}.git"}
    #     github_dict = {"owner": owner, "repo": repo}
    #     for key in variables.keys():
    #         if key == "need_init_github_commits_repos":
    #             variables[key].append(commits_dict)
    #         elif key.endswith("gits"):
    #             variables[key].append(gits_dict)
    #         else:
    #             variables[key].append(github_dict)
    # for variable_key in variables:
    #     print(variables[variable_key])
    #     print(type(variables[variable_key]))
    #     value = json.dumps(variables.get(variable_key))
    #
    #     variable_object = Variable(key=variable_key, value=value)
    #     print("------------------", variable_object)
    #     print("==================", variable_key)
    #     api_variable_api.patch_variable(variable_key=variable_key, variable=variable_object)
    #     variable_get = api_variable_api.get_variable(variable_key)
    #
    #     print(variable_get["value"])

    # todo: Judge task state
    api_task_instance_api = task_instance_api.TaskInstanceApi(api_client)
    # dag_id = "github_init_issues_comments_v1"
    # dag_run_id = "github_init_issues_comments_v1_run0"
    # task_id = "op_scheduler_init_github_issues_comments"
    # response = api_task_instance_api.get_task_instance(dag_id=dag_id, dag_run_id=dag_run_id, task_id=task_id)
    # print(response)
    # print(response.state)

    # instances = api_task_instance_api.get_task_instances(dag_id=dag_id, dag_run_id=dag_run_id)
    # print(instances)

    # todo: Trigger a dag
    api_dag_run_api = dag_run_api.DAGRunApi(api_client)
    # dag_ids={'github_init_commits_v1','github_init_issues_v1','github_init_pull_requests_v1'}
    # dag_run_ids=set()
    # for dag_id in dag_ids:
    #     dag_run_id = dag_id + datetime.now(timezone.utc).isoformat()
    #     dag_run_ids.append(dag_run_id)
    #     dag_run = DAGRun(
    #         dag_run_id=dag_run_id,
    #         conf={
    #     )
    #     try:
    #         # Trigger a new DAG run
    #         api_response = api_dag_run_api.post_dag_run(dag_id=dag_id, dag_run=dag_run)
    #         print(api_response)
    #         dag_ids=[]
    #         dag_run_ids=[]
    #     except airflow_client.client.ApiException as e:
    #         print("Exception when calling DAGRunApi->get_dag_run: %s\n" % e)

    # todo: Judge task state and retry the task till the task'state is success
    # Create an instance of the API class
    # dag_id = "github_init_issues_comments_v1"  # str | The DAG ID.
    # dag_run_id = "github_init_issues_comments_v1_run0"  # str | The DAG run ID.
    # dag_ids = []
    # # example passing only required values which don't have defaults set
    # failed_tasks = []
    # failed_task_urls = []
    # try:
    #     # List task instances
    #     api_response = api_task_instance_api.get_task_instances(dag_id, dag_run_id)
    #     # pprint(api_response['task_instances'])
    # except airflow_client.client.ApiException as e:
    #     print("Exception when calling TaskInstanceApi->get_task_instances: %s\n" % e)
    # task_instances = api_response['task_instances']
    # while task_instances:
    #     for task_instance in task_instances:
    #         state = str(task_instance.state)
    #         if state == 'success':
    #             task_instances.remove(task_instance)
    #         elif state == 'failed':
    #             dag_ids.append(dag_id)
    #             task_id_strs = task_instance.task_id.split('_')
    #             failed_task_url = "https://github.com/" + task_id_strs[-2] + "/" + task_id_strs[-1]
    #             failed_task_urls.append(failed_task_url)
    #             # failed_tasks.append({"owner": task_id_strs[-2], "repo": task_id_strs[-1]})
    #             task_instances.remove(task_instance)
    # print(failed_tasks)
    # print(failed_task_urls)
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
