from datetime import datetime, timedelta
from time import sleep
from zoneinfo import ZoneInfo

from suntimes import suntimes
from notify_run import Notify
import schedule

class NotifySunset:
    def __init__(self) -> None:
        # Set some safe defaults
        self.timeString = None
        self.job = None

        # Update the time string and job
        self._UpdateJob()

        # Run forever
        self._Run()

    # Function to send the notification
    def _SendSunsetTime(self) -> None:
        # Create the notification object
        notify = Notify(endpoint='https://notify.run/JWn7WTa1SBOXqJGI22RF')

        # Get the string to send
        sunsetString = suntimes.main()

        # Send the string
        notify.send(sunsetString)

        # Update the job if necessary
        self._UpdateJob()

    def _UpdateJob(self) -> None:
        # Get an aware datetime for tomorrow
        nowTime = datetime.now().astimezone(ZoneInfo('Europe/London')) + timedelta(days=1)

        # Set the datetime to local 9am (still tomorrow)
        localNotificationTime = nowTime.replace(hour=9, minute=0)

        # Convert 9am tomorrow into UTC
        utcNotificationTime = localNotificationTime.astimezone(ZoneInfo('UTC'))

        # Get the time string for use in scheduling the job
        timeString = utcNotificationTime.strftime('%H:%M')

        # If the timestring has changed (i.e., GMT <-> BST changover)
        if self.timeString != timeString:
            # Update the timestring member
            self.timeString = timeString

            # If a job already exists, cancel it
            if self.job:
                schedule.cancel_job(self.job)

            # Set the schedule to run once a day at the notification time in UTC
            self.job = schedule.every().day.at(self.timeString).do(self._SendSunsetTime)

            # Log that the job has been updated
            print(f'Job set to run at {self.timeString} UTC')

    def _Run(self) -> None:
        # Run forever running any pending jobs and sleeping for a second in between
        while True:
            schedule.run_pending()
            sleep(1)

if __name__ == '__main__':
    NotifySunset()
