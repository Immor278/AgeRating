# tracker_analyzer.py

import json
import os

def analyze_tracker(dx):
    trackers = []
    with open(os.path.join(os.path.dirname(__file__), 'trackers.json'), 'r') as f_trackers:
        for item in json.load(f_trackers)['trackers']:
            name = item['name']
            code_signature = "L" + str(item['code_signature']).replace('.', '/')
            if code_signature[-1] != '/':
                code_signature = code_signature + '/'

            code_signature = code_signature + '.*' 
            results = dx.find_classes(code_signature, True)
            for _ in results: 
                trackers.append(name)
                break
    result = {'Trackers': trackers}
    return result