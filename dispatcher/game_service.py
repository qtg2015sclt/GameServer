"""Game Service."""
from dispatcher import Service


class GameSyncService(Service):
    """Game sync service."""

    SERVICE_ID = 2000
    ClientSyncCmdID = 1001

    def __init__(self):
        """Register all handle functions."""
        super(GameSyncService, self).__init__(self.SERVICE_ID)
        command_dict = {
            self.ClientSyncCmdID: self.player_sync,
        }
        self.registers(command_dict)

    def player_sync(self, msg, who):
        """Sync msg of players."""
        raise NotImplementedError
