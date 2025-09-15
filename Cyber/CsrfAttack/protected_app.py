"""
CSRF Protected Banking Application.

A Flask banking application demonstrating CSRF protection.
"""

from flask import Flask, request, render_template, session, redirect
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# User database
users = {
    'admin': {'password': 'admin', 'balance': 1000},
    'user': {'password': 'user', 'balance': 500}
}


def generate_csrf_token():
    """Generate CSRF token."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']


def validate_csrf_token():
    """Validate CSRF token."""
    token = request.form.get('csrf_token')
    return token and token == session.get('csrf_token')


@app.route('/')
def login_page():
    """Show login page."""
    return render_template('protected_login.html', csrf_token=generate_csrf_token())


@app.route('/login', methods=['POST'])
def login():
    """Handle login."""
    if not validate_csrf_token():
        return "CSRF token invalid!", 403
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users and users[username]['password'] == password:
        session['username'] = username
        return redirect('/dashboard')
    
    return render_template('protected_login.html', 
                         error='Invalid login',
                         csrf_token=generate_csrf_token())


@app.route('/dashboard')
def dashboard():
    """Show user dashboard."""
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    balance = users[username]['balance']
    message = session.pop('message', None)
    
    return render_template('protected_dashboard.html', 
                         username=username, 
                         balance=balance, 
                         message=message,
                         csrf_token=generate_csrf_token())


@app.route('/transfer', methods=['POST'])
def transfer():
    """Transfer money - PROTECTED from CSRF!"""
    if 'username' not in session:
        return redirect('/')
    
    # CSRF Protection
    if not validate_csrf_token():
        return "🛡️ CSRF Attack Blocked!", 403
    
    sender = session['username']
    recipient = request.form.get('recipient')
    amount = int(request.form.get('amount', 0))
    
    if recipient in users and users[sender]['balance'] >= amount:
        users[sender]['balance'] -= amount
        users[recipient]['balance'] += amount
        session['message'] = f'✅ Transferred ${amount} to {recipient}'
    else:
        session['message'] = '❌ Transfer failed'
    
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    print("🛡️ Running PROTECTED app on http://localhost:5001")
    print("Login: admin/admin or user/user")
    app.run(debug=True, port=5001)
