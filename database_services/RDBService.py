import pymysql
import json
import logging
from datetime import datetime
import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_db_connection():
    db_connect_info = context.get_db_info()

    logger.info("RDBService._get_db_connection:")
    logger.info("\t HOST = " + db_connect_info['host'])

    db_info = context.get_db_info()
    db_connection = pymysql.connect(
        **db_info
    )
    return db_connection


def get_by_prefix(db_schema, table_name, column_name, value_prefix):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
          column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


# returns no where clause if template empty (as is default from application.py)
def _get_where_clause_args(template):
    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k, v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " where " + " AND ".join(terms)

    return clause, args


def find_by_template(db_schema, table_name, template, field_list):
    wc, args = _get_where_clause_args(template)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    res = cur.execute(sql, args=args)
    res = cur.fetchall()

    conn.close()

    return res


def get_insertion_args(db_schema, table_name, id_name, template):
    max_id = get_next_id(db_schema, table_name, id_name)
    template = dict(template)
    template['userID'] = max_id
    cols = []
    vals = []
    if template is None or template == {}:
        return None, None
    else:
        for k, v in template.items():
            if isinstance(v, str):
                vals.append("'%s'" % (v))
            else:
                vals.append("%s" % (v))
            cols.append(k)
    cols_clause = '(' + ",".join(cols) + ')'
    vals_clause = '(' + ",".join(vals) + ')'
    return cols_clause, vals_clause, cols, vals

# create a new row
def insert_by_template(db_schema, table_name, id_name, template):
    cols_clause, vals_clause, cols, vals = get_insertion_args(db_schema, table_name, id_name, template)
    if cols_clause is not None:
        conn = _get_db_connection()
        cur = conn.cursor()

        sql = "INSERT INTO " + db_schema + "." + table_name + \
              " " + cols_clause + " VALUES " + vals_clause
        print(sql)
        res = cur.execute(sql)
        res = cur.fetchall()
        conn.commit()
        conn.close()
    return dict(zip(cols, vals))


def delete_by_id(db_schema, table_name, id_name, id_no):

    sql = "delete from " + db_schema + "." + table_name + " where " + id_name + "=" + id_no
    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    res = cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()

    return res


def get_by_id(db_schema, table_name, id_name, id_no):

    sql = "select * from " + db_schema + "." + table_name + " where " + id_name + "=" + id_no
    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    res = cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()

    return res

def get_next_id(db_schema, table_name, id_name):
    sql = f"select * from {db_schema}.{table_name} order by {id_name} desc limit 1"
    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    res = cur.execute(sql)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    max_id = res[id_name]
    return max_id + 1

def update_by_id(db_schema, table_name, template, id_name, id_no):

    conn = _get_db_connection()
    cur = conn.cursor()
    sql = f"UPDATE {db_schema}.{table_name} SET "
    for k, v in template.items():
        if isinstance(v, str):
            sql += f"{k} = \"{v}\","
        else:
            sql += f"{k} = {v},"
    sql = sql[:-1]
    sql += f" WHERE {id_name} = {id_no}"

    print(sql)
    res = cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res
