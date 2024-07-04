#!/usr/bin/env python3
"""This module contains a function filter_datum"""


import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns log message with PII fields obfuscated"""
    for field in fields:
        red = r"\1" + redaction  # to exclude first group from being replaced
        str1 = re.sub(rf"({field}=)[a-zA-Z0-9/]*", red, message)
        message = str1  # make subbed string new string to maintain subs
    return str1
