#!/usr/bin/env python3
import uiautomation as auto
import time
import sqlite3
import pandas as pd
import config

db_url = 'file:' + config.db_file + '?mode=ro'                              # build database file url
neofly_window_name = config.neofly_window_name

# Get airports list from sqlite database
def get_airports_list():
    db = sqlite3.connect(db_url, uri=True)
    airports_df = pd.read_sql_query("select * from airport;", db)
    db.close()

    airports = []
    for airport in airports_df['ident']:
        if airport.startswith("LE") or airport.startswith("LP"):     # !! currently hardcoded airports to scan = "LE.." + "LP.."
            airports.append(airport)

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
    market_radius.SendKeys("5")

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

        time.sleep(0.1)


if __name__ == "__main__":
    airports = get_airports_list()
    airports = airports[0:3]   # uncomment for testing purposes (= limit number of queries)
    scan_markets(airports)