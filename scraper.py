
def fetch_stats(champ): # gpm, cspm, dpm

    import requests
    from bs4 import BeautifulSoup
    import random
    
    url = f'https://www.leagueofgraphs.com/champions/stats/{champ}/diamond'
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.17.11 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    ]

    headers = {
        'User-Agent': random.choice(user_agents)
    }

    try:
        # Fetch the page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.

        # Process the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate all the relevant div boxes
        boxes = soup.find_all('div', class_='box box-padding number-only-chart text-center requireTooltip noCursor')
        
        results = {}
        metrics = {'Gold / min': 'Gold per minute', 'CS / min': 'CS per minute', 'Damage / minute': 'Damage per minute'}

        # Loop through each box to find the specified metrics
        for box in boxes:
            title = box.find('div', class_='title with-ellipsis display-block')
            if title:
                title_text = title.text.strip()
                for key, val in metrics.items():
                    if key in title_text:
                        number_div = box.find('div', class_='number solo-number')
                        if number_div:
                            number = number_div.text.strip()
                            results[val] = number
        
        if not results:
            return "No relevant data found"
        
        return results
    except requests.RequestException as e:
        return f"An error occurred: {e}"

# Running the function
result = fetch_stats('quinn')
print(result)
