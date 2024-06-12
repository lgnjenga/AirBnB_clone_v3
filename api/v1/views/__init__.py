#!/usr/bin/python3

"""
init comment
"""

from flask import Blueprint

app_views = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Wildcard import (for internal use, PEP8 warnings can be ignored)
from . import index

