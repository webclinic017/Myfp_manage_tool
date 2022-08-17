from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# The modules below should/must define __all__ with the objects wishes
# or prepend an "_" (underscore) to private classes/variables

from .bbroker import BackBroker, BrokerBack

try:
    from .ibbroker import IBBroker
except ImportError:
    pass  # The user may not have ibpy installed

try:
    from .vcbroker import VCBroker
except ImportError:
    pass  # The user may not have something installed

try:
    from .oandabroker import OandaBroker
except ImportError as e:
    pass  # The user may not have something installed
