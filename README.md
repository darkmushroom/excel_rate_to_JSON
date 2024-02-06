# Excel to rate JSON
Oblivious parser that takes a pile of formatted text inputs and outputs a single JSON payload.

## Setup
Each courier should be placed in a folder of the same name. All the files for USPS should be in `USPS/`, for example.
You must supply four text files for each courier. See files in the `example_courier` folder for more information.

- `postcode_areas.txt` - A single column of postcode areas this courier represents. This also represents the order of postcode areas in price_tiers.txt
- `mins_and_maxs.txt` - A two-line, comma separated list of weights. The first line represents weight minimums, the second weight maximums
- `price_tiers.txt` - A matrix of prices. The X direction represents price increasing with weight, the Y direction represents each shipping area
- `area_postcode_map.txt` - A two-column, comma separated file relating postcode areas to the postcodes they represent

## Invocation
After pulling the repo, you can execute the command with:
```
python excel_to_rate_JSON.py "list, of, couriers"
```

To build the example courier, use:
```
python excel_to_rate_JSON.py example_courier
```

Output is placed in `output/export.json`

## Warnings:
This program contains some basic error checking, but in general
* Always double-check the JSON output
* There should be no gaps in `price_tiers.txt`
* There should be no commas in `price_tiers.txt` (aka 1000.00 not 1,000.00)
* If `postcode_areas.txt` includes an area that is not in the `area_postcode_map`, it will be skipped with a warning printed on the command line

Now go out there and make some commissions!
