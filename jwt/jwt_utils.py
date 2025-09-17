"""
JWT Utility Functions

This module contains helper functions for JWT operations.
We'll build these step by step to understand each concept.
"""

import base64
import json
from typing import Dict, Any

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

if __name__ == "__main__":
    explain_jwt_structure()
    print("\n" + "="*50 + "\n")
    demonstrate_jwt_parts()
