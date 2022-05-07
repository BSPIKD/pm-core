import os

import src.pm_core.src.services.db_manager as dbs
import src.pm_core.src.utils.helper as h
import src.pm_core.config as _conf


def get_cmd_type_by_name(cmd_name: str, db: int):
    with dbs.Connection(db) as conn:
        sql = f"select rights from config_cmds where name = ?"
        conn.cur.execute(sql, (cmd_name,))

