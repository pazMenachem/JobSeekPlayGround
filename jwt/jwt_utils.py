"""
JWT Utility Functions

This module contains helper functions for JWT operations.
We'll build these step by step to understand each concept.
"""

import base64
import json
import time
from typing import Dict, Any
import jwt
from datetime import datetime, timedelta

# Secret key for signing JWTs (in production, use environment variables)
SECRET_KEY = "your-secret-key-change-in-production"

def explain_jwt_structure():
    """
    Explain the three parts of a JWT token.
    
    A JWT has 3 parts separated by dots (.)
    Format: header.payload.signature
    """
    print("=== JWT STRUCTURE EXPLANATION ===")
    print()
    
    # Part 1: Header
    print("1. HEADER (Algorithm & Token Type)")
    header = {
        "alg": "HS256",  # Algorithm used for signing
        "typ": "JWT"     # Token type
    }
    print(f"Header: {header}")
    print("Purpose: Tells how to verify the signature")
    print()
    
    # Part 2: Payload (Claims)
    print("2. PAYLOAD (Claims - the actual data)")
    payload = {
        "sub": "user123",           # Subject (user ID)
        "name": "John Doe",         # Custom claim
        "iat": 1640995200,          # Issued at (timestamp)
        "exp": 1641081600           # Expires at (timestamp)
    }
    print(f"Payload: {payload}")
    print("Purpose: Contains the actual information")
    print()
    
    # Part 3: Signature
    print("3. SIGNATURE (Verification)")
    print("Signature = HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret)")
    print("Purpose: Proves the token hasn't been tampered with")
    print()
    
    print("FINAL JWT LOOKS LIKE:")
    print("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNjQwOTk1MjAwLCJleHAiOjE2NDEwODE2MDB9.signature_here")
    print()
    print("Notice the 3 parts separated by dots (.)")

def demonstrate_jwt_parts():
    """
    Show how each part of JWT is encoded.
    """
    print("=== JWT ENCODING DEMONSTRATION ===")
    print()
    
    # Header
    header = {"alg": "HS256", "typ": "JWT"}
    header_json = json.dumps(header, separators=(',', ':'))
    header_encoded = base64.urlsafe_b64encode(header_json.encode()).decode().rstrip('=')
    print(f"Header JSON: {header_json}")
    print(f"Header Base64: {header_encoded}")
    print()
    
    # Payload
    payload = {"sub": "user123", "name": "John Doe"}
    payload_json = json.dumps(payload, separators=(',', ':'))
    payload_encoded = base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip('=')
    print(f"Payload JSON: {payload_json}")
    print(f"Payload Base64: {payload_encoded}")
    print()
    
    print("JWT = header.payload.signature")
    print(f"JWT = {header_encoded}.{payload_encoded}.[signature]")

def create_simple_jwt():
    """
    Create your first JWT token using PyJWT library.
    
    This function demonstrates the basic jwt.encode() function.
    """
    print("=== CREATING YOUR FIRST JWT ===")
    print()
    
    # Step 1: Define the payload (claims)
    payload = {
        "sub": "user123",           # Subject (user ID)
        "name": "John Doe",         # Custom claim
        "email": "john@example.com", # Custom claim
        "role": "admin",            # Custom claim
        "iat": int(time.time()),    # Issued at (current timestamp)
        "exp": int(time.time()) + 3600  # Expires in 1 hour
    }
    
    print("1. Payload (the data we want to store):")
    print(json.dumps(payload, indent=2))
    print()
    
    # Step 2: Create the JWT
    print("2. Creating JWT with PyJWT...")
    print("Command: jwt.encode(payload, SECRET_KEY, algorithm='HS256')")
    print()
    
    try:
        # This is the actual JWT creation!
        jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        print("3. Generated JWT Token:")
        print(f"Token: {jwt_token}")
        print()
        
        print("4. Token Analysis:")
        parts = jwt_token.split('.')
        print(f"   Header: {parts[0]}")
        print(f"   Payload: {parts[1]}")
        print(f"   Signature: {parts[2][:20]}...")
        print()
        
        return jwt_token
        
    except Exception as e:
        print(f"Error creating JWT: {e}")
        return None

def explain_jwt_encode_parameters():
    """
    Explain each parameter in jwt.encode() function.
    """
    print("=== JWT.ENCODE() PARAMETERS EXPLAINED ===")
    print()
    
    print("jwt.encode(payload, key, algorithm)")
    print()
    print("1. PAYLOAD (dict):")
    print("   - The data you want to store in the token")
    print("   - Can contain any JSON-serializable data")
    print("   - Common fields: sub, iat, exp, name, role")
    print()
    
    print("2. KEY (string):")
    print("   - Secret key used to sign the token")
    print("   - MUST be kept secret!")
    print("   - Used to verify token authenticity")
    print("   - In production: use environment variables")
    print()
    
    print("3. ALGORITHM (string):")
    print("   - How to sign the token")
    print("   - Common: 'HS256', 'RS256', 'ES256'")
    print("   - HS256 = HMAC with SHA-256 (symmetric)")
    print("   - RS256 = RSA with SHA-256 (asymmetric)")
    print()

def create_jwt_with_custom_data():
    """
    Create JWT with custom user data.
    """
    print("=== CREATING JWT WITH CUSTOM DATA ===")
    print()
    
    # Custom user data
    user_data = {
        "user_id": "emp_001",
        "name": "Alice Smith",
        "email": "alice@company.com",
        "department": "Engineering",
        "role": "Senior Developer",
        "permissions": ["read", "write", "delete"],
        "manager": "emp_002",
        "office": "New York"
    }
    
    # Add standard JWT claims
    payload = {
        **user_data,  # Spread custom data
        "sub": user_data["user_id"],  # Subject (required)
        "iat": int(time.time()),      # Issued at
        "exp": int(time.time()) + 7200  # Expires in 2 hours
    }
    
    print("Custom user data:")
    print(json.dumps(user_data, indent=2))
    print()
    
    # Create JWT
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    print("Generated JWT:")
    print(f"Token: {jwt_token}")
    print()
    
    # Calculate token size
    token_size = len(jwt_token.encode('utf-8'))
    print(f"Token size: {token_size} bytes")
    print(f"Cookie limit: 4096 bytes")
    print(f"Usage: {(token_size / 4096) * 100:.1f}%")
    
    return jwt_token

if __name__ == "__main__":
    explain_jwt_structure()
    print("\n" + "="*50 + "\n")
    demonstrate_jwt_parts()
    print("\n" + "="*50 + "\n")
    explain_jwt_encode_parameters()
    print("\n" + "="*50 + "\n")
    create_simple_jwt()
    print("\n" + "="*50 + "\n")
    create_jwt_with_custom_data()

