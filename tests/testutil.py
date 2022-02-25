import logging

from .utils import config  # noqa
from .utils import get_token

logger = logging.getLogger(__name__)

token = get_token()
