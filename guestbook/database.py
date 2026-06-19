import sqlite3
from datetime import date

DATABASE = 'guestbook.db'

def get_db_connection():
    """Устанавливает соединение с базой данных"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени (например, row['name'])
    return conn

def init_db():
    """Создаёт таблицу messages, если её ещё нет"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_all_messages():
    """Возвращает все сообщения из таблицы, отсортированные от новых к старым"""
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
    conn.close()
    return messages

def add_message(name, message):
    """
    Добавляет новое сообщение в базу данных.
    Дата создания проставляется автоматически (текущая дата).
    """
    # Получаем соединение с базой данных
    conn = get_db_connection()
    
    # Выполняем SQL-запрос на вставку данных
    # INSERT INTO - добавляет новую строку в таблицу
    # VALUES (?, ?, ?) - знаки вопроса это заполнители (placeholders)
    # Вторым аргументом передаётся кортеж со значениями
    # Знаки вопроса защищают от SQL-инъекций
    conn.execute(
        'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
        (name, message, date.today().strftime('%Y-%m-%d'))
    )
    
    # Сохраняем изменения
    conn.commit()
    
    # Закрываем соединение
    conn.close()

def delete_message(message_id):
    "Удаляет сообщение из базы данных по его id."
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()

def get_message_count():
    """Возвращает общее количество сообщений."""
    conn = get_db_connection()
    cursor = conn.execute('SELECT COUNT(*) FROM messages')
    count = cursor.fetchone()[0]
    conn.close()
    return count