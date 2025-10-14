import re
import math

# Optional: Load common passwords from a file
def load_common_passwords(filepath='common.txt'):
    try:
        with open(filepath, 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

# Entropy estimation based on character variety
def estimate_entropy(password):
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'\d', password): charset_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): charset_size += 32
    return round(len(password) * math.log2(charset_size)) if charset_size else 0

# Strength rating based on entropy
def rate_strength(entropy):
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Moderate"
    elif entropy < 80:
        return "Strong"
    else:
        return "Very Strong"

# Main checker
def check_password_strength(password, common_passwords=None):
    feedback = []
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 12 characters.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include digits.")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Include special characters.")

    if common_passwords and password.lower() in common_passwords:
        feedback.append("Avoid common passwords.")
        score = 0

    entropy = estimate_entropy(password)
    strength = rate_strength(entropy)

    print(f"\n Password Analysis:")
    print(f"Password: {password}")
    print(f"Entropy: {entropy} bits")
    print(f"Strength: {strength}")
    if feedback:
        print("\n Suggestions to improve:")
        for tip in feedback:
            print(f"- {tip}")
    else:
        print("\n Your password looks strong!")


if __name__ == "__main__":
    common_passwords = load_common_passwords()
    user_password = input("Enter a password to check: ")
    check_password_strength(user_password, common_passwords)