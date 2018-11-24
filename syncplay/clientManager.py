from twisted.internet.endpoints import clientFromString, HostnameEndpoint

from syncplay import ui
from syncplay.messages import getMessage
from syncplay.ui.ConfigurationGetter import ConfigurationGetter


class SyncplayClientManager(object):
    def run(self):
        config = ConfigurationGetter().getConfiguration()
        from syncplay.client import SyncplayClient  # Imported later, so the proper reactor is installed
        interface = ui.getUi(graphical=not config["noGui"])
        syncplayClient = SyncplayClient(config["playerClass"], interface, config)
        if syncplayClient:
            interface.addClient(syncplayClient)
            from twisted.internet import reactor
            if config['endpoint']:
                endpoint = clientFromString(reactor, config['endpoint'])
            else:
                endpoint = HostnameEndpoint(reactor, config['host'], config['port'])
            syncplayClient.start(endpoint)
        else:
            interface.showErrorMessage(getMessage("unable-to-start-client-error"), True)
