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
    try:
        conn = _get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
              column_name + " like " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return True, res

    except Exception as e:
        print(e)
        return False, None


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

    try:
        wc, args = _get_where_clause_args(template)

        conn = _get_db_connection()
        cur = conn.cursor()

        sql = "SELECT * FROM " + db_schema + "." + table_name + " " + wc
        cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return True, res

    except Exception as e:
        print(e)
        return False, None


def get_insertion_args(template, id_name=None, id_no=None):
    if template is None or template == {}:
        return None, None, None, None
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
    try:
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

        return True, dict(zip(cols, vals))

    except Exception as e:
        print(e)
        return False, None


def insert_group_by_template(db_schema, table_name, id_name, template):
    try:
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
        return True, dict(zip(cols, vals))


    except Exception as e:
        print(e)
        return False, None


def delete_by_id(db_schema, table_name, id_name, id_no):
    try:
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

        return True, res

    except Exception as e:
        print(e)
        return False, None


def get_by_id(db_schema, table_name, id_name, id_no):
    """
    This method gets all rows of a table that have the matching
    specified id_no

    :param db_schema: The database schema we are querying
    :param table_name: The name of the table in the schema
                        we are querying
    :param id_name: The column name we are using as the id
    :param id_no: The value of the id for the column

    :return The row from the table with the specified id
    """

    try:
        # Create sql statement to select all rows that match the id
        sql = "SELECT * FROM " + db_schema + "." + table_name + " WHERE " + \
              id_name + " = "
        if isinstance(id_no, str):
            sql += "\"" + str(id_no) + "\""
        else:
            sql += str(id_no)

        print(sql)

        # Create connection to database
        conn = _get_db_connection()
        cur = conn.cursor()

        # Execute sql query
        cur.execute(sql)

        # Fetch results
        res = cur.fetchall()

        # Commit and close connection
        conn.commit()
        conn.close()

        return True, res

    except Exception as e:
        print(e)
        return False, None


def get_groups(username):
    """
    This method gets all the groups that the user specified
    by the username is in
    :param username: The username of the user we want to query
    :return All groups that the user belongs to
    """
    try:
        # Create sql statement
        sql = "SELECT UsersGroups.Groups.group_id " + \
              "FROM UsersGroups.Groups " + \
              "INNER JOIN UsersGroups.BelongsTo ON " + \
              "UsersGroups.Groups.group_id=UsersGroups.BelongsTo.group_id " + \
              "WHERE username = \"" + username + "\""

        print(sql)

        # Connect to database
        conn = _get_db_connection()
        cur = conn.cursor()

        # Execute sql query and fetch results
        cur.execute(sql)
        res = cur.fetchall()

        # Commit and close connection
        conn.commit()
        conn.close()

        return True, res

    except Exception as e:
        print(e)
        return False, None


def add_user_to_group(db_schema, table_name, group_id, username):
    """
    This method adds a specified user to a specified group

    :param db_schema: The database schema we are querying
    :param table_name: The name of the table in the schema
                        we are querying
    :param group_id: The group_id of the group we are adding
                     the user to
    :param username: The username of the user we are adding
                     to the group
    """

    try:

        # Create SQL statement
        sql = "INSERT INTO " + str(db_schema) + "." + str(table_name) + \
              " (group_id, username) " + \
              "VALUES (" + str(group_id) + ", \"" + str(username) + "\")"

        print(sql)

        # Establish connection to database
        conn = _get_db_connection()
        cur = conn.cursor()

        # Execute query and fetch results
        cur.execute(sql)
        res = cur.fetchall()

        # Commit and close connection
        conn.commit()
        conn.close()

        return True, res

    except Exception as e:
        print(e)
        return False, None


def remove_user_from_group(db_schema, table_name, group_id, username):
    """
    This removes a specified user from a specified group

    :param db_schema: The database schema we are querying
    :param table_name: The name of the table in the schema
                        we are querying
    :param group_id: The group_id of the group we are removing
                     the user from
    :param username: The username of the user we are removing
                     from the group
    """

    try:

        # Create SQL statement
        sql = "DELETE FROM " + str(db_schema) + "." + str(table_name) + " " + \
              "WHERE group_id = " + str(group_id) + " and username = \"" + \
              str(username) + "\")"

        print(sql)

        # Establish connection to database
        conn = _get_db_connection()
        cur = conn.cursor()

        # Execute query and fetch results
        cur.execute(sql)
        res = cur.fetchall()

        # Commit and close connection
        conn.commit()
        conn.close()

        return True, res

    except Exception as e:
        print(e)
        return False, None


def get_users_in_group(group_id):
    """
    This method gets all the users in a specified group

    :param group_id: The group id of the group we are getting all users of
    :return The username and gmails of all users in the specified group
    """
    try:
        # Create SQL statement
        sql = "SELECT UsersGroups.Users.username, UsersGroups.Users.gmail " + \
              "FROM UsersGroups.Users " + \
              "INNER JOIN UsersGroups.BelongsTo ON " + \
              "UsersGroups.Users.username=UsersGroups.BelongsTo.username " + \
              "WHERE group_id = " + str(int(group_id))

        print(sql)

        # Establish connection to database
        conn = _get_db_connection()
        cur = conn.cursor()

        # Execute query and fetch results
        cur.execute(sql)
        res = cur.fetchall()

        # Commit and close connection
        conn.commit()
        conn.close()

        return True, res

    except Exception as e:
        print(e)
        return False, None


def get_next_id(db_schema, table_name, id_name):
    """
    This method gets the next unique id we can use to insert
    a new row into the table

    :param db_schema: The database schema we are querying
    :param table_name: The name of the table in the schema
                        we are querying
    :param id_name: The name of the column in the table we
                    are using as the id
    """

    try:
        # Create SQL statement
        sql = "SELECT * FROM " + str(db_schema) + "." + str(table_name) + \
              " order by " + str(id_name) + \
              " desc limit 1"
        print(sql)

        # Establish connection to database
        conn = _get_db_connection()
        cur = conn.cursor()

        # Execute query and fetch results
        cur.execute(sql)
        res = cur.fetchone()

        # Commit and close connection
        conn.commit()
        conn.close()

        # Get the current max id
        max_id = -1
        if id_name in res:
            max_id = res[id_name]

        # Return the next id (counter)
        return True, max_id + 1


    except Exception as e:
        print(e)
        return False, None


def update_by_id(db_schema, table_name, template, id_name, id_no):
    """
    This method gets the next unique id we can use to insert
    a new row into the table

    :param db_schema: The database schema we are querying
    :param table_name: The name of the table in the schema
                        we are querying
    :param template: The column-value pairs (dictionary) containing
                     the updated information we want to use
    :param id_name: The column name we are using as the id for the table
    :param id_no: The value of the id we use to match all rows we want to
                  update
    """

    try:
        # Create SQL statement
        sql = f"UPDATE {db_schema}.{table_name} SET "
        for k, v in template.items():
            if len(k) == 0:
                continue
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

        # Establish connection to database
        conn = _get_db_connection()
        cur = conn.cursor()

        # Execute query and fetch results
        cur.execute(sql)
        res = cur.fetchall()
        cur.execute(f'select * from {db_schema}.{table_name} where {id_name} = \'{id_no}\'')
        res = cur.fetchall()
        # Commit and close connection
        conn.commit()
        conn.close()

        # Return the results
        return True, res


    except Exception as e:
        print(e)
        return False, None
