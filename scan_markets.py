#!/usr/bin/env python3
import uiautomation as auto
import time
import sqlite3
import pandas as pd
import config
import geopy.distance

db_url = 'file:' + config.db_file + '?mode=ro'                              # build database file url
neofly_window_name = config.neofly_window_name

airport_icao = config.airport_icao              # new, with radius
scan_radius = config.scan_radius

# Get airports list from sqlite database
def get_airports_list():
    db = sqlite3.connect(db_url, uri=True)
    airports_df = pd.read_sql_query("select * from airport;", db)
    db.close()
    
    df = airports_df[['ident','lonx','laty']]
    df = df.rename(columns={'ident':'icao'})
    df.set_index('icao', inplace=True)

    print("Generating list of all airports " + str(scan_radius) + " NM around " + airport_icao)
    search_around_airport = df.loc[airport_icao]
    search_around_airport_coords = (search_around_airport['laty'], search_around_airport['lonx'])

    airports = []                                   
    for index, row in df.iterrows():
        airport_coords = (row['laty'],row['lonx'])
        distance = geopy.distance.distance(airport_coords, search_around_airport_coords).nm
        
        if distance <= scan_radius:
            airports.append(index)

    return airports



# Scan markets by querying the NeoFly gui
def scan_markets(airports):
    total_airports = len(airports)
    print("Scanning " + str(total_airports) + " airports:")
    neowin = auto.WindowControl(searchDepth=1, Name=neofly_window_name)
    neowin.SetActive()

    # Access market tab
    market_tab = neowin.Control(searchDepth=1, AutomationId='btn_Trading')
    market_tab.Click(simulateMove=True)

    # Set radius to 5
    market_radius = neowin.EditControl(Depth=1, foundIndex=16)
    market_radius.SendKeys('{Ctrl}a{Del}')
    market_radius.SendKeys("1")

    # scanning each market from list
    for index, airport in enumerate(airports):
        print('\r' + str(index+1) + " of " + str(total_airports), end='', flush=True )
        # Enter ICAO
        market_ICAO = neowin.Control(searchDepth=1, AutomationId='textSerachICAOMarket')
        market_ICAO.SendKeys('{Ctrl}a{Del}')
        market_ICAO.SendKeys(airport)

        # Execute search
        market_search_btn = neowin.ButtonControl(Depth=1, foundIndex=21)
        market_search_btn.Click(simulateMove=True)

        #time.sleep(0.1)


if __name__ == "__main__":
    airports = get_airports_list()
    
    #airports = airports[0:3]   # uncomment for testing purposes (= limit number of queries)
    #print(airports)
     
    scan_markets(airports)