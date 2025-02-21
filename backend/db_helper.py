# ------- CRUD -------

import mysql.connector

from contextlib import contextmanager

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host='localhost',
        user = 'root',
        password = 'Ali123',
        database = 'expense_manager',
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()


def fetch_expense_for_date(expense_date):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date, ))
        expenses = cursor.fetchall()
        return expenses
    

def delete_expense_for_date(expense_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date, ))


def insert_expense(expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)", (expense_date, amount, category, notes))


def fetch_expense_summary(start_date, end_date):
    with get_db_cursor()as cursor:
        cursor.execute("SELECT category, SUM(amount) as total FROM expenses WHERE expense_date BETWEEN %s AND %s GROUP By category",(start_date, end_date))
        data = cursor.fetchall()
        return data



if __name__ == '__main__':
    # insert_expense("2024-10-10", 200, "Food", "Eat Biryani")
    # delete_expense_for_date("2024-10-10")
    data = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in data:
        print(record)