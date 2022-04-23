from time import sleep
from suntimes import suntimes
from notify_run import Notify
from schedule import Scheduler

def SendSunsetTime() -> None:
    sunsetString = suntimes.main()

    notify = Notify(endpoint='https://notify.run/JWn7WTa1SBOXqJGI22RF')

    notify.send(sunsetString)

if __name__ == '__main__':
    schedule = Scheduler()

    schedule.every().day.at('09:00').do(SendSunsetTime)

    while True:
        schedule.run_pending()
        sleep(1)
