import schedule
import time
import psutil
import logging

# ロガーの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_system_usage():
    """システムのリソース使用率（CPU, メモリ）をログに出力する"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    
    logging.info(f"[Resource Check] CPU Usage: {cpu_usage}% | Memory Usage: {memory_info.percent}% ({memory_info.used / 1024 / 1024:.2f}MB / {memory_info.total / 1024 / 1024:.2f}MB)")

def run_schedule():
    """スケジュールタスクを実行する"""
    # 4分ごとにlog_system_usageを実行
    schedule.every(4).minutes.do(log_system_usage)
    
    logging.info("Scheduler started. Will log system usage every 4 minutes.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_schedule()