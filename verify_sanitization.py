import re

def sanitize_iid(iid):
    # This simulates the n8n expression: .replace(/[^0-9]/g, '')
    return re.sub(r'[^0-9]', '', iid)

# Test cases
test_cases = [
    "1234567 1234567 1234567",  # With spaces
    "1234-5678-9012",           # With dashes
    "ID: 123456789",            # With text prefix
    "12.34.56.78",              # With dots
    "123456789012345678901234567890" # Long valid numeric ID
]

print("Verification of IID sanitization (regex: [^0-9]):")
for case in test_cases:
    sanitized = sanitize_iid(case)
    print(f"Original: '{case}' -> Sanitized: '{sanitized}'")
    assert sanitized.isdigit(), f"Failed: {sanitized} contains non-digits"

print("\nAll test cases passed! The sanitization logic is robust.")
