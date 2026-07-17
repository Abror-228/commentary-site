import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Секретный ключ для уведомлений
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_key_for_security')

# Секретное слово (код) для входа в админку
SECRET_ADMIN_CODE = "откройся123"

# Временные базы данных в оперативной памяти
users = []        
comments = []     

@app.route('/')
def index():
    return render_template('index.html', comments=comments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            if username in users:
                flash('Пользователь с таким именем уже существует!', 'danger')
            else:
                users.append(username)
                flash('Вы успешно зарегистрировались!', 'success')
                return redirect(url_for('index'))
                
    return render_template('register.html')

@app.route('/add_comment', methods=['POST'])
def add_comment():
    username = request.form.get('username')
    text = request.form.get('text')
    
    if username and text:
        comments.append({'username': username, 'text': text})
        flash('Комментарий добавлен!', 'success')
    return redirect(url_for('index'))

@app.route('/admin-panel', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        entered_code = request.form.get('secret_code')
        if entered_code == SECRET_ADMIN_CODE:
            return render_template('admin.html', users=users, total_users=len(users))
        else:
            flash('Неверный секретный код!', 'danger')
            return redirect(url_for('index'))
            
    return '''
        <div style="text-align:center; margin-top:100px; font-family:sans-serif;">
            <h2>Введите секретный код для входа в админку:</h2>
            <form method="POST">
                <input type="password" name="secret_code" placeholder="Код" required style="padding:10px; font-size:16px;"><br><br>
                <button type="submit" style="padding:10px 20px; font-size:16px; cursor:pointer;">Войти</button>
            </form>
            <br><a href="/">На главную</a>
        </div>
    '''

if __name__ == '__main__':
    # Эти настройки порта обязательны, чтобы хостинг смог запустить сайт в сети
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
