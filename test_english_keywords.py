#!/usr/bin/env python3
"""Test English keyword detection"""

from main import transpile

print("=" * 60)
print("TEST 1: Valid - pure Czech code")
print("=" * 60)

valid_code = """
x = 0
výraz = Pravda
pro i v [1; 2; 3]:
    vytiskni(i)
"""

try:
    result = transpile(valid_code)
    print("✓ Valid Czech code passed validation")
except ValueError as e:
    print(f"✗ Unexpected error: {e}")

print("\n" + "=" * 60)
print("TEST 2: Invalid - contains 'if' (English keyword)")
print("=" * 60)

invalid_code1 = """
x = 0
if x > 0:
    vytiskni(x)
"""

try:
    transpile(invalid_code1)
    print("✗ Should have caught English keyword 'if'")
except ValueError as e:
    print(f"✓ Caught error: {e}")

print("\n" + "=" * 60)
print("TEST 3: Invalid - contains 'for' (English keyword)")
print("=" * 60)

invalid_code2 = """
for i in [1, 2, 3]:
    vytiskni(i)
"""

try:
    transpile(invalid_code2)
    print("✗ Should have caught English keyword 'for'")
except ValueError as e:
    print(f"✓ Caught error: {e}")

print("\n" + "=" * 60)
print("TEST 4: Invalid - contains 'class' (English keyword)")
print("=" * 60)

invalid_code3 = """
class Zvire:
    def zvuk(self):
        přejdi
"""

try:
    transpile(invalid_code3)
    print("✗ Should have caught English keyword 'class'")
except ValueError as e:
    print(f"✓ Caught error: {e}")
