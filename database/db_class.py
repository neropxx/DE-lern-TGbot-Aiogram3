import sqlite3 as sq
from bot_set.super_admin_data import SUPER_ADMIN


class Database:
    """Класс работа с БД

    метод create_table сбрасывает и создает таблицу в БД
    метод new_user_create добавляет в БД новых пользователей (админимтратора или нет)
    метод add_admin предоставляет действительным пользователям статус администратора. Возвращает текст результата действия.
    метод add_super_admin проверяет, установлен ли супер админ, если нет, то записывает СА в БД.
    метод delete_admin отнимает у действительных пользователей права администратора. Возвращает текст результата действия.
    метод __delete_process вспомогательный метод для удаления пользователя из списка администраторов
    метод is_user сообщает, является ли пользователь активным и записанным в БД
    метод is_admin сообщает, является ли пользователь администратором
    метод get_users возвращает список всех активных пользователей
    метод update_activ_date обновляет дату активности пользователя
    метод update_activ_status обновляет факт активности пользователя
    """
    NOW_ADMIN = ("Этот пользователь уже является администратором! 🤖\n"
                 "Введите другой ID либо отмените добавление администратора выполнив команду /cancel 🔴")
    NOT_ADMIN = ("Этот пользователь не является администратором! 🔴\n"
                 "Введите другой ID либо отмените добавление администратора выполнив команду /cancel 🔴")
    SUPER_ADMIN = "Этого пользователя нельзя разжаловать! 🔴"
    SUCCESS_DEL = "Задание выполнено: пользователь больше не администратор! 🟢"
    SUCCESS_ADD = "Задание выполнено: пользователь назначен администратором! 🟢"
    ALREADY_SA = "Суперадмин уже назначен!"
    NOT_USER = ("Такой пользователь не найден. Сначала он должен запустить бота! 🔴\n"
                "Введите другой ID либо отмените добавление администратора выполнив команду /cancel 🔴")

    @staticmethod
    def create_table(conn: sq.Connection) -> None:
        """
        Функция создания таблицы в БД

        :param conn: соединение с БД
        :return: None
        """
        cur = conn.cursor()
        # cur.execute("""DROP TABLE IF EXISTS users""")

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            user_id INTEGER,
                            admin INTEGER,
                            activ INTEGER,
                            last_active_date TEXT)""")
        conn.commit()

    @classmethod
    def new_user_create(cls, user_id: int, date: str, conn: sq.Connection) -> None:
        """
        Добавление нового пользователя в БД
        вызывается каждый раз при запуске бота пользователем - /start
        если такого пользователя нет в БД, он будет добавлен

        :param user_id: Telegram ID пользователя
        :param date: дата добавления пользователя
        :param conn: соединение с БД
        :return: None
        """
        cur = conn.cursor()

        if not cls.is_user(user_id=user_id, conn=conn):
            cur.execute("""INSERT INTO users VALUES(?, ?, ?, ?)""", (user_id, 0, 1, date,))

            conn.commit()

    @classmethod
    def add_admin(cls, conn: sq.Connection, date: str, user_id: int) -> str:
        """
        Функция назначения администратора в БД
        функция вызывает проверки, является ли пользователь пользователем бота, админом
        возвращает сообщение о статусе выполнения запроса

        :param conn: соединения с БД
        :param date: дата назначения админа
        :param user_id: Telegram ID пользователя
        :return: статус запроса, str
        """
        cur = conn.cursor()

        if cls.is_admin(user_id=user_id, conn=conn):
            return cls.NOW_ADMIN
        elif not cls.is_user(user_id=user_id, conn=conn):
            return cls.NOT_USER
        else:
            # добавление администратора
            cur.execute("""UPDATE users SET admin = 1, activ = 1, last_active_date = ? WHERE user_id LIKE(?)""",
                        (date, user_id,))
            conn.commit()
            return cls.SUCCESS_ADD

    @classmethod
    def add_super_admin(cls, conn: sq.Connection, date: str) -> None:
        """
        Функция добавления супер администратора в БД
        если в БД не назначен суперадмин, он будет добавлен по айди пользователя из переменной в настройках бота

        :param conn: соединение с БД
        :param date: дата добавления пользователя
        :return: None
        """
        if cls.is_user(conn=conn, user_id=SUPER_ADMIN) and cls.is_admin(conn=conn, user_id=SUPER_ADMIN):
            print(cls.ALREADY_SA)
        else:
            cur = conn.cursor()

            cur.execute("""INSERT INTO users VALUES(?, ?, ?, ?)""", (SUPER_ADMIN, 1, 1, date,))
            conn.commit()
            print("Супер админ добавлен в БД")

    @classmethod
    def delete_admin(cls, user_id: int, conn: sq.Connection) -> str:
        """
        Функция разжалования администратора
        вызывает проверки является ли пользователь пользователем бота, админситратором

        если все условия выполнены вызывается функция, выполняющая sql запрос для разжалования админа в БД

        :param user_id: Telegram ID пользователя
        :param conn: соединение с БД
        :return: ответ о состоянии выполнения команды, str
        """
        if not cls.is_user(user_id=user_id, conn=conn):
            return cls.NOT_USER
        if not cls.is_admin(user_id=user_id, conn=conn):
            return cls.NOT_ADMIN

        cls.__delete_process(conn=conn, user_id=user_id)
        return cls.SUCCESS_DEL

    @staticmethod
    def __delete_process(user_id: int, conn: sq.Connection) -> None:
        """
        Функция производит sql запрос к БД для разжалованния администратора

        :param user_id: Telegram ID пользователя
        :param conn: соединение с БД
        :return: None
        """
        cur = conn.cursor()

        cur.execute("""UPDATE users SET admin = 0 WHERE user_id LIKE(?)""", (user_id,))
        conn.commit()

    @staticmethod
    def is_user(user_id: int, conn: sq.Connection) -> bool:
        """
        Функция проверки, является ли пользователь пользователем бота

        :param user_id: Telegram ID пользователя
        :param conn: соединение с БД
        :return: bool
        """
        cur = conn.cursor()

        res = cur.execute("""SELECT activ FROM users WHERE user_id LIKE(?)""", (user_id,))
        if res.fetchone():
            return True
        else:
            return False

    @staticmethod
    def is_admin(user_id: int, conn: sq.Connection) -> bool:
        """
        Функция проверки, является ли пользователь администратором

        :param user_id: Telegram ID пользователя
        :param conn: соединение с БД
        :return: bool
        """
        cur = conn.cursor()

        res = cur.execute("""SELECT admin FROM users WHERE user_id LIKE(?)""", (user_id,)).fetchone()

        if res and res[0] == 1:
            return True
        else:
            return False

    @staticmethod
    def get_users(conn: sq.Connection, regim: str = "all") -> list[tuple[int]]:
        """
        Функция класса работы с БД
        возвращает список пользователей

        :param conn: соединение с БД
        :param regim: режим сортировки пользователей: activ - вернет только активных, all - вернет всех пользователей
        :return: list[tuple[int]] список кортежей, каждый кортеж содержит id пользователя
        """
        cur = conn.cursor()

        if regim == "activ":
            ids_list = cur.execute("""SELECT user_id FROM users WHERE activ == 1""").fetchall()
        else:
            ids_list = cur.execute("""SELECT user_id FROM users""").fetchall()

        return ids_list

    @staticmethod
    def update_activ_date(user_id: int, date: str, conn: sq.Connection) -> None:
        """
        Функция обновляет дату активности пользователя в БД

        :param user_id: Telegram ID пользователя
        :param date: дата активности пользователя
        :param conn: соединение с БД
        :return: None
        """
        cur = conn.cursor()

        cur.execute("UPDATE users SET activ = 1, last_active_date = ? WHERE user_id = ?", (date, user_id))
        conn.commit()

    @staticmethod
    def update_activ_status(user_id: int, conn: sq.Connection) -> None:
        """
        Функция обновляет статус активности пользователя в БД

        :param user_id: Telegram ID пользователя
        :param conn: соединение с БД
        :return: None
        """
        cur = conn.cursor()

        cur.execute("""UPDATE users SET activ = 0 WHERE user_id LIKE(?)""", (user_id, ))
        conn.commit()
