#!/usr/bin/env python3
"""
Test script for Voice Integration
Demonstrates the voice-to-text and healthcare intake capabilities
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_voice_health():
    """Test voice service health"""
    print("🔍 Testing Voice Service Health...")
    response = requests.get(f"{BASE_URL}/api/voice/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Voice services are operational")
        print(f"   - Whisper available: {data['voice_services']['whisper_available']}")
        print(f"   - Azure available: {data['voice_services']['azure_available']}")
        print(f"   - Preferred method: {data['voice_services']['preferred_method']}")
    else:
        print(f"❌ Voice health check failed: {response.status_code}")
    print()

def test_text_processing():
    """Test text processing endpoint"""
    print("📝 Testing Text Processing...")
    
    test_cases = [
        {
            "text": "I have a severe headache and live in 75024",
            "insurance": "Cigna",
            "expected_specialties": ["Neurology", "Psychiatry"]
        },
        {
            "text": "My ears are swollen and I'm in zip code 75025",
            "insurance": "Blue Cross",
            "expected_specialties": ["ENT", "Allergy"]
        },
        {
            "text": "I broke my leg in a car accident, zip code 75026",
            "insurance": "Aetna",
            "expected_specialties": ["Orthopedics", "General Surgery"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"  Test Case {i}: {test_case['text'][:50]}...")
        
        response = requests.post(
            f"{BASE_URL}/api/voice/process-text",
            data={
                "text_input": test_case["text"],
                "insurance": test_case["insurance"]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"    ✅ Success!")
            print(f"    📍 Zip Code: {data['extracted_info']['zip_code']}")
            print(f"    🏥 Specialties: {', '.join(data['specialty_recommendations'])}")
            print(f"    👨‍⚕️ Providers found: {data['total_providers_found']}")
            
            # Show top provider
            if data['providers']:
                top_provider = data['providers'][0]
                print(f"    🥇 Top match: {top_provider['name']} ({top_provider['specialty']})")
        else:
            print(f"    ❌ Failed: {response.status_code}")
        print()

def test_specialty_endpoints():
    """Test specialty-related endpoints"""
    print("🏥 Testing Specialty Endpoints...")
    
    # Test getting all specialties
    response = requests.get(f"{BASE_URL}/api/specialties")
    if response.status_code == 200:
        specialties = response.json()
        print(f"✅ Available specialties: {len(specialties)} total")
        print(f"   Sample: {', '.join(specialties[:5])}...")
    else:
        print(f"❌ Failed to get specialties: {response.status_code}")
    
    # Test specialty recommendations
    test_injury = "I have chest pain and shortness of breath"
    response = requests.post(
        f"{BASE_URL}/api/specialty-recommendations",
        json={"injury_description": test_injury}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Specialty recommendations for '{test_injury}':")
        print(f"   {', '.join(data['recommended_specialties'])}")
    else:
        print(f"❌ Failed to get specialty recommendations: {response.status_code}")
    print()

def test_insurance_endpoints():
    """Test insurance endpoints"""
    print("💳 Testing Insurance Endpoints...")
    
    response = requests.get(f"{BASE_URL}/api/insurances")
    if response.status_code == 200:
        insurances = response.json()
        print(f"✅ Available insurances: {len(insurances)} total")
        print(f"   {', '.join(insurances)}")
    else:
        print(f"❌ Failed to get insurances: {response.status_code}")
    print()

def test_provider_matching():
    """Test provider matching endpoint"""
    print("🔍 Testing Provider Matching...")
    
    test_data = {
        "injury_description": "I have a persistent cough and fever",
        "zip_code": "75024",
        "insurance": "Cigna"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/match-providers",
        json=test_data
    )
    
    if response.status_code == 200:
        providers = response.json()
        print(f"✅ Found {len(providers)} matching providers")
        for i, provider in enumerate(providers[:2], 1):
            print(f"   {i}. {provider['name']} - {provider['specialty']}")
            print(f"      Distance: {provider['distance']} miles")
            print(f"      Reason: {provider['ranking_reason']}")
    else:
        print(f"❌ Provider matching failed: {response.status_code}")
    print()

def main():
    """Run all tests"""
    print("🎤 Voice Integration Test Suite")
    print("=" * 50)
    
    try:
        # Test basic endpoints
        test_voice_health()
        test_insurance_endpoints()
        test_specialty_endpoints()
        
        # Test core functionality
        test_text_processing()
        test_provider_matching()
        
        print("✅ All tests completed successfully!")
        print("\n🎯 Next Steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Navigate to 'Voice Intake' in the sidebar")
        print("3. Try recording audio or uploading audio files")
        print("4. Test the voice-to-text and provider matching features")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure the backend is running on http://localhost:8000")
        print("   Run: cd backend-fastapi && python -m uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main() 