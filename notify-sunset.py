import signal
import sys
from time import sleep
import logging

from suntimes import suntimes
from notify_run import Notify
import schedule

class NotifySunset:
    def __init__(self) -> None:
        # Set up logging
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

        # Register signal handlers
        self._register_signal_handlers()

        # Set some safe defaults
        self.timeString = "09:00"
        self.timezone = "Europe/London"
        self.job = None

        # Update the time string and job
        self._UpdateJob()

        # Run forever
        self._Run()

    def _signal_handler(self, sig: int, _):
        # Handle SIGINT and SIGTERM signals to ensure the Docker container stops gracefully
        match sig:
            case signal.SIGINT:
                logging.info("Stopping due to keyboard interrupt...")
                sys.exit(0)
            case signal.SIGTERM:
                logging.info("Stopping due to SIGTERM...")
                sys.exit(0)

    def _register_signal_handlers(self) -> None:
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    # Function to send the notification
    def _SendSunsetTime(self) -> None:
        # Create the notification object
        notify = Notify(endpoint='https://notify.run/JWn7WTa1SBOXqJGI22RF')

        # Get the string to send
        sunsetString = suntimes.main()

        # Send the string
        notify.send(sunsetString)

    def _UpdateJob(self) -> None:
            # If a job already exists, cancel it
            if self.job:
                schedule.cancel_job(self.job)

            # Set the schedule to run once a day at the notification time in UTC
            self.job = schedule.every().day.at(self.timeString, self.timezone).do(self._SendSunsetTime)

            # Log that the job has been updated
            logging.info(f'Job set to run at {self.timeString} {self.timezone}')

    def _Run(self) -> None:
        # Run forever running any pending jobs and sleeping for a second in between
        while True:
            schedule.run_pending()
            sleep(1)

if __name__ == '__main__':
    NotifySunset()
