from functools import wraps
from logging import getLogger

import attrs

__all__ = ("define",)
log = getLogger("anilibria.attrs")


define_defaults = dict(kw_only=True)


@wraps(attrs.define)
def define(**kwargs):
    return attrs.define(**kwargs, **define_defaults)
