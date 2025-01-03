import asyncio
import csv
import json
import random
import re
import time
from datetime import datetime
from threading import Lock
from bs4 import BeautifulSoup
import noble_tls
from noble_tls import Client

# Constants
PROXY_FILE = "proxies.txt"  # File containing proxies
CSV_INPUT_FILE = "../../Datasets/Aggregated Sets/companies.csv"  # Input CSV file
CSV_OUTPUT_FILE = "Results/Twitter/companies_twitter.csv"  # Output CSV file for results
MAX_CONCURRENT_TASKS = 10  # Number of concurrent tasks
SAVE_INTERVAL = 5  # Save results every 10 seconds

# Global variables
results = []
results_lock = Lock()


UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
HEADERS = {
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "upgrade-insecure-requests": "1",
    "user-agent": UserAgent,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "de-DE,de;q=0.9",
    "priority": "u=1, i",
}


# Function to load proxies
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

# Function to rotate proxies
def get_random_proxy(proxies):
    return random.choice(proxies)

# Function to build proxy headers
def get_proxy_headers(proxy):
    proxy_url = f"http://{proxy['user']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}"
    return proxy_url

# Function to clean date strings
def clean_date(date_str):
    return re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str)

# Function to process data array
def process_data_array(data_string):
    try:
        data_array = json.loads(data_string)
        growth_data = {}
        for timestamp, value in data_array:
            date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
            growth_data[date] = value
        max_growth_month = max(growth_data, key=growth_data.get)
        max_growth_value = growth_data[max_growth_month]
        max_loss_month = min(growth_data, key=growth_data.get)
        max_loss_value = growth_data[max_loss_month]
        return {
            "max_growth_month": max_growth_month,
            "max_growth_value": max_growth_value,
            "max_loss_month": max_loss_month,
            "max_loss_value": max_loss_value,
        }
    except json.JSONDecodeError as e:
        print(f"Error decoding data: {e}")
        return None

# Function to fetch data
async def fetch_socialblade_data(url, proxies):
    proxy = get_random_proxy(proxies)
    for attempt in range(2):
        try:
            session = noble_tls.Session(client=Client.CHROME_131, random_tls_extension_order=True)
            username = url.split(".com/")[1]
            if "/" in username:
                username = username.split("/")[0]
            if "?" in username:
                username = username.split("?")[0]
            getUrl = "https://socialblade.com/twitter/user/"+username
            response = await session.get(getUrl, headers=HEADERS, proxy="http://pkg-lemonprime-country-DE:old6zc33df86s1z8@gw-eu.lemonclub.io:5555")
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            soup = BeautifulSoup(response.text, 'html.parser')

            print("Request Successful: 200")
            # Parse details
            followers = int(soup.find('span', text='Followers').find_next_sibling('span').text.strip().replace(",", ""))
            following = int(soup.find('span', text='Following').find_next_sibling('span').text.strip().replace(",", ""))
            tweets = int(soup.find('span', text='Tweets').find_next_sibling('span').text.strip().replace(",", ""))
            user_created = soup.find('span', text='User Created').find_next_sibling('span').text.strip()
            account_creation_date = datetime.strptime(clean_date(user_created), "%b %d, %Y")
            account_age_days = (datetime.now() - account_creation_date).days
            tweet_activity = tweets / account_age_days if account_age_days > 0 else 0

            # Regex to extract followers data
            followers_match = re.search(
                r"graph-twitter-monthly-followers-container.*?data:\s*(\[\[.*?\]\])",
                response.text,
                re.DOTALL
            )
            if followers_match:
                followers_data_string = followers_match.group(1)
                followers_stats = process_data_array(followers_data_string)
                #if followers_stats:
                    #print(
                     #   f"[FOLLOWERS] Maximum Growth in a Month: {followers_stats['max_growth_value']} followers in {followers_stats['max_growth_month']}")
                    #print(
                     #   f"[FOLLOWERS] Maximum Loss in a Month: {followers_stats['max_loss_value']} followers in {followers_stats['max_loss_month']}")
            else:
                followers_stats = {}
                followers_stats["max_growth_value"] = ""
                followers_stats["max_loss_value"] = ""

            # Regex to extract tweets data
            tweets_match = re.search(
                r"graph-twitter-monthly-tweets-container.*?data:\s*(\[\[.*?\]\])",
                response.text,
                re.DOTALL
            )
            if tweets_match:
                tweets_data_string = tweets_match.group(1)
                tweets_stats = process_data_array(tweets_data_string)
                #if tweets_stats:
                    #print(
                     #   f"[TWEETS] Maximum Growth in a Month: {tweets_stats['max_growth_value']} tweets in {tweets_stats['max_growth_month']}")
                    #print(
                     #   f"[TWEETS] Maximum Loss in a Month: {tweets_stats['max_loss_value']} tweets in {tweets_stats['max_loss_month']}")
            else:
                print("Tweet data array not found in script.")
                tweets_stats = {}
                tweets_stats["max_growth_value"] = ""
                tweets_stats["max_loss_value"] = ""

            return {
                "url": url,
                "followers": followers,
                "following": following,
                "tweets": tweets,
                "account_created": account_creation_date.strftime('%Y-%m-%d'),
                "account_age_days": account_age_days,
                "tweet_activity": round(tweet_activity, 2),
                "followers_max_growth": followers_stats['max_growth_value'],
                "followers_max_loss": followers_stats['max_loss_value'],
                "tweets_max_growth": tweets_stats['max_growth_value'],
                "tweets_max_loss": tweets_stats['max_loss_value'],
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

# Process URLs
async def process_urls(urls, proxies):
    sem = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

    async def fetch_with_semaphore(url):
        async with sem:
            result = await fetch_socialblade_data(url, proxies)
            with results_lock:
                results.append(result)
            #await time.sleep(1)

    tasks = [fetch_with_semaphore(url) for url in urls]
    await asyncio.gather(*tasks)

# Write results to CSV
def write_results_to_csv(results, file_path):
    with open(file_path, "w", newline="") as csvfile:
        fieldnames = ["url", "followers", "following", "tweets", "account_created", "account_age_days", "tweet_activity", "followers_max_growth", "followers_max_loss", "tweets_max_growth", "tweets_max_loss", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

# Main function
async def main():
    proxies = load_proxies(PROXY_FILE)

    # check already processed urls
    alreadyDone = []
    #with open(CSV_OUTPUT_FILE, "r") as csvfile:
    #    reader = csv.reader(csvfile)
    #    for row in reader:
    #        if row[0] != "":
    #            if "http" not in row[8]:
    #                continue
    #            alreadyDone.append(row[0])

    urls = []
    with open(CSV_INPUT_FILE, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[8] != "":
                if "http" not in row[8]:
                    continue
                if row[8] in alreadyDone:
                    continue
                url = row[8]
                urls.append(url)

    print(f"Processing {len(urls)} URLs with {len(proxies)} proxies...")
    save_task = asyncio.create_task(periodic_save(CSV_OUTPUT_FILE))
    await process_urls(urls, proxies)
    save_task.cancel()
    with results_lock:
        write_results_to_csv(results, CSV_OUTPUT_FILE)
    print("Finished.")

asyncio.run(main())
