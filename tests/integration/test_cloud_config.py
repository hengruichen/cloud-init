# This file is part of cloud-init. See LICENSE file for license information.

import os
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent
from typing import List, Optional, Tuple

import pytest
from cloudinit import distros, helpers, subp
from cloudinit.config import cc_cloud_config
from cloudinit.config.schema import (
    SchemaValidationError,
    get_schema,
    validate_cloudconfig_schema,
)
from