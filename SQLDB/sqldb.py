import json
import subprocess
import time
from typing import Any, Callable, Optional, Union
from urllib.parse import urlparse

import psycopg
from psycopg import sql


class SQL:
    def __init__(self) -> None:
        # Makes SQL connection to remote server.
        import os

        conStr = os.getenv("DATABASE_URL")
        if not conStr or conStr.startswith("sqlite"):
            # Fallback for local dev or if no DB is provided
            conStr = "postgres://postgres.ngvbvmbaeujkldkcqcgx:RbayPHbgAIQh7khk@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"

        p = urlparse(conStr)

        pg_connection_dict = {
            "dbname": p.path[1:] if p.path else "postgres",
            "user": p.username,
            "password": p.password,
            "port": p.port,
            "host": p.hostname,
            "autocommit": True,
        }

        self.connection = psycopg.connect(**pg_connection_dict)  # type: ignore

    def check_exists(self, result: Any):
        # Checks if an entity exists from an SQL Command.
        try:
            if len(result) == 0:
                return False
            else:
                return True
        except Exception:
            return False

    def load_json_file(self, filename: str):
        # Loads json file
        with open(filename) as f:
            datajson = json.load(f)
        return datajson

    def fetch(self, result: Any):
        # Callback function that fetches data after an SQL command is run self.runcommand("SELECT * FROM names WHERE name LIKE 'bill'",self.fetch)
        return result

    def json_to_sql(self, datajson: Union[dict, list]):
        # Converts JSON to SQL.
        if isinstance(datajson, list):
            columns = str(tuple(datajson[0].keys())).replace("'", "")
            values = str(tuple(tuple(data.values()) for data in datajson))[1:-1]
            return columns, values
        elif isinstance(datajson, dict):
            columns = str(tuple(datajson.keys())).replace("'", "")
            values = str(tuple(datajson.values())).replace("'", "")
            return columns, values
        else:
            print("JSON is invalid data shape.")
            return None, None

    def executeScriptsFromFile(self, filename: str):
        with open(filename, "r") as fd:
            sqlFile = fd.read()
        sqlCommands = sqlFile.split(";")
        print(sqlCommands)
        with self.connection.cursor() as cursor:
            for command in sqlCommands:
                try:
                    if command.strip() != "":
                        print(command)
                        cursor.execute(command.replace("\n", "").replace("\n", ""))
                except Exception as ex:
                    print("Command skipped: ", type(ex), ex)

    def run_command(
        self,
        sqlcommand: Optional[Union[str, sql.Composed]] = None,
        result_function: Optional[Callable] = None,
        datatuple: Optional[tuple] = None,
        filename: Optional[str] = None,
        verbose: int = 0,
    ):
        # Executes SQL Command or takes SQL file as input.
        # if verbose == 1:
        # if self.connection.is_connected():
        #    db_Info = self.connection.get_server_info()
        #    print("Connected to MySQL Server version ", db_Info)
        if sqlcommand is None and filename is None:
            print("Please input an SQL command or SQL filename.")
        else:
            if filename is not None:
                with open(filename) as f:
                    sqlcommand = f.read()

            with self.connection.cursor() as cursor:
                assert sqlcommand is not None
                cursor.execute(sqlcommand, datatuple)

                result = cursor.fetchall()

                if result_function is not None:
                    new_result = result_function(result)
                elif result_function is None:
                    new_result = None

                # self.connection.commit()
            if verbose == 1:
                print("SQL command executed.")
                return new_result
            else:
                return new_result

    def run_command_generator(
        self,
        sqlcommand: Optional[Union[str, sql.Composed]] = None,
        arraysize: int = 1000,
        datatuple: Optional[tuple] = None,
        filename: Optional[str] = None,
        verbose: int = 1,
    ):
        # Executes SQL Command or takes SQL file as input.
        # if verbose == 1:
        # if self.connection.is_connected():
        #    db_Info = self.connection.get_server_info()
        #    print("Connected to MySQL Server version ", db_Info)
        if sqlcommand is None and filename is None:
            print("Please input an SQL command or SQL filename.")
        else:
            if filename is not None:
                with open(filename) as f:
                    sqlcommand = f.read()
            try:
                with self.connection.cursor() as cursor:
                    assert sqlcommand is not None
                    cursor.execute(sqlcommand, datatuple)
                    if verbose == 1:
                        print("SQL command executed.")
                    while True:
                        results = cursor.fetchmany(arraysize)
                        if not results:
                            break
                        for result in results:
                            yield result
            except Exception as poe:
                print(f"{type(poe)} - {poe}")

    def sql_to_json(self, table, sqldata: tuple):
        # Convert SQL tuple to json
        columnsinfo = self.run_command(f"DESCRIBE {table}", self.fetch)
        columns = [col[0] for col in columnsinfo]
        # print(sqldata)
        final_json = []
        for data in sqldata:
            record = {}
            for ind in range(len(data)):
                record.update({data[ind]: columns[ind]})
            final_json.append(record)

        return {table: final_json}

    @staticmethod
    def convert_to_blob(filename: str):
        # Convert digital data to binary format
        with open(filename, "rb") as file:
            blobData = file.read()
        return blobData

    @staticmethod
    def start_docker_db(verbose=1):
        # Start the docker database
        # Run the database commands - "docker exec -it mysql mysql -p"
        # https://mothishdeenadayalan.medium.com/containerizing-a-python-app-mysql-python-docker-1ce64e444ed9
        dockercommand = 'docker run --name mysql -p 3306:3306 -v mysql_volume:/var/lib/mysql/ -d -e "MYSQL_ROOT_PASSWORD=temp123" mysql'
        process = subprocess.Popen(
            dockercommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if stderr != b"" and verbose == 1:
            print(stderr)
        elif stderr == b"" and verbose == 1:
            print(stdout)
        time.sleep(2)
        return stdout, stderr
