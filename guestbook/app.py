from flask import Flask, render_template, request, redirect
from database import (init_db, get_all_messages, add_message, delete_message, get_message_count, get_messages_sorted_newest, get_messages_sorted_oldest)

# Словарь для преобразования номера месяца в название на русском
MONTHS_RU = {
    '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
    '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
    '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
}

app = Flask(__name__)
init_db()


@app.route('/')
def index():
    """Главная страница: показывает все сообщения."""
    messages = get_all_messages()
    total_count = get_message_count()
    
    # Преобразуем формат даты для каждого сообщения
    formatted_messages = []
    for msg in messages:
        new_msg = dict(msg)
        if new_msg.get('created_at'):
            year, month, day = new_msg['created_at'].split('-')
            new_msg['created_at'] = f"{day} {MONTHS_RU.get(month, month)} {year}"
        formatted_messages.append(new_msg)

    return render_template('index.html', messages=formatted_messages, total_count=total_count)


@app.route('/add', methods=['POST'])
def add():
    """Обрабатывает отправку нового сообщения."""
    # Получаем данные из формы
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    # Проверяем, что оба поля не пустые
    if name and message:
        add_message(name, message)
    
    # Перенаправляем на главную страницу
    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    delete_message(message_id)
    return redirect('/')

@app.route('/sort/newest')
def sort_newest():
    """Сортировка: сначала новые."""
    messages = get_messages_sorted_newest()
    total_count = get_message_count()
    formatted_messages, today = format_messages(messages)
    return render_template('index.html', messages=formatted_messages,
                           total_count=total_count, today=today)


@app.route('/sort/oldest')
def sort_oldest():
    """Сортировка: сначала старые."""
    messages = get_messages_sorted_oldest()
    total_count = get_message_count()
    formatted_messages, today = format_messages(messages)
    return render_template('index.html', messages=formatted_messages,
                           total_count=total_count, today=today)

if __name__ == '__main__':
    app.run(debug=True)