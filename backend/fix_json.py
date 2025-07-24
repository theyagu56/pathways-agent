#!/usr/bin/env python3
import json
import re

def fix_providers_json():
    """Fix the providers.json file by removing the extra closing bracket"""
    
    # Read the file
    with open('../shared-data/providers.json', 'r') as f:
        content = f.read()
    
    print(f"Original file length: {len(content)}")
    print(f"Last 10 characters: {repr(content[-10:])}")
    
    # Remove the extra closing bracket at the end
    # The file should end with "  ]" not "  ]\n]"
    content = re.sub(r'\]\s*\]\s*$', ']', content)
    
    print(f"After fix, last 10 characters: {repr(content[-10:])}")
    
    # Try to parse the JSON
    try:
        data = json.loads(content)
        print(f"JSON is valid! Found {len(data)} providers")
        
        # Extract all unique specialties
        specialties = set()
        for provider in data:
            if isinstance(provider, dict) and 'specialty' in provider:
                specialties.add(provider['specialty'])
        
        print(f"Found {len(specialties)} unique specialties: {sorted(specialties)}")
        
        # Write the fixed JSON back
        with open('../shared-data/providers.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Fixed providers.json successfully!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"JSON still invalid: {e}")
        return False

if __name__ == "__main__":
    fix_providers_json() 