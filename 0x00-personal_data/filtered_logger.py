#!/usr/bin/env python3
"""Returns log msg obfuscated"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with the list of fields to redact"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record and apply redaction"""
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message,
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Filters datum using regex"""
    pattern = '|'.join([f"{field}=[^{separator}]*" for field in fields])
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)
