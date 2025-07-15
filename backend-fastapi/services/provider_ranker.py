from typing import List, Dict

def calculate_distance(zip1: str, zip2: str) -> float:
    try:
        zip1_num = int(zip1[:5]) if zip1.isdigit() else 10000
        zip2_num = int(zip2[:5]) if zip2.isdigit() else 10000
        return abs(zip1_num - zip2_num) / 1000.0
    except Exception:
        return 50.0

def rank_providers(providers: List[Dict], specialties: List[str], target_zip: str, target_insurance: str) -> List[Dict]:
    ranked = []
    for provider in providers:
        specialty_match = 1.0 if provider.get("specialty") in specialties else 0.3
        distance = calculate_distance(target_zip, provider.get("zip_code", ""))
        insurance_match = 1.0 if target_insurance in provider.get("insurances", []) else 0.5
        score = (specialty_match * 0.5) + (insurance_match * 0.3) + (1.0 / (1.0 + distance) * 0.2)
        reasons = []
        if specialty_match > 0.8:
            reasons.append("Specialty match")
        if insurance_match > 0.8:
            reasons.append("Insurance match")
        if distance < 10:
            reasons.append("Nearby provider")
        ranked.append({
            "name": provider.get("name"),
            "specialty": provider.get("specialty"),
            "distance": distance,
            "availability": provider.get("availability_date"),
            "ranking_reason": ", ".join(reasons) or "General match",
            "score": score
        })
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:3] 