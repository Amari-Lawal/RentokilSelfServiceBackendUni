import base64
from typing import Any, List, Optional, Union

from psycopg import ProgrammingError, sql

from CaesarSQLDB.caesarsql import CaesarSQL


class CaesarCRUD:
    def __init__(self) -> None:
        self.caesarsql = CaesarSQL()

    def create_table(self, primary_key: str, fields: tuple, types: tuple, table: str):
        query = sql.SQL(
            "CREATE TABLE IF NOT EXISTS {table} ({primary} serial PRIMARY KEY, {fields})"
        ).format(
            table=sql.Identifier(table),
            primary=sql.Identifier(primary_key),
            fields=sql.SQL(", ").join(
                [
                    sql.SQL("{} {}").format(sql.Identifier(f), sql.Identifier(t))
                    for f, t in zip(fields, types)
                ]
            ),
        )
        try:
            self.caesarsql.run_command(query, self.caesarsql.fetch)
            return {"message": f"{table} table was created."}
        except ProgrammingError as pex:
            if "already exists" in str(pex):
                return {"message": f"{table} table already exists."}
            raise pex

    def base64_to_hex(self, value):
        value = value.encode()
        value = base64.decodebytes(value).hex()
        return value

    def post_data(self, fields: tuple, values: tuple, table: str):
        query = sql.SQL(
            "INSERT INTO {table} ({fields}) VALUES ({values}) RETURNING {ret}"
        ).format(
            table=sql.Identifier(table),
            fields=sql.SQL(", ").join(map(sql.Identifier, fields)),
            values=sql.SQL(", ").join(sql.Placeholder() * len(values)),
            ret=sql.Identifier(fields[0]),
        )

        result = self.caesarsql.run_command(
            query,
            self.caesarsql.fetch,
            datatuple=values,
        )
        return len(result) != 0

    def tuple_to_json(self, fields: tuple, result: Union[tuple, List[Any]]):
        if not result:
            return []
        if isinstance(result[0], tuple):
            final_result = []
            for entry in result:
                entrydict = dict(zip(fields, entry))
                final_result.append(entrydict)
            return final_result
        else:
            single_result = dict(zip(fields, result))
            return single_result

    def json_to_tuple(self, json_data: dict):
        keys = tuple(json_data.keys())
        values = tuple(json_data.values())
        return keys, values

    def get_data(
        self,
        fields: tuple,
        table: str,
        condition: Optional[str] = None,
        getamount: int = 1000,
    ):
        query_str = "SELECT {fields} FROM {table}"
        if condition:
            query_str += " WHERE {condition}"
        query_str += " LIMIT {limit}"

        query = sql.SQL(query_str).format(
            fields=sql.SQL(", ").join(map(sql.Identifier, fields)),
            table=sql.Identifier(table),
            condition=sql.SQL(condition) if condition else None,
            limit=sql.Literal(getamount),
        )

        result = self.caesarsql.run_command(query, self.caesarsql.fetch)
        if not result:
            return False
        if isinstance(result, list):
            return self.tuple_to_json(fields, result)
        return {"message": "syntax error.", "error": result}

    def hex_to_base64(self, hex_file: bytes):
        return base64.b64encode(bytes.fromhex(hex_file.hex())).decode()

    def get_large_data(
        self, fields: tuple, table: str, condition: Optional[str] = None
    ):
        query_str = "SELECT {fields} FROM {table}"
        if condition:
            query_str += " WHERE {condition}"

        query = sql.SQL(query_str).format(
            fields=sql.SQL(", ").join(map(sql.Identifier, fields)),
            table=sql.Identifier(table),
            condition=sql.SQL(condition) if condition else None,
        )
        return self.caesarsql.run_command_generator(query)

    def update_data(
        self, fieldstoupdate: tuple, values: tuple, table: str, condition: str
    ):
        set_clause = sql.SQL(", ").join(
            [sql.SQL("{} = %s").format(sql.Identifier(f)) for f in fieldstoupdate]
        )
        query = sql.SQL("UPDATE {table} SET {set} WHERE {cond} RETURNING {ret}").format(
            table=sql.Identifier(table),
            set=set_clause,
            cond=sql.SQL(condition),
            ret=sql.Identifier(fieldstoupdate[0]),
        )
        result = self.caesarsql.run_command(
            query, self.caesarsql.fetch, datatuple=values
        )
        return len(result) == 0

    def update_blob(self, fieldstoupdate: str, value: str, table: str, condition: str):
        # Note: update_blob still uses some string formatting for hex, but table/fields are safe now
        query = sql.SQL("UPDATE {table} SET {field} = {val} WHERE {cond} RETURNING {ret}").format(
            table=sql.Identifier(table),
            field=sql.Identifier(fieldstoupdate),
            val=sql.SQL("x'{}'").format(sql.SQL(self.base64_to_hex(value))),
            cond=sql.SQL(condition),
            ret=sql.Identifier(fieldstoupdate),
        )
        result = self.caesarsql.run_command(query, self.caesarsql.fetch)
        return len(result) == 0

    def delete_data(self, table: str, condition: str):
        field_name = condition.split("=")[0].strip()
        query = sql.SQL("DELETE FROM {table} WHERE {cond} RETURNING {ret}").format(
            table=sql.Identifier(table),
            cond=sql.SQL(condition),
            ret=sql.Identifier(field_name),
        )
        result = self.caesarsql.run_command(query, self.caesarsql.fetch)
        return len(result) == 0

    def check_exists(self, fields: tuple, table: str, condition: Optional[str] = None):
        query_str = "SELECT {fields} FROM {table}"
        if condition:
            query_str += " WHERE {condition}"

        query = sql.SQL(query_str).format(
            fields=sql.SQL(", ").join(map(sql.Identifier, fields)),
            table=sql.Identifier(table),
            condition=sql.SQL(condition) if condition else None,
        )
        result = self.caesarsql.run_command(query, self.caesarsql.check_exists)
        if isinstance(result, bool):
            return result
        return {
            "message": "syntax error or table doesn't exist.",
            "error": result,
        }
