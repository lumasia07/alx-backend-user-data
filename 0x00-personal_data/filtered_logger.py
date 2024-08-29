#!/usr/bin/env python3
"""Returns log msg obfuscated"""
import re
from typing import List, Tuple, Optional
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """Returns a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """Returns a MySQLConnection object"""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError("The db name must be set in the PERSONAL_DATA_DB_NAME env")

    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return connection


def main() -> None:
    """Main function that retrieves and logs data from the users table."""
    db_connection = get_db()
    cursor = db_connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    logger = get_logger()

    for row in rows:
        message = "; ".join([f"{key}={value}" for key, value in row.items()])
        logger.info(message)

    cursor.close()
    db_connection.close()

