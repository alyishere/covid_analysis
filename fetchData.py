def nytData():    
    import requests

    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    response = requests.get(url)

    with open('us-counties.csv', 'wb') as f:
        f.write(response.content)