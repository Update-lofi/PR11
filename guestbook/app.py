from flask import Flask, render_template, request, redirect
from database import init_db, get_all_messages, add_message, delete_message

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
    
    # Преобразуем формат даты для каждого сообщения
    formatted_messages = []
    for msg in messages:
        # Создаем копию сообщения в виде обычного словаря (на случай, если msg - это sqlite3.Row)
        new_msg = dict(msg) 
        
        if new_msg.get('created_at'):
            # Разбиваем строку '2024-05-28' на части: ['2024', '05', '28']
            year, month, day = new_msg['created_at'].split('-')
            # Собираем новую строку: '28 мая 2024'
            # .get(month, month) вернет русское название, если месяц найден, иначе оставит как есть
            new_msg['created_at'] = f"{day} {MONTHS_RU.get(month, month)} {year}"
            
        formatted_messages.append(new_msg)

    return render_template('index.html', messages=formatted_messages)


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

if __name__ == '__main__':
    app.run(debug=True)