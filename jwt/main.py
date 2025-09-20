"""
Simple JWT Learning Project

This project demonstrates JWT (JSON Web Token) concepts step by step.
Perfect for learning authentication fundamentals.
"""

from jwt_utils import (
    explain_jwt_structure, 
    demonstrate_jwt_parts,
    explain_jwt_encode_parameters,
    create_simple_jwt,
    create_jwt_with_custom_data
)

def main():
    """Main function to run the JWT learning examples."""
    print("Welcome to JWT Learning Project!")
    print("This project will teach you JWT concepts step by step.")
    print()
    
    # Step 2: Understanding JWT Structure
    explain_jwt_structure()
    print("\n" + "="*50 + "\n")
    demonstrate_jwt_parts()
    print("\n" + "="*50 + "\n")
    
    # Step 3: Creating JWT Tokens
    explain_jwt_encode_parameters()
    print("\n" + "="*50 + "\n")
    create_simple_jwt()
    print("\n" + "="*50 + "\n")
    create_jwt_with_custom_data()

if __name__ == "__main__":
    main()
