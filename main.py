#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import base64
from datetime import datetime, timedelta
from termcolor import colored
import json

def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config
    
config = load_config()

GITHUB_ACCESS_TOKEN = config["GITHUB_ACCESS_TOKEN"]
REPO_OWNER = config["REPO_OWNER"]
REPO_NAME = config["REPO_NAME"]
FILE_NAME = config["FILE_NAME"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def register_ip():
    clear_screen()
    print(colored("\nEnter the details to register a new IP:", "cyan"))
    ip_address = input("IP VPS: ")
    name = input("Name for the IP: ")
    
    thirty_days_from_now = datetime.now() + timedelta(days=30)
    registration_date = thirty_days_from_now.strftime('%Y-%m-%d')

    sha_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    response = requests.get(sha_url, headers=headers)
    sha = response.json().get("sha", "")

    content_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
    existing_content = requests.get(content_url, headers=headers).json().get("content", "")

    if existing_content:
        existing_content = base64.b64decode(existing_content).decode()

    new_entry = f"### {name} {registration_date} {ip_address}"
    new_content = f"{existing_content}\n{new_entry}" if existing_content else new_entry

    content_base64 = base64.b64encode(new_content.encode()).decode()

    commit_message = f"Register IP: {ip_address}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"

    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    payload = {"branch": "main", "content": content_base64, "message": commit_message, "sha": sha}
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        success_message = (
            f"\nSuccessfully Registered On GitHub!\n"
            f"Nama    : {name}\n"
            f"IP VPS  : {ip_address}\n"
            f"Expired : {registration_date}"
        )
        print(colored(success_message, "green"))
    else:
        print(colored(f"\nError: {response.status_code}, {response.text}", "red"))

    input("Press Enter to continue...")

def delete_ip():
    clear_screen()
    print(colored("\nEnter the details to delete an IP:", "cyan"))
    name = input("Name to delete: ")

    sha_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    response = requests.get(sha_url, headers=headers)
    sha = response.json().get("sha", "")

    content_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
    existing_content = requests.get(content_url, headers=headers).json().get("content", "")
    existing_content = base64.b64decode(existing_content).decode()

    updated_content = '\n'.join(line for line in existing_content.split('\n') if f"### {name}" not in line)

    content_base64 = base64.b64encode(updated_content.encode()).decode()

    commit_message = f"Delete IP: {name}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"

    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    payload = {"branch": "main", "content": content_base64, "message": commit_message, "sha": sha}
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(colored(f"\nEntry with name {name} successfully deleted from GitHub!", "green"))
    else:
        print(colored(f"\nError: {response.status_code}, {response.text}", "red"))

    input("Press Enter to continue...")

def list_registered_ips():
    clear_screen()
    content_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    existing_content = requests.get(content_url, headers=headers).json().get("content", "")

    if existing_content:
        existing_content = base64.b64decode(existing_content).decode()
        entries = [line.split() for line in existing_content.split('\n') if line.startswith("###")]

        if entries:
            sorted_entries = sorted(entries, key=lambda entry: datetime.strptime(entry[2], '%Y-%m-%d'))
            ips_message = "\n".join([f"{index + 1}. {entry[1]} {entry[2]} {entry[3]}" for index, entry in enumerate(sorted_entries)])
            print(colored(f"\nList of registered IPs:\n{ips_message}", "cyan"))
        else:
            print(colored("\nNo IPs are registered.", "yellow"))
    else:
        print(colored("\nNo IPs are registered.", "yellow"))

    input("Press Enter to continue...")

while True:
    clear_screen()
    print(colored("\nMenu:", "cyan"))
    print("1. Register IP")
    print("2. Delete IP")
    print("3. List registered IPs")
    print("4. Exit")

    choice = input(colored("Enter your choice (1-4): ", "cyan"))

    if choice == "1":
        register_ip()
    elif choice == "2":
        delete_ip()
    elif choice == "3":
        list_registered_ips()
    elif choice == "4":
        clear_screen()
        print(colored("\nExiting the program. Goodbye!", "cyan"))
        break
    else:
        print(colored("\nInvalid choice. Please enter a number between 1 and 4.", "red"))
        input("Press Enter to continue...")