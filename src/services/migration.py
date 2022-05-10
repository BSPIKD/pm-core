import os
import pm_core.src.utils.helper as _h

from pm_core.src.services.db_manager import Connection
from pm_core.src.models.base_db import BaseDb
from termcolor import cprint
from pyfiglet import figlet_format


def base_migration(migration_files, db=0, is_server: bool = False):
    # Kontrola a vytvoření databáze jestli neexistuje
    base = BaseDb(database=db)
    is_db_new = base.create_database_if_not_exist(is_server)

    with Connection(database=base.db) as conn:
        if is_db_new is True:
            # Byla vytvořena nová db, je potřeba nahrát všechny migrace
            for migration in migration_files:
                basename = os.path.basename(migration)
                # executnem všechny dotazy v migraci
                base.execute_sql_file(filename=migration)
                conn.cur.execute('insert into _migrations (`name`) values (?)', (basename,))
                cprint(f'{base.db}>> Migrace {basename} byla úspěšně nasazena!', 'green', attrs=['bold'])
        else:
            # Databáze existuje a je potřeba nahrát nové migrace
            for migration in migration_files:
                basename = os.path.basename(migration)
                sql = f"select count(*) from _migrations where name = ?"
                conn.cur.execute(sql, (basename,))
                if conn.cur.fetchone()[0] < 1:
                    base.execute_sql_file(filename=migration)
                    conn.cur.execute('insert into _migrations (`name`) values (?)', (basename,))
                    cprint(f'{base.db}> Migrace {basename} byla úspěšně nasazena!', 'green', attrs=['bold'])
                else:
                    cprint(f'<{base.db} Migrace {basename} již byla aplikována!', 'yellow')


def apply_master_migrations():
    cprint(figlet_format('CORE MASTER  MIGRATION', font='small'), 'magenta')
    base_migration(migration_files=_h.get_master_migration_files(project='core'), db=0)

    cprint(figlet_format('SANDBOX MASTER  MIGRATION', font='small'), 'magenta')
    base_migration(migration_files=_h.get_master_migration_files(project='sandbox'), db=0)


def apply_server_migrations(gid, name):
    cprint(figlet_format('CORE SERVER MIGRATION', font='small'), 'magenta')
    base_migration(migration_files=_h.get_server_migration_files(project='core'), db=gid, is_server=True)

    cprint(figlet_format('SANDBOX SERVER MIGRATION', font='small'), 'magenta')
    base_migration(migration_files=_h.get_server_migration_files(project='sandbox'), db=gid, is_server=True)

    cprint(figlet_format('Setup complete', font='standard'), 'blue')
