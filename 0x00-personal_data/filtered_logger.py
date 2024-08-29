#!/usr/bin/env python3
"""Returns log msg obfuscated"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Filters datum using regex"""
    pattern = '|'.join([f"{field}=[^{separator}]*" for field in fields])
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)
