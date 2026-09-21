import functools
import socket
import logging

def proof_or_stop(timeout_seconds=5.0):
    """
    5-line drop-in decorator for HTTP 504 mitigation.
    Intercepts network timeouts and forcefully downgrades state to UNKNOWN.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            socket.setdefaulttimeout(timeout_seconds)
            try:
                return func(*args, **kwargs)
            except (socket.timeout, TimeoutError) as e:
                logging.error(f"[WIRE FAULT] Settlement state downgraded to UNKNOWN: {str(e)}")
                return {"status": "UNKNOWN", "reason": "HTTP 504 / TCP RST"}
        return wrapper
    return decorator
