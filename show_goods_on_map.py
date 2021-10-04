#!/usr/bin/env python3
import sqlite3
import pandas as pd
from flask import render_template
import flask
import config

db_url = 'file:' + config.db_file + '?mode=ro'                              # build database file url


# Get airports list from sqlite database
def get_airports_list():
    db = sqlite3.connect(db_url, uri=True)
    airports_df = pd.read_sql_query("select * from airport;", db)           # get data from sqlite database
    db.close()

    df = airports_df[['ident','lonx','laty']]                               # get only columns: ident, lonx, laty
    df = df.rename(columns={'ident':'icao'})                                # rename column ident to icao
    df.set_index('icao', inplace=True)                                      # set column icao as index

    return df


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
    all_airports = get_airports_list()                                      # call function to retrieve full airport list (for lat/long information)
    airports_with_good = get_airports_that_trade(config.good)               # call function to retrieve list of airports trading selected good
    
    airports_with_good = pd.merge(airports_with_good, all_airports, how="left", on="icao")  # merge dataframes to get list of airports with lat/long
    airports_list = airports_with_good.reset_index().to_dict('records')     # convert dataframe to list of dicts (for easy flask usage)

    for airport in airports_list:                                           # print to list terminal
        print(airport)

    app = flask.Flask('my app')
    with app.app_context():                                                 # generate index.html with flask
        rendered = render_template('map.html', \
            bingkey = config.bingkey,
            map_center_lat = config.map_center_lat,
            map_center_lng = config.map_center_lng,
            zoom_level = config.zoom_level,
            airports = airports_list, )

        file = open("index.html", 'w', encoding="utf-8")
        file.write(rendered)
        file.close
