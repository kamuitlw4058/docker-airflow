# encoding: utf-8

import os

from airflow import settings
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.base_hook import CONN_ENV_PREFIX


MYSQL_CONN_ID = "dag_creation_manager_plugin_sql_alchemy_conn"


def get_mysql_hook():
    os.environ[CONN_ENV_PREFIX + MYSQL_CONN_ID.upper()] = settings.SQL_ALCHEMY_CONN
    return PostgresHook(postgres_conn_id=MYSQL_CONN_ID)


def run_sql(sql, ignore_error=False):
    hook = get_mysql_hook()
    print ("sql:\n%s" % sql)
    try:
        res = hook.get_records(sql)
    except Exception as e:
        if not ignore_error:
            raise e
        res = None
    print (res)
    return res


def run_version_0_0_1():
    run_sql("""
        CREATE TABLE dcmp_dag (
          id serial NOT NULL,
          dag_name varchar(100) NOT NULL,
          version int NOT NULL,
          category varchar(50) NOT NULL,
          editing boolean NOT NULL,
          editing_user_id int DEFAULT NULL,
          editing_user_name varchar(100) DEFAULT NULL,
          last_editor_user_id int DEFAULT NULL,
          last_editor_user_name varchar(100) DEFAULT NULL,
          updated_at timestamp NOT NULL,
          approved_version int not NULL,
          approver_user_id int not NULL,
          approver_user_name varchar(100) DEFAULT NULL,
          last_approved_at timestamp,
          editing_start timestamp,

          PRIMARY KEY (id),
          constraint dcmp_dag_dag_name_unique unique(dag_name) 
        ) ;
        CREATE INDEX dcmp_dag_category_index ON dcmp_dag   (category);
        CREATE INDEX dcmp_dag_editing_index ON dcmp_dag   (editing);
        CREATE INDEX dcmp_dag_updated_at_index ON dcmp_dag   (updated_at);
        CREATE INDEX dcmp_dag_editing_start_index ON dcmp_dag   (editing_start);
        CREATE INDEX dcmp_dag_last_edited_at_index ON dcmp_dag   (last_edited_at);
    """, ignore_error=True)

    run_sql("""
        CREATE TABLE  dcmp_dag_conf (
          id serial NOT NULL,
          dag_id int NOT NULL,
          dag_name varchar(100) NOT NULL,
          action varchar(50) NOT NULL,
          version int NOT NULL,
          conf text NOT NULL,
          creator_user_id int DEFAULT NULL,
          creator_user_name varchar(100) DEFAULT NULL,
          created_at timestamp NOT NULL,
          approver_user_id int DEFAULT NULL,
          approver_user_name varchar(100) DEFAULT NULL,
          approved_at timestamp,
          last_edited_at timestamp,
          PRIMARY KEY (id)
        ) ;
        CREATE INDEX dcmp_dag_conf_dag_id_index ON dcmp_dag_conf   (dag_id);
        CREATE INDEX dcmp_dag_conf_dag_name_index ON dcmp_dag_conf   (dag_name);
        CREATE INDEX dcmp_dag_conf_action_index ON dcmp_dag_conf   (action);
        CREATE INDEX dcmp_dag_conf_version_index ON dcmp_dag_conf   (version);
        CREATE INDEX dcmp_dag_conf_created_at_index ON dcmp_dag_conf   (created_at);
    """, ignore_error=True)


def run_version_0_0_2():
    pass
    run_sql("ALTER TABLE dcmp_dag ADD editing_start timestamp;", ignore_error=True)
    run_sql("CREATE INDEX dcmp_dag_editing_start_index ON dcmp_dag   (editing_start);", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag ADD last_edited_at timestamp;", ignore_error=True)
    run_sql("CREATE INDEX dcmp_dag_last_edited_at_index ON dcmp_dag   (last_edited_at);", ignore_error=True)


def run_version_0_1_1():
    pass


def run_version_0_2_0():
    run_sql("""
        CREATE TABLE dcmp_user_profile (
          id serial NOT NULL,
          user_id int NOT NULL,
          is_superuser bool NOT NULL,
          is_data_profiler bool NOT NULL,
          is_approver bool NOT NULL,
          updated_at timestamp NOT NULL,
          created_at timestamp NOT NULL,
          approval_notification_emails text NOT NULL,
          PRIMARY KEY (id)
        );
        CREATE INDEX dcmp_user_profile_user_id_index ON dcmp_user_profile   (user_id);
        CREATE INDEX dcmp_user_profile_is_superuser_index ON dcmp_user_profile   (is_superuser);
        CREATE INDEX dcmp_user_profile_is_data_profiler_index ON dcmp_user_profile   (is_data_profiler);
        CREATE INDEX dcmp_user_profile_is_approver_index ON dcmp_user_profile   (is_approver);
        CREATE INDEX dcmp_user_profile_updated_at_index ON dcmp_user_profile   (updated_at);
        CREATE INDEX dcmp_user_profile_created_at_index ON dcmp_user_profile   (created_at);
    """, ignore_error=True)


def run_version_0_2_1():
    pass
    run_sql("ALTER TABLE dcmp_dag ADD approved_version int(11) NOT NULL;", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag ADD INDEX approved_version (approved_version);", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag ADD approver_user_id int(11) DEFAULT NULL;", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag ADD approver_user_name varchar(100) DEFAULT NULL;", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag ADD last_approved_at timestamp;", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag ADD INDEX last_approved_at (last_approved_at);", ignore_error=True)

    run_sql("ALTER TABLE dcmp_dag_conf ADD approver_user_id int(11) DEFAULT NULL;", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag_conf ADD approver_user_name varchar(100) DEFAULT NULL;", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag_conf ADD approved_at timestamp;", ignore_error=True)
    run_sql("ALTER TABLE dcmp_dag_conf ADD INDEX approved_at (approved_at);", ignore_error=True)
    
    run_sql("ALTER TABLE dcmp_user_profile ADD approval_notification_emails text NOT NULL;", ignore_error=True)


def main():
    run_version_0_0_1()
    run_version_0_0_2()
    run_version_0_1_1()
    run_version_0_2_0()
    run_version_0_2_1()


if __name__ == "__main__":
    main()
