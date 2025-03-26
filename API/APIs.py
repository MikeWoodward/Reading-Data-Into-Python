import requests
import keyring as kr
import tldextract


def get_search_matches(*,
                       token: str,
                       pattern: str) -> None | dict:
    """
    Function to get all permid matches to pattern.

    Args:
        token (str): the access token
        pattern (str): the search pattern

    Returns:
        The pattern matches (if any) in dict,
        None if no matches or an error.
    """

    search_url = "https://api-eit.refinitiv.com:443/permid/search?"
    try:
        response = requests.get(
            search_url,
            headers={'access-token': token},
            params={'q': pattern,
                    "entityType": 'organization'},
            timeout=(5, 5)
        )
    except requests.Timeout:
        print("""Timeout error.""")
        return None
    except requests.exceptions.ConnectionError as err:
        print(f"""ConnectionError {err}""")
        return None
    except requests.RequestException as err:
        print(f"""RequestException {err}""")
        return None

    if response.status_code != 200:
        print(f"Reponse code is {response.status_code}")
        return None

    return response.json()


def get_company_match(*,
                      token: str,
                      permid_url: str) -> dict:
    """
    Function to get company data from a PermId url.

    Args:
        token (str): the access token
        permid_url (str): the PermId url pattern

    Returns:
        The company data (if any) in dict,
        None if no matches or an error.
    """
    try:
        response = requests.get(
            permid_url,
            params={'format': 'json-ld'},
            headers={'access-token': token},
            timeout=(5, 5)
        )
    except requests.Timeout:
        print("""Timeout error.""")
        return None
    except requests.exceptions.ConnectionError as err:
        print(f"""ConnectionError {err}""")
        return None
    except requests.RequestException as err:
        print(f"""RequestException {err}""")
        return None

    if response.status_code != 200:
        print(f"Reponse code is {response.status_code}")
        return None

    return response.json()

# %%
token = kr.get_password("PermId",
                        "YOUR-EMAIL")

# Get all smiths companies
companies_json = get_search_matches(token=token,
                                    pattern="smiths")

# %%
# Locate the right smiths
permid_url = None
for company in (companies_json
                ['result']
                ['organizations']
                ['entities']):
    if ('hasURL' in company
        and (tldextract
             .extract(company['hasURL'])
             .registered_domain) == 'smiths.com'):
        print("High level company info")
        print("=======================")
        print(f"Name: {company['organizationName']}")
        print(f"Ticker: {company['primaryTicker']}")
        print(f"Type: {company['hasHoldingClassification']}")
        print(f"PermId: {company['@id']}")    
        permid_url = company['@id']
        
# %%
# Get more data on the right smiths   
if permid_url:
    if (company
        := get_company_match(token=token,
                             permid_url=permid_url)):
        print("Detailed company info")
        print("=====================")
        print("""Address: """
              f"""{company['mdaas:HeadquartersAddress']}""")
        print("""Phone: """
              f"""{company['tr-org:hasHeadquartersPhoneNumber']}""")
        print("""IPO date: """
              f"""{company['hasIPODate']}""")
        print("""LEI: """
              f"""{company['tr-org:hasLEI']}""")
