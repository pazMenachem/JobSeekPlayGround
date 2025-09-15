# CSRF Attack Demo

A clear example demonstrating CSRF attacks and protection.

## 📁 Files

### Vulnerable Application
- `vulnerable_app.py` - Flask banking app with CSRF vulnerability
- `templates/login.html` - Login page
- `templates/dashboard.html` - Banking dashboard (vulnerable)

### Attack
- `attack.html` - Malicious page that performs CSRF attack

### Protected Application  
- `protected_app.py` - Flask banking app with CSRF protection
- `templates/protected_login.html` - Login with CSRF token
- `templates/protected_dashboard.html` - Protected dashboard

## 🚀 Quick Start

### 1. Install Flask
```bash
pip install -r requirements.txt
```

### 2. Run Vulnerable App
```bash
python vulnerable_app.py
```
→ Opens on http://localhost:5000

### 3. Run Protected App (optional)
```bash
python protected_app.py
```
→ Opens on http://localhost:5001

## 🎯 Demo Steps

### Step 1: Login to Vulnerable App
1. Go to http://localhost:5000
2. Login: `admin` / `admin` 
3. Note balance: $1000

### Step 2: Execute CSRF Attack
1. Open `attack.html` in browser
2. Click "Claim Prize!" button
3. Return to banking app
4. See $100 was stolen! 💸

### Step 3: Try Protected App
1. Go to http://localhost:5001  
2. Login: `admin` / `admin`
3. Open `attack.html` again
4. Attack fails! 🛡️

## 🔍 How It Works

### Vulnerable Code
```python
@app.route('/transfer', methods=['POST'])
def transfer():
    # NO CSRF PROTECTION!
    recipient = request.form.get('recipient')
    amount = int(request.form.get('amount', 0))
    # Transfer happens...
```

### Attack Code
```html
<!-- Hidden form submits to vulnerable app -->
<form method="POST" action="http://localhost:5000/transfer">
    <input type="hidden" name="recipient" value="user">
    <input type="hidden" name="amount" value="100">
</form>
```

### Protection Code
```python
@app.route('/transfer', methods=['POST'])
def transfer():
    # CSRF PROTECTION!
    if not validate_csrf_token():
        return "CSRF Attack Blocked!", 403
    # Safe transfer...
```

## 🛡️ Key Lessons

- **Vulnerable**: Forms without CSRF tokens can be exploited
- **Protected**: CSRF tokens prevent unauthorized requests
- **Implementation**: Basic protection is easy to implement

## ⚠️ Educational Only

This demo is for learning purposes. Never deploy vulnerable code!