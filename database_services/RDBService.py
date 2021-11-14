import pymysql
import logging
import middleware.context as context
# import json
# from datetime import datetime

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

    cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


# returns no where clause if template empty (as is default from application.py)
def _get_where_clause_args(template):
    terms = []
    args = []

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k, v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " where " + " AND ".join(terms)

    return clause, args


def find_by_template(db_schema, table_name, template):
    wc, args = _get_where_clause_args(template)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    cur.execute(sql, args=args)
    res = cur.fetchall()

    conn.close()

    return res


def get_insertion_args(template, id_name=None, id_no=None):
    if template is None or template == {}:
        return None, None
    else:
        cols = []
        vals = []

        if id_name is not None and id_no is not None:
            cols.append(id_name)
            if isinstance(id_no, str):
                vals.append("'%s'" % id_no)
            else:
                vals.append("%s" % id_no)

        for col, val in template.items():
            if col == id_name:
                continue
            if isinstance(val, str):
                vals.append("'%s'" % val)
            else:
                vals.append("%s" % val)
            cols.append(col)
    cols_clause = '(' + ", ".join(cols) + ')'
    vals_clause = '(' + ", ".join(vals) + ')'
    return cols_clause, vals_clause, cols, vals


# create a new row
def insert_user_by_template(db_schema, table_name, id_name, template):
    col_val_dict = template
    if id_name not in col_val_dict:
        return None

    id_no = col_val_dict[id_name]
    cols_clause, vals_clause, cols, vals = get_insertion_args(col_val_dict,
                                                              id_name,
                                                              id_no)
    if cols_clause is not None:
        conn = _get_db_connection()
        cur = conn.cursor()

        sql = "INSERT INTO " + db_schema + "." + table_name + \
              " " + cols_clause + " VALUES " + vals_clause + ";"
        print(sql)
        cur.execute(sql)
        cur.fetchall()
        conn.commit()
        conn.close()
    return dict(zip(cols, vals))


def insert_group_by_template(db_schema, table_name, id_name, template):
    next_group_id = get_next_id(db_schema, table_name, id_name)
    col_val_dict = template
    cols_clause, vals_clause, cols, vals = get_insertion_args(col_val_dict,
                                                              id_name,
                                                              next_group_id)
    if cols_clause is not None:
        conn = _get_db_connection()
        cur = conn.cursor()

        sql = "INSERT INTO " + db_schema + "." + table_name + \
              " " + cols_clause + " VALUES " + vals_clause + ";"
        print(sql)
        cur.execute(sql)
        cur.fetchall()
        conn.commit()
        conn.close()
    return dict(zip(cols, vals))


def delete_by_id(db_schema, table_name, id_name, id_no):
    sql = "DELETE FROM " + db_schema + "." + table_name + \
          " WHERE " + id_name + "="
    if isinstance(id_no, str):
        sql += f"\"{id_no}\""
    else:
        sql += str(id_no)
    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()

    return res


def get_by_id(db_schema, table_name, id_name, id_no):
    sql = "select * from " + db_schema + "." + table_name + " where " + \
          id_name + "= \"" + id_no + "\""
    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()

    return res


def get_groups(id_no):
    sql = "SELECT UsersGroups.Groups.group_id " + \
          "FROM UsersGroups.Groups " + \
          "INNER JOIN UsersGroups.BelongsTo ON " + \
          "UsersGroups.Groups.group_id=UsersGroups.BelongsTo.group_id " + \
          "WHERE username = \"" + id_no + "\""

    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()

    return res


def add_user_to_group(db_schema, table_name, group_id, username):
    sql = "INSERT INTO " + str(db_schema) + "." + str(table_name) + \
          " (group_id, username) " + \
          "VALUES (" + str(group_id) + ", \"" + str(username) + "\")"

    print(sql)
    try:
        conn = _get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        conn.commit()
        conn.close()
    except Exception:
        return None
    return res


def remove_user_from_group(db_schema, table_name, group_id, username):
    sql = "DELETE FROM " + str(db_schema) + "." + str(table_name) + " " + \
          "WHERE group_id = " + str(group_id) + " and username = \"" + \
          str(username) + "\")"

    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()

    return res


def get_users(id_no):
    sql = "SELECT UsersGroups.Users.username, UsersGroups.Users.gmail " + \
          "FROM UsersGroups.Users " + \
          "INNER JOIN UsersGroups.BelongsTo ON " + \
          "UsersGroups.Users.username=UsersGroups.BelongsTo.username " + \
          "WHERE group_id = " + id_no

    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()

    return res


def get_next_id(db_schema, table_name, id_name):
    sql = "SELECT * FROM " + str(db_schema) + "." + str(table_name) + \
          " order by " + str(id_name) + \
          " desc limit 1"
    print(sql)
    conn = _get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
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
    if isinstance(id_no, str):
        sql += f" WHERE {id_name} = \"{id_no}\""
    else:
        sql += f" WHERE {id_name} = {id_no}"

    print(sql)
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res
