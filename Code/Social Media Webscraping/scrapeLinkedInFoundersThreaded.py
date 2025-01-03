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
CSV_INPUT_FILE = "../../Datasets/Aggregated Sets/founders_with_links.csv"  # Input CSV file with LinkedIn URLs
CSV_OUTPUT_FILE = "Results/LinkedIn/Founders/founders_linkedin.csv"  # Output CSV file for results
MAX_CONCURRENT_TASKS = 1  # Number of concurrent tasks
SAVE_INTERVAL = 10  # Save results every 10 seconds

HEADERS = {
    "sec-ch-ua-platform": "\"macOS\"",
    "x-li-track": "{\"clientVersion\":\"1.13.28248.2\",\"mpVersion\":\"1.13.28248.2\",\"osName\":\"web\",\"timezoneOffset\":1,\"timezone\":\"Europe/Berlin\",\"deviceFormFactor\":\"DESKTOP\",\"mpName\":\"voyager-web\",\"displayDensity\":1,\"displayWidth\":2560,\"displayHeight\":1440}",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "csrf-token": "ajax:5152424158188856001",
    "sec-ch-ua-mobile": "?0",
    "x-restli-protocol-version": "2.0.0",
    "x-li-page-instance": "urn:li:page:d_flagship3_profile_view_base;sXCd/IC3QxCDRW6hH0f6rA==",
    "x-li-lang": "de_DE",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "accept": "application/vnd.linkedin.normalized+json+2.1",
    "x-li-pem-metadata": "Voyager - Profile=profile-top-card-supplementary",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.linkedin.com/in/nstoronsky/?originalSubdomain=uk",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i",
    "cookie": """bcookie="v=2&ee10d884-c977-4861-80f2-d7d1a9a45245"; li_gc=MTswOzE3MjQ5NDgzNDg7MjswMjEoYapxl+tQulIVGdD+3g8bVog7aJIWIKGcEPEqi/gYtw==; JSESSIONID=ajax:5152424158188856001; lang=v=2&lang=en-us; bscookie="v=1&202412301620380080bda9-227f-4265-85ff-ac8473e83362AQHrcn1OQn3l17qlSV6sNmi5VJGp9U-O"; li_alerts=e30=; g_state={"i_l":0}; liap=true; li_at=AQEDAVYul0gAOvDrAAABlBhfAkYAAAGUPGuGRk0AaWZs14F6LyQL2MZvCHcEGUIG0nF5gMALUJBRYz4vAJF82hzFku7XebsgPzQFbDWwtmWfAoKp3HmyIOqS2DTSDX8DcdaHgcxt8-jzBFpHkon-Yrte; timezone=Europe/Berlin; li_theme=light; li_theme_set=app; dfpfpt=1751713f20f7411e9b9593a38ba40b4c; fid=AQF_nZos_h1I7gAAAZQnID_-5OqF86Mt3wodQ0kBikRTXooSYk6H7TIErxYiMg9RTcNHLGwhuzjaKQ; li_mc=MTswOzE3MzU4MjMyMTI7MjswMjGBfRMw6PUHirD27+dePmfC5xPAF8tkKVVl4piEHxFBzw==; lidc="b=TB60:s=T:r=T:a=T:p=T:g=4034:u=1:x=1:i=1735823212:t=1735836150:v=2:sig=AQG1SOqRtfULLdB9anIg5fwObZ-MLXdH"; __cf_bm=6pcYrpjMPFxynDGal_I2dzk6iBr000g98QN3Uv.vobM-1735823212-1.0.1.1-JN52t3HMb_.ZzCuLP4K3l2xSjyFEM32Z5IZnCJ3cx04kJaId.tst1MY9fMy6KqonF4oZ.GHa4CpT_BIJDG_uRQ; fptctx2=taBcrIH61PuCVH7eNCyH0LNKRXFdWqLJ6b8ywJyet7W1QRukDDR8%252fOqtKlU9HCLjoBMn40CO1h0DRtZGGoKfEnByfFt3AUYl79Yql4pgIv2%252brMynw8ZYQ1fiad66gZ2Lh4VFlxY2vp6phuZ0qSOUqDrSiPbnLZ3lr%252bG2pAwFluVbxQH9Y32zp1y77vSVoSKmHuNqBmxwAqTxP1l%252b9rawBU54oysKPlPUEDx3zPypZ3a3Swipim0VdbP%252fNYLI%252ffC5ZmNRPb6viIQxtdedY28h14wMe02YoMazwuAxrseHi%252bEgWUdxpPpswFIMSMgGTBwTEKkXjZbgx6dJ%252frXAjSeNDfz8cI1pusRlqyJPoMrM094%253d"""
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
    return proxy_url


# Fetch LinkedIn company data
async def fetch_company_data(url, proxies):
    proxy = get_random_proxy(proxies)
    for attempt in range(2):
        try:
            session = noble_tls.Session(
                client=Client.CHROME_131,
                random_tls_extension_order=True
            )
            if "/in/" not in url:
                raise Exception("Invalid Profile Link.")

            username = url.split("/in/")[1]
            if "/" in username:
                username = username.split("/")[0]

            getUrl = "https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(vanityName:"+username+")&queryId=voyagerIdentityDashProfiles.006f9921d016ba6bbed83dcb9e8bcab8"
            response = await session.get(getUrl, headers=HEADERS, proxy=get_proxy_headers(proxy))

            #print(response.status_code, response.text)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            if "followerCount" not in response.text:
                raise Exception("No followerCount found. Invalid response or login required.")

            print(f"Request successful for {url} with proxy {proxy['ip']}")

            # Extract data

            profileId = response.text.split('"*elements":["')[1].split('"],')[0]

            try:
                connections = response.text.split('"connections":{"paging"')[1].split('"total":')[1].split(",")[0]
            except:
                connections = "N/A"

            try:
                Followers = response.text.split('","followerCount":')[1].split(",")[0]
            except:
                Followers = "N/A"

            if "}" in Followers:
                Followers = Followers.replace("}", "")

            return {
                "url": url,
                "username": username,
                "followers": Followers,
                "connections": connections,
                "profileId": profileId
            }
        except Exception as e:
            print(f"Proxy {proxy['ip']} failed for {url}: {e}")
            proxy = get_random_proxy(proxies)
            time.sleep(2)
    print(f"Failed to fetch data for {url} after rotating proxies.")
    return {"url": url, "error": "Failed after proxy rotation"}

async def fetch_education(url, profileId, proxies):
    proxy = get_random_proxy(proxies)
    for attempt in range(2):
        try:
            session = noble_tls.Session(
                client=Client.CHROME_131,
                random_tls_extension_order=True
            )
            if "/in/" not in url:
                raise Exception("Invalid Profile Link.")

            getUrl = "https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:"+profileId.replace(":", "%3A")+")&queryId=voyagerIdentityDashProfileCards.d34fc34cd086009bd15b6768ac1a100e"
            response = await session.get(getUrl, headers=HEADERS, proxy=get_proxy_headers(proxy))
            #print(getUrl)
            #print(response.status_code, response.text)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            if "followerCount" not in response.text:
                raise Exception("No followerCount found. Invalid response or login required.")

            print(f"2. Request successful for {url} with proxy {proxy['ip']}")

            # Extract data
            degree1 = ""
            degree2 = ""
            degree1_university = ""
            degree2_university = ""
            try:
                #raw = response.text.split('"text":"Ausbildung"')[1].split('"fixedListComponent":{')[1]
                raw = response.text.split('"text":"Ausbildung"')[1].split('"profileContentCollectionsComponent":null')[1]
                # loop through objects
                objects = raw.split('"components":{')
                for i in objects:
                    #print(i)
                    if "titleV2" not in i:
                        continue
                    try:
                        # get title of education (usually university name)
                        university = i.split("titleV2")[1].split('"text":"')[1].split('"')[0]
                    except Exception as e:
                        #print("uni", e)
                        university = ""
                    #print(university)
                    try:
                        # get subtitle (usually degree name)
                        subtitle = i.split("titleV2")[1].split('"subtitle":{')[1].split('"text":"')[1].split('"')[0]
                    except Exception as e:
                        #print("subtitle", e)
                        subtitle = ""
                    #print(subtitle)
                    #print(university, subtitle)
                    if degree1 == "":
                        degree1 = subtitle
                    elif degree2 == "":
                        degree2 = subtitle
                    if degree1_university == "":
                        degree1_university = university
                    elif degree2_university == "":
                        degree2_university = university
            except:
                print("Failed parsing degrees. Assuming no degrees.")
                return {
                    "degree_1": "",
                    "degree_1_university": "",
                    "degree_2": "",
                    "degree_2_university": "",
                }
            return {
                "degree_1": degree1,
                "degree_1_university": degree1_university,
                "degree_2": degree2,
                "degree_2_university": degree2_university,
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
            try:
                if result["profileId"] != "":
                    education = await fetch_education(url, result["profileId"], proxies)
                    if education["degree_1_university"] != "":
                        result["degree_1"] = education["degree_1"]
                        result["degree_1_university"] = education["degree_1_university"]
                        result["degree_2"] = education["degree_2"]
                        result["degree_2_university"] = education["degree_2_university"]
                del result["profileId"]
            except:
                pass
            print(result)
            with results_lock:
                results.append(result)
            time.sleep(1)

    tasks = [fetch_with_semaphore(url) for url in urls]
    await asyncio.gather(*tasks)


# Write results to CSV
def write_results_to_csv(results, file_path):
    with open(file_path, "w", newline="") as csvfile:
        fieldnames = ["url", "username", "followers", "connections", "degree_1", "degree_1_university", "degree_2", "degree_2_university", "error"]
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
            if row[6] != "":
                if "http" not in row[6]:
                    continue
                url = row[6]
                urls.append(url)

    print(f"Processing {len(urls)} URLs with {len(proxies)} proxies...")
    save_task = asyncio.create_task(periodic_save(CSV_OUTPUT_FILE))
    await process_urls(urls, proxies)
    save_task.cancel()
    with results_lock:
        write_results_to_csv(results, CSV_OUTPUT_FILE)
    print("Finished.")

asyncio.run(main())