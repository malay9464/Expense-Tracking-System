import mysql.connector
from contextlib import contextmanager
from backend.logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        database='expense_manager'
    )

    if connection.is_connected():
        print("Connection Successful")
    else:
        print("Connection Failed")

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute('select * from expenses')
        expenses = cursor.fetchall()
        return expenses   # ✅ return instead of print


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date: {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute('select * from expenses WHERE expense_date=%s', (expense_date,))
        expenses = cursor.fetchall()
        return expenses   # ✅ return instead of print


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date: {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date=%s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date:{expense_date}, amount:{amount}, category:{category}, notes:{notes}")
    with get_db_cursor() as cursor:
        sql = "INSERT into expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)"
        values = (expense_date, amount, category, notes)
        cursor.execute(sql, values)
        cursor._connection.commit()   # keep your original way


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start:{start_date}, end:{end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total
               FROM expenses WHERE expense_date
               BETWEEN %s and %s
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


if __name__ == '__main__':
    expenses = fetch_expenses_for_date("2024-09-30")
    print(expenses)
    # delete_expenses_for_date("2024-08-25")
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)



def get_monthly_expense_totals():
    """Get total expenses for each month in the database"""
    logger.info("get_monthly_expense_totals called")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT DATE_FORMAT(expense_date, '%Y-%m') as month, 
                      SUM(amount) as total_expense
               FROM expenses 
               GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
               ORDER BY month'''
        )
        monthly_totals = [{"month": row["month"], "total": float(row["total_expense"])} for row in cursor.fetchall()]
        return monthly_totals