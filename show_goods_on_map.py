#!/usr/bin/env python3
import sqlite3
import pandas as pd
from flask import render_template
import flask
import config

db_url = 'file:' + config.db_file + '?mode=ro'                              # build database file url
airport_icao = config.airport_icao

# Get airports list from sqlite database
def get_airports_list():
    db = sqlite3.connect(db_url, uri=True)
    airports_df = pd.read_sql_query("select * from airport;", db)           # get data from sqlite database
    db.close()

    df = airports_df[['ident','lonx','laty']]                               # get only columns: ident, lonx, laty
    df = df.rename(columns={'ident':'icao'})                                # rename column ident to icao
    df.set_index('icao', inplace=True)                                      # set column icao as index

    return df

def get_search_airport_lat_lng(airport_icao, all_airports):
    map_center_coords_df_row = all_airports.loc[airport_icao]
    map_center_lat = map_center_coords_df_row['laty']
    map_center_lng = map_center_coords_df_row['lonx']

    return (map_center_lat, map_center_lng)

# Get goodsMarket list from sqlite database
def get_airports_that_trade(good):
    db = sqlite3.connect(db_url, uri=True)
    goodsMarket_df = pd.read_sql_query("select * from goodsMarket;", db)    # get data from sqlite database
    db.close()
   
    df = goodsMarket_df[goodsMarket_df['name'] == good]
    df = df[['location','unitprice','quantity','tradetype']]                # get only columns: location, unitprice, quantity, tradetype
    df = df.rename(columns={'location':'icao'})                             # rename column location to icao
    df.set_index('icao', inplace=True)                                      # set column icao as index
    
    return df


if __name__ == "__main__":
    good = config.good
    all_airports = get_airports_list()                                      # call function to retrieve full airport list (for lat/long information)
    airports_with_good = get_airports_that_trade(good)               # call function to retrieve list of airports trading selected good
    
    airports_with_good = pd.merge(airports_with_good, all_airports, how="left", on="icao")  # merge dataframes to get list of airports with lat/long
    airports_list = airports_with_good.reset_index().to_dict('records')     # convert dataframe to list of dicts (for easy flask usage)

    #for airport in airports_list:                                           # print list to terminal
    #    print(airport)

    map_center_coords = get_search_airport_lat_lng(airport_icao, all_airports)
    map_center_lat, map_center_lng = map_center_coords

    print(good + " is being traded at " + str(len(airports_list)) + " known airports" ) # print status

    app = flask.Flask('my app')
    with app.app_context():                                                 # generate index.html with flask
        rendered = render_template('map.html', \
            bingkey = config.bingkey,
            map_center_lat = map_center_lat,
            map_center_lng = map_center_lng,
            zoom_level = config.zoom_level,
            airports = airports_list, )

        file = open("index.html", 'w', encoding="utf-8")
        file.write(rendered)
        file.close
