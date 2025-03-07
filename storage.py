from typing import Dict, Any
from threading import Lock

class Storage:
    def __init__(self):
        self._data = {}
        self._lock = Lock()

    def set(self, key: str, value: Any) -> None:
        """Thread-safe storage of key-value pairs."""
        with self._lock:
            self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Thread-safe retrieval of values."""
        with self._lock:
            return self._data.get(key, default)

    def delete(self, key: str) -> None:
        """Thread-safe deletion of keys."""
        with self._lock:
            self._data.pop(key, None)

    def clear(self) -> None:
        """Thread-safe clearing of all data."""
        with self._lock:
            self._data.clear()
