from database.connection_fabrica import get_connection

# получаем соединение с БД в переменную через соответствующую функцию
db_conn = get_connection(my_db_name="my_db.db")
