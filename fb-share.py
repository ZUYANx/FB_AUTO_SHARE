#!/usr/bin/python3
# CODED BY - ZUYAN
# PROJECT - FB POST AUTO SHARE
# TEAM - XVSOULX

import os
import sys
import json
import time
import requests
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# File paths for storing cookies and tokens
STORAGE_DIR = "/data/data/com.termux/files/home/storage/shared"
COOKIE_FILE = os.path.join(STORAGE_DIR, ".cookie.txt")
TOKEN_FILE = os.path.join(STORAGE_DIR, ".token.txt")

line = 45 * '-'

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def animate_text(text, color=Fore.GREEN, delay=0.05):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()

def print_banner():
    print(Fore.CYAN + """
    ▗▖  ▗▖▗▖  ▗▖ ▗▄▄▖ ▗▄▖ ▗▖ ▗▖▗▖   ▗▖  ▗▖
     ▝▚▞▘ ▐▌  ▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌    ▝▚▞▘ 
      ▐▌  ▐▌  ▐▌ ▝▀▚▖▐▌ ▐▌▐▌ ▐▌▐▌     ▐▌  
    ▗▞▘▝▚▖ ▝▚▞▘ ▗▄▄▞▘▝▚▄▞▘▝▚▄▞▘▐▙▄▄▖▗▞▘▝▚▖""")
    print(Fore.MAGENTA + "           FB POST AUTO SHARE TOOL")
    print(Fore.YELLOW + "              CODED BY - ZUYAN")
    print(Fore.GREEN + "               TEAM - XVSOULX")
    print(Fore.CYAN + line)

def save_data(file_path, data):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(data)

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()
    return None

def remove_data(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(Fore.GREEN + f"(>) Removed {file_path}")
    else:
        print(Fore.RED + f"(!!) File {file_path} does not exist.")

def parse_cookies(cookie_string):
    cookies = {}
    for part in cookie_string.split(";"):
        if "=" in part:
            key, value = part.strip().split("=", 1)
            cookies[key] = value
    return cookies

def ZUYAN_Login():
    clear_screen()
    print_banner()
    
    cookie = input(Fore.YELLOW + "(+) ENTER COOKIES: ").strip()
    token = input(Fore.YELLOW + "(+) ENTER TOKEN: ").strip()
    print(Fore.CYAN + line)
    
    if not cookie or not token:
        print(Fore.RED + "(!!) Cookies and Token are required.")
        time.sleep(2)
        return
    
    save_data(COOKIE_FILE, cookie)
    save_data(TOKEN_FILE, token)
    print(Fore.GREEN + "(>) LOGIN SUCCESSFUL")
    print(Fore.CYAN + line)
    time.sleep(2)
    main_menu()

def ZUYAN_Share():
    clear_screen()
    print_banner()
    
    token = load_data(TOKEN_FILE)
    cookie_string = load_data(COOKIE_FILE)
    
    if not token or not cookie_string:
        print(Fore.RED + "(!!) No token or cookies found. Please login first.")
        time.sleep(2)
        main_menu()
        return
    
    try:
        cookies = parse_cookies(cookie_string)
        user_info = requests.get(
            f"https://graph.facebook.com/me?fields=name,id&access_token={token}",
            cookies=cookies
        ).json()
        nama = user_info.get("name")
        user_id = user_info.get("id")
        ip = requests.get("https://api.ipify.org").text
        
        print(Fore.GREEN + f"[+] YOUR NAME: {nama}")
        print(Fore.GREEN + f"[+] YOUR UID: {user_id}")
        print(Fore.GREEN + f"[+] YOUR IP: {ip}")
        print(Fore.CYAN + line)
        
        link = input(Fore.YELLOW + "(+) ENTER POST LINK: ").strip()
        limit = int(input(Fore.YELLOW + "(?) ENTER SHARE LIMIT: "))
        print(Fore.CYAN + line)
        
        header = {
            "authority": "graph.facebook.com",
            "cache-control": "max-age=0",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1"
        }
        
        for x in tqdm(range(limit), desc=Fore.BLUE + "Sharing Posts", unit="post"):
            post = requests.post(
                f"https://graph.facebook.com/v13.0/me/feed?link={link}&published=0&access_token={token}",
                headers=header,
                cookies=cookies
            ).json()
            #print(post)
            if "id" in post:
                print(Fore.GREEN + f"(>) Successfully Shared - [{x + 1}]")
            else:
                print(Fore.RED + f"(>) Failed To Share! Error: {post.get('error', {}).get('message', 'Unknown error')}")
            print(Fore.CYAN + line)
        
        print(Fore.GREEN + "\n(/) XVSOULX Post Share Completed!")
        time.sleep(2)
        main_menu()
    
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "(!!) Internet Connection Error!")
        print(Fore.CYAN + line)
        time.sleep(2)
        main_menu()
    except Exception as e:
        print(Fore.RED + f"(!!) ERROR: {str(e)}")
        print(Fore.RED + "(!!) Something went wrong. Please check your token and try again.")
        print(Fore.CYAN + line)
        time.sleep(2)
        main_menu()

def main_menu():
    clear_screen()
    print_banner()
    
    print(Fore.YELLOW + "[1] SHARE POST")
    print(Fore.YELLOW + "[2] REMOVE TOKEN & COOKIES")
    print(Fore.YELLOW + "[0] EXIT")
    print(Fore.CYAN + line)
    
    choice = input(Fore.YELLOW + "(?) SELECT OPTION: ").strip()
    
    if choice == "1":
        ZUYAN_Share()
    elif choice == "2":
        remove_data(COOKIE_FILE)
        remove_data(TOKEN_FILE)
        time.sleep(2)
        main_menu()
    elif choice == "0":
        animate_text("Exiting...", Fore.RED)
        sys.exit()
    else:
        print(Fore.RED + "(!!) INVALID OPTION")
        time.sleep(2)
        main_menu()

if __name__ == "__main__":
    if not os.path.exists(COOKIE_FILE) or not os.path.exists(TOKEN_FILE):
        ZUYAN_Login()
    else:
        main_menu()