## MetaData on Polling Stations

The script [poll_station_metadata.py](poll_station_metadata.py) scrapes http://psleci.nic.in/Default.aspx and creates [poll_station_metadata.csv](poll_station_metadata.csv) containing data from the dropdowns (State, District, AC, etc.), location of the polling station from Google Maps, and whatever is available on the polling station page (example: http://psleci.nic.in/pslinfoc.aspx?S=S01&A=153&P=15). 

The final CSV has the following columns:

1. from the dropdowns: `state_or_ut, district, ac, polling_station`
2. lat/long of the polling station: `lat, long`
3. details about the election officer: `blo, ero, deo, ceo`
4. `eroll, supplementary` (There can be two links. If there is one, link is put under eroll. If there is a supplementary eroll, second link goes under it. **Some links are dead.**)
5. data on polling station: 

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
