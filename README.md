# neofly-market-helper

Helper scripts to assist trading in NeoFly.

## Installation
- NeoFly and Python (3.x) need to be installed
- Download neofly-market-helper either by:
  - Clicking on "Code" - "Download ZIP" above or
  - `git clone https://github.com/marcluer/neofly-market-helper.git`
- Install Python requirements:
  - `pip3 install --requirements requirements.txt`

## Configuration
- Create a `config.py` in the neofly-market-helper directory with the following contents:
  ```
  bingkey = 'AddYourBingKeyHere'
  db_file = 'C:/ProgramData/NeoFly/common.db'
  neofly_window_name = 'NeoFly 3.11.4'                  # needed for interfacing with the NeoFly gui

  good = 'Caviar'

  map_center_lat = '40.416775'
  map_center_lng = '-3.703790'
  zoom_level = '6'
  ```
  
## Running
Before running these scripts, please backup your NeoFly database!

### scan_markets.py
Execution: `python3 scan_markets.py`<br>
Before running the script, NeoFly needs to be running and e.g. on the "Mission" tab.<br>
This script will move your mouse cursor and access the specified markets in the NeoFly gui.<br>
Inside NeoFly this will effectively generate the list of goods an airport wants to buy/sell.

### show_goods_on_map.py
Execution: `python3 show_goods_on_map.py`<br>
NeoFly itself does not need to be running for this script.<br>
This script will access the NeoFly database and fetch a list of airports that buy/sell the specified goods.<br>
A map will be generated with these airports and be saved as index.html <br>
Now simply open the index.html in the browser of your choice.

## Example
![This is an image](/doc/screenshot_LE+LP.png)
