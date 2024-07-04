#!/usr/bin/env python3
"""This module contains a function filter_datum"""


import re
from typing import List
import logging


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns log message with PII fields obfuscated"""
    for field in fields:
        red = rf"\1{redaction}"  # to exclude first group from being replaced
        message = re.sub(rf"({field}=)[^{separator}]*", red, message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns filtered records from record"""
        logging.basicConfig(level=logging.INFO, format=self.FORMAT)
        flds = record.getMessage().split(";")
        formatted_message = "; ".join(flds)
        return logging.info(filter_datum(self.fields, self.REDACTION,
                                         formatted_message, self.SEPARATOR))
