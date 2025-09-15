"""
CSRF Vulnerable Banking Application.

A Flask banking application demonstrating CSRF vulnerability.
"""

from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'demo_key'  # Weak secret for demo

# User database
users = {
    'admin': {'password': 'admin', 'balance': 1000},
    'user': {'password': 'user', 'balance': 500}
}


@app.route('/')
def login_page():
    """Show login page."""
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """Handle login."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['test'] = 'test'
        return redirect('/dashboard')
    
    return render_template('login.html', error='Invalid login')


@app.route('/dashboard')
def dashboard():
    """Show user dashboard."""
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    balance = users[username]['balance']
    message = session.pop('message', None)
    
    return render_template('dashboard.html', 
                         username=username, 
                         balance=balance, 
                         message=message)


@app.route('/transfer', methods=['POST'])
def transfer():
    """Transfer money - VULNERABLE TO CSRF!"""
    if 'username' not in session:
        return redirect('/')
    
    sender = session['username']
    recipient = request.form.get('recipient')
    amount = int(request.form.get('amount', 0))
    
    if recipient in users and users[sender]['balance'] >= amount:
        users[sender]['balance'] -= amount
        users[recipient]['balance'] += amount
        session['message'] = f'Transferred ${amount} to {recipient}'
    else:
        session['message'] = 'Transfer failed'
    
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    print("🚨 Running VULNERABLE app on http://localhost:5000")
    print("Login: admin/admin or user/user")
    app.run(debug=True, port=5000)
