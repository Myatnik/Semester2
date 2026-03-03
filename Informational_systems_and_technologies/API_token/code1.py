from my_token import my_token as token
from apify_client import ApifyClient

client = ApifyClient(token)

game1 = "https://store.steampowered.com/app/312520/Rain_World/"
game2 = "https://store.steampowered.com/app/1150690/OMORI/" #might implement getting list of games and interface later

params = {
    "startUrl": game2,
    "maxConcurrency": 5,
    "onlyOnSale": False,
    "onlyReleased": False,
    "maxResults": 50, #originally set to 100, i dunno if it speeds up search or not,
    "proxyConfiguration": #but since incoming JSON is unsorted and games come at random setting this to 1 wont do anything good (i tried)
    {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"]
    }
}

run = client.actor("shahidirfan/steam-store-scraper").call(run_input=params)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    
    if item.get('isDLC') == True or "soundtrack" in item.get('title').lower():
        continue #sorting out DLCs and soundtracks
    
    print("---")
    print(f"Name: {item.get('title')}")
    print(f"Price: {item.get('price')}")
    if 'salePercentage' in item:
        print(f"Discount: {item.get('salePercentage')}")
#
# holy shit its 2AM i spent like 4 hours on this one