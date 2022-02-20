from prometheus_client import Enum, Info

stream_status = Enum(
    "earhorn_stream_status",
    "Whether the stream is up",
    states=["up", "down"],
)
stream_silence = Enum(
    "earhorn_stream_silence",
    "Whether the stream is silent",
    states=["up", "down"],
)
unhandled_errors = Info(
    "earhorn_unhandled_errors",
    "Unhandled internal or stream errors",
)
