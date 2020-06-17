from django.apps import AppConfig


class ManagerActivitiesConfig(AppConfig):
    name = 'manager_activities'

    def ready(self):
    	import configurations.signals.handlers