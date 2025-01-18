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

# First Step: check already processed urls
alreadyDone = []
with open(CSV_OUTPUT_FILE, "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # print(row[0])
        if row[0] != "":
            if "http" not in row[0]:
                continue
            alreadyDone.append(row[0])

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
    # url = "https://www.linkedin.com/in/mituca/"
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

            getUrl = "https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(vanityName:" + username + ")&queryId=voyagerIdentityDashProfiles.006f9921d016ba6bbed83dcb9e8bcab8"
            response = await session.get(getUrl, headers=HEADERS, proxy=get_proxy_headers(proxy))

            # print("1", response.status_code, response.text)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            if "followerCount" not in response.text:
                raise Exception("No followerCount found. Invalid response or login required.")

            print(f"Request successful for {url} with proxy {proxy['ip']}")

            # Extract data

            profileId = response.text.split('"*elements":["')[1].split('"],')[0]

            try:
                headline = \
                response.text.split(profileId + '","companyNameOnProfileTopCardShown"')[1].split(',"headline":"')[
                    1].split('","')[0]
            except:
                headline = ""
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
                "profileId": profileId,
                "headline": headline
            }
        except Exception as e:
            print(f"Proxy {proxy['ip']} failed for {url}: {e}")
            proxy = get_random_proxy(proxies)
            time.sleep(2)
    print(f"Failed to fetch data for {url} after rotating proxies.")
    return {"url": url, "error": "Failed after proxy rotation"}


def has_multiple_entries(entity_component):
    """
    Checks if a job entry has multiple sub-entries (sub-roles).

    Args:
        entity_component (dict): The entity component of a job.

    Returns:
        bool: True if multiple entries exist, False otherwise.
    """
    if not entity_component or not isinstance(entity_component, dict):
        return False

    try:
        # Access subComponents
        sub_components = entity_component.get("subComponents", {}).get("components", [])
        if not isinstance(sub_components, list) or len(sub_components) <= 1:
            return False

        FoundFirstTitle = False
        # Check if subComponents have meaningful job-related data
        for sub_component in sub_components:
            title = sub_component.get("components", {}).get("entityComponent", {}).get("titleV2", {}).get("text",
                                                                                                          {}).get(
                "text", "")
            if title and FoundFirstTitle:
                return True  # Valid multiple entries found
            FoundFirstTitle = True
            fixed_list_component = sub_component.get("components", {}).get("fixedListComponent", {})
            if fixed_list_component:
                # print(fixed_list_component)
                # Validate the fixedListComponent contains entityComponents
                components = fixed_list_component.get("components", [])
                for component in components:
                    entity = component.get("components", {}).get("entityComponent", {})
                    if entity and isinstance(entity, dict):
                        return True  # Valid multiple entries found
    except Exception as e:
        # print("Error checking for multiple entries:", e)
        pass

    return False


def parse_linkedin_jobs(data):
    jobs = []
    try:
        # Traverse the JSON to find job-related components
        included_items = data.get("included", [])
        for item in included_items:
            top_components = item.get("topComponents", [])
            if "Berufserfahrung" not in str(top_components):
                # print("No Berufserfahrung found.")
                continue
            for top_component in top_components:

                # Loop through components to find the first valid fixedListComponent
                components = top_component.get("components", {}).values()
                for component in components:
                    if component == None:
                        continue

                    # Process job components inside fixedListComponent
                    job_components = component.get("components", [])
                    for job in job_components:
                        # Extract job details
                        entity_component = job.get("components", {}).get("entityComponent", {})
                        multipleEntries = False
                        if has_multiple_entries(entity_component):
                            # Handle logic for multiple entries
                            multipleEntries = True
                        try:
                            if multipleEntries:
                                # multiple entries
                                for entry in entity_component["subComponents"]["components"]:
                                    title = entry.get("components", {}).get("entityComponent", {}).get("titleV2",
                                                                                                       {}).get("text",
                                                                                                               {}).get(
                                        "text", "")
                                    company = entity_component.get("titleV2", {}).get("text", {}).get("text", "")
                                    try:
                                        duration = entry.get("components", {}).get("entityComponent", {}).get("caption",
                                                                                                              {}).get(
                                            "text", "")
                                    except:
                                        duration = ""
                                    try:
                                        location = entry.get("components", {}).get("entityComponent", {}).get(
                                            "metadata", {}).get("text", "")
                                    except:
                                        location = ""
                                    # Extract job description if available
                                    description = ""
                                    # Extract sub-components for description
                                    try:
                                        sub_components = entry.get("components", {}).get("entityComponent", {}).get(
                                            "subComponents", {}).get("components", [])
                                        for sub_component in sub_components:
                                            fixed_list_component = sub_component.get("components", {}).get(
                                                "fixedListComponent", {})
                                            if not fixed_list_component:
                                                continue

                                            # Navigate to textComponent for the description
                                            description_components = fixed_list_component.get("components", [])
                                            for desc_component in description_components:
                                                text_component = desc_component.get("components", {}).get(
                                                    "textComponent", {})
                                                description = text_component.get("text", {}).get("text", "")
                                    except Exception as e:
                                        pass

                                    # Add to jobs list
                                    jobs.append({
                                        "title": title,
                                        "company": company,
                                        "duration": duration,
                                        "description": description,
                                        "location": location
                                    })
                            else:
                                title = entity_component.get("titleV2", {}).get("text", {}).get("text", "")
                                company = entity_component.get("subtitle", {}).get("text", "")
                                try:
                                    duration = entity_component.get("caption", {}).get("text", "")
                                except:
                                    duration = ""
                                try:
                                    location = entity_component.get("metadata", {}).get("text", "")
                                except:
                                    location = ""
                                # Extract job description if available
                                description = ""
                                # Extract sub-components for description
                                try:
                                    sub_components = entity_component.get("subComponents", {}).get("components", [])
                                    for sub_component in sub_components:
                                        fixed_list_component = sub_component.get("components", {}).get(
                                            "fixedListComponent", {})
                                        if not fixed_list_component:
                                            continue

                                        # Navigate to textComponent for the description
                                        description_components = fixed_list_component.get("components", [])
                                        for desc_component in description_components:
                                            text_component = desc_component.get("components", {}).get("textComponent",
                                                                                                      {})
                                            description = text_component.get("text", {}).get("text", "")
                                except Exception as e:
                                    pass

                                # Add to jobs list
                                jobs.append({
                                    "title": title,
                                    "company": company,
                                    "duration": duration,
                                    "description": description,
                                    "location": location
                                })
                        except Exception as e:
                            print(f"Error parsing job: {e}")
                            continue
    except AttributeError as e:
        print(f"Error parsing JSON structure: {e}")
    return jobs


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

            getUrl = "https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:" + profileId.replace(
                ":", "%3A") + ")&queryId=voyagerIdentityDashProfileCards.d34fc34cd086009bd15b6768ac1a100e"

            response = await session.get(getUrl, headers=HEADERS, proxy=get_proxy_headers(proxy))
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")

            if "followerCount" not in response.text:
                raise Exception("No followerCount found. Invalid response or login required.")

            print(f"2. Request successful for {url} with proxy {proxy['ip']}")

            jsondata = response.json()

            # parse job history
            parsed_jobs = parse_linkedin_jobs(jsondata)

            # Extract data
            degree1 = ""
            degree2 = ""
            degree1_university = ""
            degree2_university = ""
            degree1_duration = ""
            degree2_duration = ""
            try:
                raw = response.text.split('"text":"Ausbildung"')[1].split('"profileContentCollectionsComponent":null')[
                    1]
                # loop through objects
                objects = raw.split('"components":{')
                for i in objects:
                    if "titleV2" not in i:
                        continue
                    try:
                        # get duration
                        duration = i.split("caption")[1].split('"text":"')[1].split('"')[0]
                    except Exception as e:
                        duration = ""
                    try:
                        # get title of education (usually university name)
                        university = i.split("titleV2")[1].split('"text":"')[1].split('"')[0]
                    except Exception as e:
                        university = ""
                    try:
                        # get subtitle
                        subtitle = i.split("titleV2")[1].split('"subtitle":{')[1].split('"text":"')[1].split('"')[0]
                    except Exception as e:
                        subtitle = ""

                    if degree1 == "":
                        degree1 = subtitle
                    elif degree2 == "":
                        degree2 = subtitle
                    if degree1_university == "":
                        degree1_university = university
                    elif degree2_university == "":
                        degree2_university = university
                    if degree1_duration == "":
                        degree1_duration = duration
                    elif degree2_duration == "":
                        degree2_duration = duration
            except:
                print("Failed parsing degrees. Assuming no degrees.")

            result = {
                "degree_1": degree1,
                "degree_1_university": degree1_university,
                "degree_1_duration": degree1_duration,
                "degree_2": degree2,
                "degree_2_university": degree2_university,
                "degree_2_duration": degree2_duration,
            }
            # Add up to 5 jobs to the result
            for i, job in enumerate(parsed_jobs[:10]):
                result[f"job_title_{i + 1}"] = job["title"]
                result[f"job_company_{i + 1}"] = job["company"]
                result[f"job_duration_{i + 1}"] = job["duration"]
                result[f"job_location_{i + 1}"] = job["location"]
                result[f"job_description_{i + 1}"] = job["description"]

            return result
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
                        result["degree_1_duration"] = education["degree_1_duration"]
                        result["degree_2"] = education["degree_2"]
                        result["degree_2_university"] = education["degree_2_university"]
                        result["degree_2_duration"] = education["degree_2_duration"]
                    try:
                        for i in range(1, 11):
                            result[f"job_title_{i}"] = education[f"job_title_{i}"]
                            result[f"job_company_{i}"] = education[f"job_company_{i}"]
                            result[f"job_duration_{i}"] = education[f"job_duration_{i}"]
                            result[f"job_location_{i}"] = education[f"job_location_{i}"]
                            result[f"job_description_{i}"] = education[f"job_description_{i}"]
                    except:
                        pass
                del result["profileId"]
            except:
                pass
            print(result)
            with results_lock:
                results.append(result)
            time.sleep(0.3)

    tasks = [fetch_with_semaphore(url) for url in urls]
    await asyncio.gather(*tasks)


# Write results to CSV
def write_results_to_csv(results, file_path):
    with open(file_path, "a", newline="") as csvfile:
        fieldnames = ["url", "username", "followers", "connections", "headline", "degree_1", "degree_1_university",
                      "degree_1_duration", "degree_2", "degree_2_university", "degree_2_duration", "job_title_1",
                      "job_company_1", "job_duration_1", "job_location_1", "job_description_1",
                      "job_title_2", "job_company_2", "job_duration_2", "job_location_2", "job_description_2",
                      "job_title_3", "job_company_3", "job_duration_3", "job_location_3", "job_description_3",
                      "job_title_4", "job_company_4", "job_duration_4", "job_location_4", "job_description_4",
                      "job_title_5", "job_company_5", "job_duration_5", "job_location_5", "job_description_5",
                      "job_title_6", "job_company_6", "job_duration_6", "job_location_6", "job_description_6",
                      "job_title_7", "job_company_7", "job_duration_7", "job_location_7", "job_description_7",
                      "job_title_8", "job_company_8", "job_duration_8", "job_location_8", "job_description_8",
                      "job_title_9", "job_company_9", "job_duration_9", "job_location_9", "job_description_9",
                      "job_title_10", "job_company_10", "job_duration_10", "job_location_10", "job_description_10",
                      "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        for result in results:
            if result["url"] not in alreadyDone:  # Check for duplicates
                writer.writerow(result)
                alreadyDone.append(result["url"])  # Mark as written


# Main function
async def main():
    print("Loading proxies...")
    proxies = load_proxies(PROXY_FILE)

    # Read the CSV and remove duplicates
    unique_rows = []
    seen = set()

    with open(CSV_OUTPUT_FILE, "r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            # Convert the row to a tuple (because lists are not hashable) and check for duplicates
            row_tuple = tuple(row)
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_rows.append(row)

    # Write the unique rows back to a new CSV file
    with open(CSV_OUTPUT_FILE, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(unique_rows)

    print(f"Removed duplicates. Unique rows written to {CSV_OUTPUT_FILE}.")

    print("Reading LinkedIn URLs...")
    urls = []
    with open(CSV_INPUT_FILE, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[6] != "":
                if "http" not in row[6]:
                    continue
                if row[6] in alreadyDone:
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
