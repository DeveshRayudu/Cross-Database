import json
from collections import OrderedDict

with open('first.json', 'r') as f1:
    first_data = json.load(f1)

with open('second.json', 'r') as f2:
    second_data = json.load(f2, object_pairs_hook=OrderedDict)

first_names = {item['objectName'] for item in first_data}
second_names = {item['objectName'] for item in second_data}
common_names = first_names & second_names

merged_data = []

# Merge common entries
for second_item in second_data:
    if second_item['objectName'] in common_names:
        first_item = next(f for f in first_data if f['objectName'] == second_item['objectName'])
        combined = OrderedDict()

        # Start with keys from second (preserve their order)
        for key in second_item:
            combined[key] = first_item.get(key, second_item[key])

        # Add any additional keys from first that aren't in second
        for key in first_item:
            if key not in combined:
                combined[key] = first_item[key]

        merged_data.append(combined)

# Add entries only in first.json
for first_item in first_data:
    if first_item['objectName'] not in second_names:
        merged_data.append(first_item)

with open('third.json', 'w') as f3:
    json.dump(merged_data, f3, indent=4)
