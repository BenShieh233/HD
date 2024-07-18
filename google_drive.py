import os
import time
from datetime import datetime, timedelta
import schedule
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pytz
from scraper import Scraper

def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication
    return GoogleDrive(gauth)

def upload_to_drive(file_path, folder_id='root'):
    drive = authenticate_google_drive()
    file_name = os.path.basename(file_path)
    file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    print(f"File {file_name} uploaded to Google Drive.")

def run_scraper():
    base_url = 'https://www.homedepot.com/b/Lighting-Ceiling-Fans-Ceiling-Fans-With-Lights/N-5yc1vZcjnu?NCNI-5&searchRedirect=ceiling%20fan%20with%20lights&semanticToken=k27r10r00f22000000000e_202407051741572580635995840_us-central1-bz9l%20k27r10r00f22000000000e%20%3E%20st%3A%7Bceiling%20fan%20with%20lights%7D%3Ast%20ml%3A%7B24%7D%3Aml%20nr%3A%7Bceiling%20fan%20with%20lights%7D%3Anr%20nf%3A%7Bn%2Fa%7D%3Anf%20qu%3A%7Bceiling%20fan%20with%20lights%7D%3Aqu%20ie%3A%7B0%7D%3Aie%20qr%3A%7Bceiling%20fan%20with%20lights%7D%3Aqr'  # Replace with your actual base URL
    scraper = Scraper(base_url)
    scraper.scrape(start_page=1, end_page=5)
    df = scraper.to_dataframe()
    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    file_name = f"HD_products_{timestamp}.csv"
    file_path = os.path.join('My Drive/HD_competitive_analysis', file_name)
    df.to_csv(file_path)
    upload_to_drive(file_path, folder_id='1tiu74hnlyNGhVOBYQN8SNdnmbKXBr_th')  # Replace with your actual folder ID


def schedule_task_at(time_str, func, tz):
    now = datetime.now(tz)
    target_time = datetime.strptime(time_str, '%H:%M').replace(
        year=now.year, month=now.month, day=now.day, tzinfo=tz
    )
    if now > target_time:
        target_time += timedelta(days=1)
    delay = (target_time - now).total_seconds()
    schedule.every(delay).seconds.do(func)

def schedule_tasks():
    seattle_tz = pytz.timezone('America/Los_Angeles')
    times = ["12:00", "13:00", "18:00", "19:00"]
    for time_str in times:
        schedule_task_at(time_str, run_scraper, seattle_tz)



if __name__ == '__main__':

    base_url = 'https://www.homedepot.com/b/Lighting-Ceiling-Fans-Ceiling-Fans-With-Lights/N-5yc1vZcjnu?NCNI-5&searchRedirect=ceiling%20fan%20with%20lights&semanticToken=k27r10r00f22000000000e_202407051741572580635995840_us-central1-bz9l%20k27r10r00f22000000000e%20%3E%20st%3A%7Bceiling%20fan%20with%20lights%7D%3Ast%20ml%3A%7B24%7D%3Aml%20nr%3A%7Bceiling%20fan%20with%20lights%7D%3Anr%20nf%3A%7Bn%2Fa%7D%3Anf%20qu%3A%7Bceiling%20fan%20with%20lights%7D%3Aqu%20ie%3A%7B0%7D%3Aie%20qr%3A%7Bceiling%20fan%20with%20lights%7D%3Aqr'
    scraper = Scraper(base_url)
    scraper.scrape(start_page=1, end_page=5)
    df = scraper.to_dataframe()

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    df.to_csv(f'HD_products{timestamp}.csv')