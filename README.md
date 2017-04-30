# BattleParis-Districts
Fetch basic infos about a district in Battle Paris.

Battle Paris is a geolocalization based game that's taking place in Paris. This little Python script helps you to fetch infos about a district.

## How to use ?

- Fill out the infos on userpwd.txt
- Import BPQuartiers
- Call `BPQuartiers.getFormattedText()`

You can pass the index of the district you want as argument to that function : `BPQuartiers.getFormattedText(44)`

The good thing is, it's just what I needed.
