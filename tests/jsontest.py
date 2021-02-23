import json


data = {}
data['errors'] = []
data['errors'].append({
    'date': '',
    'command': '',
    'author': 'the author',
    'channel': 'The channel',
    'error': 'the errror'
})

with open('tests/test.json', 'w') as outfile:
    json.dump(data, outfile, indent=5)