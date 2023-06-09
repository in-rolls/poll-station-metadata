## MetaData on Polling Stations

### 🚫 This repository is a public read only archive. The code was written to scrape data at a point in time.

Data on 989,624 polling stations from 32 states or union territories from http://psleci.nic.in/Default.aspx

## Data

The [final CSV (.7z)](poll_station_metadata_all.7z) has the following columns:

1. state, district, ac, and polling station: `state_or_ut, district, ac, polling_station` 
2. lat/long of the polling station: `lat, long`
3. details about the election officer: `blo, ero, deo, ceo`
4. links to electoral rolls: The link to the primary electoral roll is posted under `eroll` and the supplementary roll goes under `supplementary`. Not all polling stations have supplementary rolls. **Note: Many of the links are dead.**
5. data on the polling station: 

    `Building Quality,
    PS with less than 20 sqmts,  
    PS buildings is dilapidated or dangerous,  
    PS is in Govt building/Premises,  
    PS located in an institution/religious place,  
    PS in School/College building,  
    PS in ground floor,  
    PS having Separate door for Entry and Exit,  
    political party office situated within 200 meters of PS premises,  
    PS is having drinking water facilities in the premises,  
    PS buildings having Electricity Supply,  
    PS buildings with Proper lighting, Fixtures etc.,  
    PS buildings with Toilet(Male/Female),  
    PS with ramps For Disable,  
    PS buildings with Adequate Furniture,  
    PS with shade/shelter for protection from sun/rain etc.,  
    PS with Proper road connectivity,  
    PS where voters have to cross river/valley/ravine or natural obstacle to reach PS,  
    PS with Landline Telephone/Fax Connection,  
    PS with Mobile connectivity,  
    PS with Internet facility,  
    PS with Proper signage of Building name and address,  
    PS with in LWE/insurgency affected area,  
    PS With in forest/semi-forest area,  
    PS in vulnerable critical location,  
    sensitive/hyper-sensitive PS`

### Script

The script [poll_station_metadata.py](poll_station_metadata.py) scrapes http://psleci.nic.in/Default.aspx and creates [poll_station_metadata.csv](poll_station_metadata.csv) containing data from the dropdowns (State, District, AC, etc.), location of the polling station from Google Maps, and whatever is available on the polling station page (example: http://psleci.nic.in/pslinfoc.aspx?S=S01&A=153&P=15). 

### Running the Script

```
pip install -r requirements.txt
python poll_station_metadata.py
```

### Some Basic Facts About Indian Polling Stations

Of the 748,584 polling stations about which we have data on building conditions, nearly 24% report having Internet and a similar number report 
having "Landline Telephone/Fax Connection." 97.7% report having toilets for men and women. 2.6% report being in a "dilapidated or dangerous" building. 

93.2% report having ramps for the disabled. 98.3% report having "proper road connectivity." Nearly 4% report being located at a place where the "voters have to cross river/valley/ravine or natural obstacle to reach PS."

92% of the polling stations are located in "Govt building/Premises." And 11.4% are reportedly located in "an institution/religious place." 

8% report having a "political party office situated within 200 meters of PS premises."
