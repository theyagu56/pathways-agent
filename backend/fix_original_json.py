#!/usr/bin/env python3
import json
import re

def fix_original_providers_json():
    """Fix the original providers.json file to extract all specialties dynamically"""
    
    # Read the original file
    with open('../shared-data/providers.json', 'r') as f:
        content = f.read()
    
    print(f"Original file length: {len(content)}")
    
    # Find all provider objects by looking for the pattern
    # This is a more robust way to extract providers even with JSON corruption
    provider_pattern = r'\{\s*"id":\s*"[^"]*",\s*"name":\s*"[^"]*",\s*"specialty":\s*"[^"]*",\s*"zip_code":\s*"[^"]*",\s*"insurances":\s*\[[^\]]*\],\s*"rating":\s*[0-9.]+,\s*"distance":\s*[0-9.]+,\s*"availability_date":\s*"[^"]*"\s*\}'
    
    providers = []
    matches = re.finditer(provider_pattern, content, re.DOTALL)
    
    for match in matches:
        try:
            provider_str = match.group(0)
            provider = json.loads(provider_str)
            providers.append(provider)
        except json.JSONDecodeError:
            continue
    
    print(f"Extracted {len(providers)} valid providers")
    
    # Extract all unique specialties
    specialties = set()
    for provider in providers:
        if 'specialty' in provider:
            specialties.add(provider['specialty'])
    
    print(f"Found {len(specialties)} unique specialties: {sorted(specialties)}")
    
    # Write the fixed JSON back
    with open('../shared-data/providers.json', 'w') as f:
        json.dump(providers, f, indent=2)
    
    print("Fixed providers.json successfully!")
    
    # Show specialty distribution
    specialty_counts = {}
    for provider in providers:
        specialty = provider['specialty']
        specialty_counts[specialty] = specialty_counts.get(specialty, 0) + 1
    
    print("\nSpecialty distribution:")
    for specialty, count in sorted(specialty_counts.items()):
        print(f"  {specialty}: {count} providers")
    
    return True

if __name__ == "__main__":
    fix_original_providers_json() 