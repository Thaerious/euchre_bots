# ABotInterface.py
# ABotInterface.py

from euchre import Snapshot


class ABotInterface:
    def decide(self, snap: Snapshot) -> tuple[str, object]:
        """
        Returns a tuple of action and either a Card or a suit (str) depending on state.
        """
        raise NotImplementedError()
