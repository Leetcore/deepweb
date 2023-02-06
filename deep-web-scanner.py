import threading
import ipaddress
import socket
import time
from datetime import datetime
from typing import Optional, Union
import requests
requests.packages.urllib3.disable_warnings()  # type: ignore
from concurrent.futures import ThreadPoolExecutor
import colorama
import random

colorama.init(autoreset=True)
import os
import bs4
import argparse



folder = os.path.dirname(__file__)
output_strings: list[str] = []
ports = [80, 443, 3000, 3128, 5000, 8080, 8081, 8443, 4434]
keywords = ["cam", "rasp", " hp ", "system", "index of", "dashboard", "webmail" ,"roundcube", "logs"]
output_tmp = ""
last_write = time.time()
global_lock = threading.Lock()
banner_targets: list[dict[str, Union[str, int]]] = []

def main():
    print("----------------------------")
    print("      Deep Web Scanner!     ")
    print("----------------------------\n")
    print("Every active webserver url will be logged in the output file.")
    print("This terminal will only show urls/metadata with the following keywords: " + ", ".join(keywords))
    if indexof.lower() == "true":
        print ("'Index of /' filenames will be logged!")
    print("Scan will start...")

    with open(input_file, "r") as myfile:
        content = myfile.readlines()
        
        for line in content:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            line = random.choice(content)
            # split ip range 2.56.20.0-2.56.23.255
            if "-" in line:
                ip_range_array = line.split("-")
                ip_range_start = ip_range_array[0].strip()
                ip_range_end = ip_range_array[1].strip()
                print(f"[*] {current_time} - Start scan from range: {ip_range_start} - {ip_range_end}")

                current_ip = ipaddress.IPv4Address(ip_range_start)
                end_ip = ipaddress.IPv4Address(ip_range_end)

                with ThreadPoolExecutor(max_workers=150) as executor_portcheck:
                    while current_ip < end_ip:
                        executor_portcheck.submit(start_portcheck, current_ip.exploded)
                        current_ip += 1

            elif "/" in line:
                ip_range = ipaddress.ip_network(line.strip())
                with ThreadPoolExecutor(max_workers=150) as executor_portcheck:
                    for ip in ip_range.hosts():
                        executor_portcheck.submit(start_portcheck, ip.exploded)

            else:
                print("No valid input file! Should be something like 2.56.20.0-2.56.23.255 per line!")
                
            global banner_targets
            print(f"[*] {current_time} - got {len(banner_targets)} responses")
            for target in banner_targets:
                start_request(target["ip"], target["port"])  # type: ignore
            banner_targets.clear()
        write_line("", True)


def still_running():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    while True:
        wait = 15
        for i in range(wait+1):
            write_line(f"[*] {current_time} - Scan is still running")

def start_portcheck(ip: str) -> None:
    global banner_targets
    # fast webserver port checking
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                # queue normal browser request
                banner_targets.append({"ip": ip, "port": port})
        
def start_request(ip: str, port: int):
    # check for running websites
    try:
        url = "https://" + ip + ":" + str(port)
        if port == 80:
            url = "http://" + ip
        elif port == 8080:
            url = "http://" + ip + ":8080"
        elif port == 8081:
            url = "http://" + ip + ":8081"
        elif port == 3000:
            url = "http://" + ip + ":3000"
        elif port == 3128:
            url = "http://" + ip + ":3128"
        elif port == 5000:
            url = "http://" + ip + ":5000"
        

        site_result = request_url(url)
        if not isinstance(site_result, bool) and site_result is not False:
            # if the site is reachable get some information
            get_banner(site_result[0], site_result[1])  # type: ignore
    except Exception as e:
        print(e)

def request_url(url: str) -> Union[tuple[requests.Response, bs4.BeautifulSoup], bool]:
    # request url and return the response
    try:
        session = requests.session()
        session.headers[
            "User-Agent"
        ] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
        header = session.head(url=url, timeout=20, verify=False)

        # check content type
        one_allowed_content_type = False
        content_type_header = header.headers.get("content-type")
        if content_type_header is not None:
            for allowed_content_type in ["html", "plain", "xml", "text", "json"]:
                if allowed_content_type in content_type_header.lower():
                    one_allowed_content_type = True
            if not one_allowed_content_type:
                return False
        else:
            return False

        response = session.get(url=url, timeout=30, verify=False)
        session.close()

        soup = bs4.BeautifulSoup(response.text, "html.parser")
        return (response, soup)
    except Exception:
        return False

def get_banner(request: requests.Response, soup: bs4.BeautifulSoup):
    now = datetime.now()
    current_time = now.strftime("%d.%m. - %H:%M:%S")
    # get banner information, show console output and save them to file
    banner_array: list[str] = []
    banner_array.append(request.url)
    server_header = request.headers.get("Server")
    if isinstance(server_header, str):
        banner_array.append(server_header)
        title = soup.find("title")
        if isinstance(title, bs4.Tag):
            title = title.get_text().strip().replace("\n", "")
            banner_array.append(title)
        
        meta_tags: bs4.element.ResultSet[bs4.Tag] = soup.find_all("meta", attrs={"name": "generator"})
        if len(meta_tags) > 0:
            for meta_tag in meta_tags:
                attrs = meta_tag.attr
                if isinstance(attrs, bs4.Tag):
                    generator = attrs.get("content")
                    if isinstance(generator, str):
                        banner_array.append(generator)

    # has this site a password field?
    password_fields = soup.find_all(attrs={"type": "password"})
    if len(password_fields) > 0:
        banner_array.append("login required")

    # check for "index of" websites and show root files/folders
    global indexof
    if indexof.lower() == "true" and "index of" in request.text.lower():
        a_array: list[bs4.Tag] = soup.find_all("a")
        for a in a_array:
            href = a.attrs.get("href")
            if isinstance(href, str):
                if href.find("?") != 0:
                    banner_array.append(href)

    banner_array.append(f"{str(len(request.content))} content size")

    fullstring = ", ".join(str(item) for item in banner_array)
    if fullstring not in output_strings:
        output_strings.append(fullstring)
        for keyword in keywords:
            if keyword in fullstring.lower():
                if "login required" in fullstring:
                    print(f"{colorama.Fore.RED}[+] {current_time} - {fullstring}")
                elif "Index of /" in fullstring:
                    print(f"{colorama.Fore.YELLOW}[+] {current_time} - {fullstring}")
                else:
                    print(f"{colorama.Fore.GREEN}[+] {current_time} - {fullstring}")
        write_line(fullstring)

def write_line(line: str, force: Optional[bool] = False):
    # buffers and writes output to file
    now = datetime.now()
    current_time = now.strftime("%d.%m. - %H:%M:%S")
    global output_tmp, last_write
    output_tmp += line + "\n"

    if last_write + 30 < time.time() or force:
        last_write = time.time()

        while global_lock.locked():
            continue

        global_lock.acquire()

        lines_to_write = output_tmp.count("\n")
        with open(output_file, "a") as output_1:
            output_1.write(output_tmp)
            output_tmp = ""

        if lines_to_write > 1:
            print(f"{colorama.Fore.BLUE}[*] {current_time} - {lines_to_write} webservers found and written to file")
        else:
            print(f"{colorama.Fore.BLUE}[*] {current_time} - {lines_to_write} webservers found and written to file")

        global_lock.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if domain has an active website and grab banner."
    )
    parser.add_argument(
        "-i", type=str, default="./asn-country-ipv4.csv", help="Path to input file"
    )
    parser.add_argument(
        "-o", type=str, default="./deep-web.txt", help="Path to output file"
    )
    parser.add_argument(
        "-indexof", type=str, default="no", help="Show files from index of sites"
    )
    args = parser.parse_args()
    input_file = args.i
    output_file = args.o
    indexof = args.indexof
    main()
