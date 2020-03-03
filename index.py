from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'roottoor'
app.config['MYSQL_DB'] = 'weblogin'
mysql = MySQL(app)


#sesion
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        data = cursor.fetchone()
        print(data)
        if not data:
            flash('Incorrect Email')
            return redirect(url_for('index'))
        elif password == data[1]:
            return redirect(url_for('home', user=data[2]), code=307)
        else:
            flash('Incorrect Password')
            return redirect(url_for('index'))


@app.route('/home/<string:user>', methods=['POST'])
def home(user):
    if request.method == 'POST':
        return render_template('home.html', user=user)
        

  
@app.route('/register', methods=['POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        data = cursor.fetchall()
        if not data:
            cursor.execute('INSERT into users (email, password, name) VALUES (%s, %s, %s)', (email, password, username))
            mysql.connection.commit()
            flash('User Registered Succesfully')
        else:
            flash('User Already Exists')
            return redirect(url_for('register_page'))
        return redirect(url_for('index'))


@app.route('/register_page')
def register_page():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)