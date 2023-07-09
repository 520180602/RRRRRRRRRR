# -*- coding: utf-8 -*-
# Gmail Lookup Tool
# Author: @smtpinjector
import re
import os
import socket
import smtplib
import dns.resolver
import threading
import random
from queue import Queue
from rich.console import Console
from emoji import emojize
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)



console = Console()
def log(msg, indent=0):
    indented = " " * indent
    console.print(f"{indented}{emojize(':inbox_tray:')} [bold orange_red1]Glook[/bold orange_red1] => {msg}")
def perr(msg):
    log(f"[bold red]{emojize(':x:')} {msg}[/bold red]")
def palr(msg, indent=0):
    log(f"[bold orange1]{emojize(':bell:')} {msg}[/bold orange1]", indent=indent)
def psuc(msg):
    log(f"[bold green]{emojize(':white_check_mark:')} {msg}[/bold green]")



load_dotenv()

MAX_THREADS = 0

def get_threads_count():
    try:
        palr("Enter the number of threads you want to run:")
        threads_count = int(input())
        if threads_count < 1:
            perr("Please enter a number greater than 0")
    except ValueError:
        threads_count = 10
        perr("Defaulting to 10 threads")
    return threads_count


def check_email(email_address):
    address_to_verify = email_address.strip().lower()
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', address_to_verify)
    if match is None:
        perr(f'{address_to_verify} => Bad Syntax')
        return

    domain_name = address_to_verify.split('@')[1]
    try:
        records = dns.resolver.query(domain_name, 'MX')
        mx_record = str(records[0].exchange)
    except Exception as e:
        perr(f"{address_to_verify} => MX record lookup failed")
        return

    host = socket.gethostname()
    server = smtplib.SMTP()
    server.set_debuglevel(0)
    try:
        server.connect(mx_record)
        server.helo(host)
        server.mail('me@domain.com')
        code, message = server.rcpt(address_to_verify)
        server.quit()
        if code == 250:
            psuc(f"{address_to_verify} => YY")
            with open('verified_emails.txt', 'a') as f:
                f.write(f"{address_to_verify}\n")
        else:
            perr(f"{address_to_verify} => NN")
    except Exception as e:
        perr(f"Failed to verify {address_to_verify}: {e}")


def worker(email_queue):
    while True:
        email = email_queue.get()
        if email is None:
            break
        check_email(email)
        email_queue.task_done()


def main():
    with open('h.txt', 'r') as f:
        emails = f.readlines()
    email_queue = Queue()
    for i in range(MAX_THREADS):
        threading.Thread(target=worker, args=(email_queue,)).start()
    for email in emails:
        email_queue.put(email)
    for i in range(MAX_THREADS):
        email_queue.put(None)
    email_queue.join()

if __name__ == "__main__":
    MAX_THREADS = get_threads_count()
    main()
