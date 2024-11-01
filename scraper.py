from bs4 import BeautifulSoup
import requests
import random
import webbrowser
import pyautogui
import pyperclip
import sys
import json
import time
import re

def main(address):
    # address = "750 Rue des Sureaux, Boucherville, QC, Canada" # realtor/centris
    # address = "815 Rue de Châteauguay, Boucherville, QC, Canada" #duproprio
    address_parsed = None
    query_info = None
    property = None
    # parsing de l'adresse
    address_parsed = address_parser(address)

    # trouve le listing de la propriete
    if address_parsed:
        query_info = find_property(address_parsed)
    else:
        print("address null")
        return None

    # trouve les infos de la propriete
    if query_info:
        property = get_property_info(query_info)
    else:
        print("query info null")
        return None

    if property:
        print("\nPROPERTY INFOS")
        print(property)
        return None
    print("property null")
    return None

def get_property_info(query_info):
    if query_info:
        print()
        print("PROPERTY FOUND")
        print(query_info["platform"])
        print(query_info["address"]["verbose"])
        print(query_info["url"])

        if "realtor.ca" in query_info["url"]:
            print("MLS ID: ",query_info["mls_ID"])
            print("Realtor ID: ", query_info["property_id"])
            data = get_property_realtor(query_info["property_id"], query_info["mls_ID"])
            if data:
                json_data = json.loads(data)
                formated_data = json.dumps(json_data, indent=4)
                return formated_data


        if "duproprio" in query_info["url"]:
            data = get_property_duproprio(query_info["url"])
            if data:
                formated_data = json.dumps(data, indent=4)
                return formated_data
    
    else:
        return None
def address_parser(address):
    address_dict = {}
    address_dict["verbose"] = address
  
    parts = [part.strip() for part in address.split(',')]
    
    if len(parts) == 4:
        street = parts[0]
        address_dict["city"] = parts[1]   
        address_dict["province"] = parts[2]
        address_dict["country"] = parts[3]
        
        street_parts = street.split(' ', 1)
        address_dict["street_number"] = street_parts[0]
        address_dict["street_name"] = street_parts[1] if len(street_parts) > 1 else ''
        return address_dict
    else:
        return None
     

def validate_id(property_id):
    pattern = r'^\d{7,8}$'
    if re.match(pattern, property_id) :
        return True
    return False
def validate_title(text, number):
    return str(number) in text
def get_mls_ID(results):
    for result in results:
        link_element = result.find('a')
        href_element = link_element['href']
        if "centris.ca" in href_element:
            mls_id = href_element.split('/')[-1]
            if(validate_id(mls_id)):
                return mls_id
            else:
                return None
def find_property(address):
    if address:
        query_info = {}
        query_info["address"] = address
        query_info["valide"] = False
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        ]
        
        headers = {
            "User-Agent": random.choice(user_agents)
        }

        url = f"https://www.google.com/search?q={address["street_number"]}+{address["street_name"]}+{address["city"]}+{address["province"]}+{address["country"]}+for+sale"
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the search results
            results = soup.find_all('div', class_='g')

            print()
            print("RESEARCH FOR")
            print(f'{query_info["address"]["verbose"]}')
            print()
            print('Searching ... ')

            for result in results:
                try:
                    title_element = result.find('h3')
                    title = title_element.text
                    link_element = result.find('a')
                    description_element = result.find('em')
                    description = description_element.text
                    href_element = link_element['href']

                    print(f"Title: {title}")
                    print(f"Link: {href_element}")
                    print(f"Description: {description}")
                    print()

                    if "realtor.ca" in href_element:

                        # ID
                        query_info["property_id"] = href_element.split('/')[-2]

                        # Validation
                        if(validate_id(query_info["property_id"]) or (validate_title(description, query_info["address"]["street_number"]) or validate_title(title, query_info["address"]["street_number"]))):
                            query_info["valide"] = True
                        else:
                            continue

                        # Platform
                        query_info["platform"] = "Realtor"
              
                        # url
                        query_info["url"] = href_element
                 
                        #  mls id
                        query_info["mls_ID"] = get_mls_ID(results)

                        if query_info["mls_ID"] is None:
                            return None
                
                        return query_info
                        
                    
                    if "duproprio.com" in href_element:
                        # ID
                        duproprio_ID = href_element.split('/')[-1]
                        query_info["property_id"] =  duproprio_ID.split('-')[-1]

                        # Validate
                        if(validate_id(query_info["property_id"]) or (validate_title(description, query_info["address"]["street_number"]) or validate_title(title, query_info["address"]["street_number"]))):
                            query_info["valide"] = True
                        else:
                            continue

                        # Platform
                        query_info["platform"] = "DuProprio"

                        # Link
                        query_info["url"] = href_element

                        return query_info
                    
                except Exception as e:
                    print("Error processing result:", e)
                    continue
            return None
        else:
            return None
    else:
        return None 
def get_property_duproprio(property_url):
    
    response = requests.get(property_url)

    if response.status_code == 200:
        html_content = response.text
        print()
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    
    soup = BeautifulSoup(html_content, 'html.parser')

    property_details = {}

    if 'duproprio' in property_url:
            
        rows = soup.find_all(class_='listing-box__dotted-row')
        
        for row in rows:
            columns = row.find_all('div')
            
            if len(columns) >= 2:
                label = columns[0].get_text(strip=True)
                value = columns[2].get_text(strip=True) if len(columns) > 2 else ""
                property_details[label] = value

        main_div = soup.find(class_='listing-complete-list-characteristics')

        for content_group in main_div.find_all(class_='listing-complete-list-characteristics__content__group'):
            label = content_group.find(class_='listing-complete-list-characteristics__content__group__title').text.strip(":").replace("Près des ", "")
            items = [item.text.strip() for item in content_group.find_all(class_='listing-complete-list-characteristics__content__group__item')]
            value = ', '.join(items)
            property_details[label] = value

        return property_details

    return None 
def open_browser(url):
    webbrowser.open(url)
def capture_html():
    attempts = 0
    retries = 100
    html_content = None
    # workaround ne pas cliquer sur d'autre fenetre pendant l'execution
    while not html_content and attempts < retries:
        pyperclip.copy("")
        time.sleep(0.1)
        # CTRL+A (select all)
        pyautogui.hotkey('ctrl', 'a')
        # CTRL+C (copy)
        pyautogui.hotkey('ctrl', 'c')
        html_content = pyperclip.paste()  # Get the clipboard content
        attempts += 1

    if html_content:
        return html_content
    else:
        return None
def close_browser():
    pyautogui.hotkey('ctrl', 'w')
def get_property_realtor(property_id, mls_reference_number):
    baseurl = "https://api2.realtor.ca/Listing.svc/PropertyDetails?ApplicationId=1&CultureId=1"
    url = baseurl + "&PropertyID=" + property_id + "&ReferenceNumber=" + mls_reference_number
    
    open_browser(url)
    # time.sleep(1) # browser doit etre ouvert sinon bug
    info = capture_html()
    close_browser()
    return info
def format_json(json_string):
    try:
        # Load the JSON string into a Python dictionary
        json_data = json.loads(json_string)
        
        # Convert the dictionary back to a formatted JSON string
        formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
        
        return formatted_json
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <[numero d'adresse] [nom de rue], [ville], [province], [pays]>")
        sys.exit(1)

    address = sys.argv[1]
    main(address)


