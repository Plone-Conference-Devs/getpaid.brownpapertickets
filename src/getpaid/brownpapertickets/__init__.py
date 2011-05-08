import interfaces
from getpaid.core.options import PersistentOptions


BPTOptions = PersistentOptions.wire(
    "BPTOptions",
    "getpaid.brownpapertickets",
    interfaces.IBPTOptions)
