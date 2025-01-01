import asyncio
import csv
import random
import time
from datetime import datetime
from threading import Lock

import noble_tls
from noble_tls import Client

# Constants
PROXY_FILE = "proxies.txt"  # File containing proxies (one per line in the format ip:port:user:password)
CSV_INPUT_FILE = "../../Datasets/Companies/companies-stuttgart.csv"  # Input CSV file with LinkedIn URLs
CSV_OUTPUT_FILE = "Results/LinkedIn/Companies/"+CSV_INPUT_FILE.split("Companies/")[1].split(".csv")[0]+"_linkedin.csv"  # Output CSV file for results
MAX_CONCURRENT_TASKS = 1  # Number of concurrent tasks
SAVE_INTERVAL = 10  # Save results every 10 seconds

HEADERS = {
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "de-DE,de;q=0.9",
    "priority": "u=0, i",
    "cookie": """bcookie="v=2&ee10d884-c977-4861-80f2-d7d1a9a45245"; li_gc=MTswOzE3MjQ5NDgzNDg7MjswMjEoYapxl+tQulIVGdD+3g8bVog7aJIWIKGcEPEqi/gYtw==; fid=AQH_0bFqyBgG5QAAAZQYXpLBvIvinHcDm5-hJHYGFXe9WdfQRQFNci7SezWBWhxDOGG3SmDOQl88dg; JSESSIONID=ajax:5152424158188856001; lang=v=2&lang=en-us; bscookie="v=1&202412301620380080bda9-227f-4265-85ff-ac8473e83362AQHrcn1OQn3l17qlSV6sNmi5VJGp9U-O"; __cf_bm=acpytBRTfcJ2xeD5zweldRKlwA3qjaFzQhYS1FyP3Lw-1735575638-1.0.1.1-kNqxtzMswEuCAogr5xUjHC8ieL2KXIDXhQgSVShUA.NnR0jHEpXBUhWn30BgBbcC1WaVCgjGZtyUctrwqJl64A; li_alerts=e30=; g_state={"i_l":0}; liap=true; li_at=AQEDAVYul0gAOvDrAAABlBhfAkYAAAGUPGuGRk0AaWZs14F6LyQL2MZvCHcEGUIG0nF5gMALUJBRYz4vAJF82hzFku7XebsgPzQFbDWwtmWfAoKp3HmyIOqS2DTSDX8DcdaHgcxt8-jzBFpHkon-Yrte; lidc="b=VGST04:s=V:r=V:a=V:p=V:g=3417:u=1:x=1:i=1735575667:t=1735662067:v=2:sig=AQGuwvyI0fraroFVPzEqiPbm5DkauUTB"; li_mc=MTswOzE3MzU1NzU2Njc7MjswMjHmU3eTA5+mVl+SvduYWZ/1Knq2AKSyqZVUZ81LGYzfxw==; timezone=Europe/Berlin; li_theme=light; li_theme_set=app; dfpfpt=1751713f20f7411e9b9593a38ba40b4c; fptctx2=taBcrIH61PuCVH7eNCyH0LNKRXFdWqLJ6b8ywJyet7W1QRukDDR8%252fOqtKlU9HCLjoBMn40CO1h0DRtZGGoKfEnByfFt3AUYl79Yql4pgIv2%252brMynw8ZYQ1fiad66gZ2Lh4VFlxY2vp6phuZ0qSOUqIsEJcWkw9bdo9%252fcrNaVlk5WC6Xgei6WAruIveYZHKYPvcFpAMoLeUAvBO1THa5gD%252fkKGT%252bvWeIiXhowg0sG61r0FuMAwMUxSdHVlm8SHm3hB4YI6EqymBuzNVy63sytlgpmLsxrsCNMQnF4MtBcL2lN3D7vW2FVeg2QdzdkRZoQPM013%252bNDJYpXCYBCwz%252fBq%252fSNzbszGlZjYmtySF9J9MI%253d"""
}
# Global variables
results = []
results_lock = Lock()


# Read proxies from file
def load_proxies(file_path):
    proxies = []
    with open(file_path, "r") as file:
        for line in file:
            proxy_parts = line.strip().split(":")
            if len(proxy_parts) == 4:
                proxies.append({
                    "ip": proxy_parts[0],
                    "port": proxy_parts[1],
                    "user": proxy_parts[2],
                    "password": proxy_parts[3],
                })
    return proxies


# Rotate proxies
def get_random_proxy(proxies):
    return random.choice(proxies)


# Build proxy string for noble_tls
def get_proxy_headers(proxy):
    proxy_url = f"http://{proxy['user']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
    return {"http_proxy": proxy_url, "https_proxy": proxy_url}


# Fetch LinkedIn company data
async def fetch_company_data(url, proxies):
    proxy = get_random_proxy(proxies)
    for attempt in range(2):
        try:
            session = noble_tls.Session(
                client=Client.CHROME_131,
                random_tls_extension_order=True
            )
            getUrl = url
            if "https" not in url:
                getUrl = url.replace("http", "https")
            response = await session.get(getUrl, headers=HEADERS, proxy=get_proxy_headers(proxy))

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            if "followerCount" not in response.text:
                raise Exception("No followerCount found. Invalid response or login required.")

            print(f"Request successful for {url} with proxy {proxy['ip']}")

            # Extract data
            try:
                companyId = response.text.split("fsd_company:")[1].split(",")[0]
                if "&" in companyId:
                    companyId = companyId.split("&")[0]
            except:
                companyId = "N/A"

            try:
                all = response.text.split("&quot;employeeCount&quot;:")
                for i in all:
                    if i[0] != "{":
                        employeeCountPart = i
                        employeeCount = i.split(",")[0]
            except:
                employeeCount = "N/A"

            if "<!DOCTYPE html>" in employeeCount:
                print("Invalid LinkedIn Profile.")
                return {
                    "url": url,
                    "company_id": "OFFLINE",
                    "followers": "OFFLINE",
                    "employeeCount": "OFFLINE",
                    "employeeCountRange": "OFFLINE",
                    "employeeCountRangeMin": "OFFLINE",
                    "employeeCountRangeMax": "OFFLINE",
                }

            try:
                employeeCountRange = response.text.split(companyId + "&quot;,&quot;employeeCountRange&quot;:{&quot;start&quot;:")[1]
                employeeCountRangeMin = employeeCountRange.split(",")[0]
                employeeCountRangeMax = employeeCountRange.split("end&quot;:")[1].split(",")[0]
            except:
                try:
                    # fallback parsing
                    raw = employeeCountPart.split("&quot;employeeCountRange&quot;:{&quot;start&quot;:")[1]
                    employeeCountRangeMin = raw.split(",")[0]
                    employeeCountRangeMax = raw.split("&quot;end&quot;:")[1]
                    employeeCountRangeMax = employeeCountRangeMax.split(",")[0]
                except:
                    employeeCountRangeMin = "N/A"
                    employeeCountRangeMax = "N/A"

            try:
                Followers = response.text.split("fs_followingInfo:urn:li:company:" + companyId)[1].split("followerCount&quot;:")[1].split(",")[0]
            except:
                Followers = "N/A"

            if "}" in Followers:
                Followers = Followers.replace("}", "")

            return {
                "url": url,
                "company_id": companyId,
                "followers": Followers,
                "employeeCount": employeeCount,
                "employeeCountRange": f"{employeeCountRangeMin}-{employeeCountRangeMax}",
                "employeeCountRangeMin": employeeCountRangeMin,
                "employeeCountRangeMax": employeeCountRangeMax,
            }
        except Exception as e:
            print(f"Proxy {proxy['ip']} failed for {url}: {e}")
            proxy = get_random_proxy(proxies)
            time.sleep(2)
    print(f"Failed to fetch data for {url} after rotating proxies.")
    return {"url": url, "error": "Failed after proxy rotation"}


# Periodically save results to CSV
async def periodic_save(file_path):
    while True:
        await asyncio.sleep(SAVE_INTERVAL)
        with results_lock:
            write_results_to_csv(results, file_path)
        print(f"Results saved to {file_path}")


# Process LinkedIn URLs
async def process_urls(urls, proxies):
    sem = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    async def fetch_with_semaphore(url):
        async with sem:
            result = await fetch_company_data(url, proxies)
            with results_lock:
                results.append(result)
            time.sleep(1)

    tasks = [fetch_with_semaphore(url) for url in urls]
    await asyncio.gather(*tasks)


# Write results to CSV
def write_results_to_csv(results, file_path):
    with open(file_path, "w", newline="") as csvfile:
        fieldnames = ["url", "company_id", "followers", "employeeCount", "employeeCountRange", "employeeCountRangeMin", "employeeCountRangeMax", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)


# Main function
async def main():
    print("Loading proxies...")
    proxies = load_proxies(PROXY_FILE)

    print("Reading LinkedIn URLs...")
    urls = []
    with open(CSV_INPUT_FILE, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[21] != "":
                if "http" not in row[21]:
                    continue
                url = row[21]
                urls.append(url)

    print(f"Processing {len(urls)} URLs with {len(proxies)} proxies...")
    save_task = asyncio.create_task(periodic_save(CSV_OUTPUT_FILE))
    await process_urls(urls, proxies)
    save_task.cancel()
    with results_lock:
        write_results_to_csv(results, CSV_OUTPUT_FILE)
    print("Finished.")

asyncio.run(main())