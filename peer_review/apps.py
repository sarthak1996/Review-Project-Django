from django.apps import AppConfig


class PeerReviewConfig(AppConfig):
    name = 'peer_review'

    def ready(self):
    	import configurations.signals.handlers