#!/usr/bin/env python3
"""This module contains a function filter_datum"""


import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns log message with PII fields obfuscated"""
    for field in fields:
        red = rf"\1{redaction}"  # to exclude first group from being replaced
        message = re.sub(rf"({field}=)[^{separator}]*", red, message)
    return message
