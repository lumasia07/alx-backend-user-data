#!/usr/bin/env python3
"""Module to retrieve and display user data with sensitive information filtered."""

import os
import mysql.connector
import logging
from typing import List, Tuple

# Define PII_FIELDS with sensitive fields
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Filters datum using regex"""
    pattern = '|'.join([f"{field}=[^{separator}]*" for field in fields])
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a MySQLConnection object to the database."""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    if not db_name:
        raise ValueError("The database name must be set in the PERSONAL_DATA_DB_NAME environment variable")

    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return connection


def get_logger() -> logging.Logger:
    """Returns a logger with RedactingFormatter."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def main() -> None:
    """Retrieves and logs data from the users table."""
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


if __name__ == "__main__":
    main()
