# Has_Hooks.py
# Has_Hooks.py
class HasHooks:
    def __init__(self):
        self._hooks = {}

    def hook(self, event: str, func):
        """Register a function to a hook event."""
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(func)

        return self

    def _trigger_hook(self, event: str, *args, **kwargs):
        """Trigger all hooks associated with an event."""
        if event in self._hooks:
            for func in self._hooks[event]:
                func(*args, **kwargs)

        return self
