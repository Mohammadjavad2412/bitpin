from django.core.management.base import BaseCommand
import subprocess
import threading
import logging
import traceback


class Command(BaseCommand):
    help = 'run application with migration'

    def run(self):
        try:
            subprocess.run(['make', 'run'])
        except:
            logging.error(traceback.format_exc())

    def handle(self, *args, **kwargs):
        t0 = threading.Thread(target=self.initial_datas)
        t0.start()
        t0.join()
    