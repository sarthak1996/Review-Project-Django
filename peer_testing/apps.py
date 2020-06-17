from django.apps import AppConfig


class PeerTestingConfig(AppConfig):
    name = 'peer_testing'

    def ready(self):
    	import configurations.signals.handlers
