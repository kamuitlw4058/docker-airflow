# Custom Dockerfile
FROM apache/airflow:1.10.11

USER root

COPY script/requirements.txt /requirements.txt
COPY script/entrypoint_wrapper.sh /entrypoint_wrapper.sh
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY src/ /home/airflow/.local/lib/python3.6/site-packages/airflow/

USER airflow
ENTRYPOINT ["/entrypoint_wrapper.sh"]
