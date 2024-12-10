from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print("Job実行")

sched = BackgroundScheduler(standalone=True, coalesce=True)
sched.add_job(job, "interval", minutes=10)
sched.start()
