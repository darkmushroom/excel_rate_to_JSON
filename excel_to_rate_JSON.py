import os
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description ='Create price strategies from Excel copypasta')
    parser.add_argument('couriers', help='A comma-separated list of couriers to build.')
    parser_args = parser.parse_args()
    couriers = parser_args.couriers.split(',')
    couriers = [s.strip() for s in couriers]

    strategies = []

    for courier in couriers:
        strategies.append(cookJSON(courier))

    pricing_strategies = {"pricing_strategies": strategies}

    if (os.path.exists('output') == False):
        os.mkdir('output')
    output_file = open('output/export.json', 'w+', encoding='utf8')
    output_file.write(json.dumps(pricing_strategies))
    output_file.close()

def cookJSON(this_carrier):

    postal_codes = parse_postcode_areas(this_carrier + "/postcode_areas.txt")
    weight_mins_and_maxs = parse_weight_mins_and_maxs(this_carrier + "/mins_and_maxs.txt")
    weight_minimums = weight_mins_and_maxs["minimums"]
    weight_maximums = weight_mins_and_maxs["maximums"]
    shipping_amounts = parse_price_tiers(this_carrier + "/price_tiers.txt")
    postcode_map = parse_postcode_map(this_carrier + "/area_postcode_map.txt")

    if (len(postal_codes) != len(shipping_amounts)):
        raise Exception("postal code list not the same size as provided amounts")

    if (len(weight_minimums) != len(weight_maximums)):
        raise Exception("uneven amount of minimums and maximums")

    if (len(weight_minimums) != len(shipping_amounts[0].split(','))):
        raise Exception("uneven amount of weight tiers to shipping amounts")

    print("Alright, let's cook up some JSON for " + this_carrier +"...")

    tiered_destination_prices = []
    tiered_prices = []

    for i in range (0, len(postal_codes)):
        for j in range(0, len(weight_minimums)):
            tiered_prices.append( {'start_value': weight_minimums[j], 'end_value': weight_maximums[j], 'price': shipping_amounts[i].split(',')[j].strip() } )
    
        if postal_codes[i] in postcode_map:
            tiered_destination_prices.append( {'restriction_strategy': 'postal_code_starts_with', 'restriction_value': postcode_map[postal_codes[i]], 'tiered_prices': tiered_prices} )
        else:
            print("Warning! Postcode abbreviation: " + postal_codes[i] + " not in " + this_carrier + " postcode map")

        tiered_prices = []


    price_strategy = {'price_strategy': 'weight-tiered_destination_prices', 'product_restrictions': [ { 'restriction_value': this_carrier, 'restriction_strategy': "product_tag_is" } ], "tiered_destination_prices": tiered_destination_prices }

    print("...done!\n")

    return price_strategy

# comma-separated list of postal codes.
# each value should match a row in price_tiers.txt
def parse_postcode_areas(postcode_file):
    with open(postcode_file) as f:
        contents = f.readlines()

    postal_codes = []
    for line in contents:
        if line[0] == '\n' or line[0] == "#":
            pass
        else:
            postal_codes.append(line.strip())

    return postal_codes

# a two-line comma-separated list of weight values in kilograms
# the top line is the weight minimums, the bottom line is the weight maximums
# These weights may be accurate to two decimal places (i.e. decagram)
def parse_weight_mins_and_maxs(limits_file):
    with open(limits_file) as f:
        contents = f.readlines()

    i = 0
    for line in contents:
        if line[0] == '\n' or line[0] == "#":
            i += 1
        else:
            break

    weight_minimums_parse = contents[i].strip().split(',')
    weight_maximums_parse = contents[i+1].split(',')
    weight_minimums = [float(numeric_string) for numeric_string in weight_minimums_parse]
    weight_maximums = [float(numeric_string) for numeric_string in weight_maximums_parse]

    return {"minimums": weight_minimums, "maximums": weight_maximums}

# A two dimensional matrix of prices. 
# Values must NOT have commas (aka 1000.00 not 1,000.00)
#
# each row represents a list of prices for the given postcode
# each column represents what prices are available in that weight range
def parse_price_tiers(price_tiers_file):

    shipping_amounts = []
    with open(price_tiers_file) as f:
        contents = f.readlines()
    for line in contents:
        if line[0] == '\n' or line[0] == "#":
            pass
        else:
            shipping_amounts.append(line.strip())

    return shipping_amounts

# Reduce the postcode map to a dictionary of {"postcode_area": "list, of, postcodes"}
# When we encounter a postcode area for the first time, add it and its corresponding postcode to the dictionary
# if a postcode area is already in the dictionary, append that postcode to it's entry with a comma
def parse_postcode_map(postcode_map_file):
    
    postcode_map = {}

    with open(postcode_map_file) as f:
        contents = f.readlines()

    for line in contents:
        if line[0] == '\n' or line[0] == "#":
            pass
        else:
            line_key_value = line.strip().split(',')
            postcode_abbreviation = line_key_value[0]
            postcode_value = line_key_value[1]

            if not postcode_abbreviation in postcode_map:
                postcode_map[postcode_abbreviation] = postcode_value.strip()
            else:
                postcode_map[postcode_abbreviation] += ', '+postcode_value.strip()

    return postcode_map

if __name__ =="__main__":
    main()
