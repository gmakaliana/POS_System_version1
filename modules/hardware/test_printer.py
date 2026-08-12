"""
GeoMaka POS Printer Hardware Test
"""


from hardware.receipt_printer import (
    test_print
)


success, message = test_print()


print()
print(
    "================================"
)
print(
    "GeoMaka POS Hardware Test"
)
print(
    "================================"
)
print(
    f"Success: {success}"
)
print(
    f"Message: {message}"
)
print(
    "================================"
)