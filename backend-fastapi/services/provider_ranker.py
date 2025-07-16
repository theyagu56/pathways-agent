from typing import List, Dict
from utils.logger import get_logger

logger = get_logger(__name__)

def calculate_distance(zip1: str, zip2: str) -> float:
    logger.debug(f"Calculating distance between zip codes: {zip1} and {zip2}")
    try:
        zip1_num = int(zip1[:5]) if zip1.isdigit() else 10000
        zip2_num = int(zip2[:5]) if zip2.isdigit() else 10000
        distance = abs(zip1_num - zip2_num) / 1000.0
        logger.debug(f"Distance calculated: {distance} miles")
        return distance
    except Exception as e:
        logger.warning(f"Error calculating distance between '{zip1}' and '{zip2}': {e}")
        return 50.0

def rank_providers(providers: List[Dict], specialties: List[str], target_zip: str, target_insurance: str) -> List[Dict]:
    logger.info(f"Ranking {len(providers)} providers")
    logger.debug(f"Target specialties: {specialties}")
    logger.debug(f"Target zip: {target_zip}, Target insurance: {target_insurance}")
    
    ranked = []
    
    for i, provider in enumerate(providers):
        try:
            logger.debug(f"Processing provider {i+1}/{len(providers)}: {provider.get('name', 'Unknown')}")
            
            # Calculate specialty match score
            specialty_match = 1.0 if provider.get("specialty") in specialties else 0.3
            logger.debug(f"Specialty match score: {specialty_match}")
            
            # Calculate distance
            distance = calculate_distance(target_zip, provider.get("zip_code", ""))
            logger.debug(f"Distance: {distance} miles")
            
            # Check insurance compatibility
            insurance_match = 1.0 if target_insurance in provider.get("insurances", []) else 0.5
            logger.debug(f"Insurance match score: {insurance_match}")
            
            # Calculate overall score (weighted combination)
            score = (specialty_match * 0.5) + (insurance_match * 0.3) + (1.0 / (1.0 + distance) * 0.2)
            logger.debug(f"Overall score: {score:.3f}")
            
            # Create ranking reason
            reasons = []
            if specialty_match > 0.8:
                reasons.append("Specialty match")
            if insurance_match > 0.8:
                reasons.append("Insurance match")
            if distance < 10:
                reasons.append("Nearby provider")
            
            ranking_reason = ", ".join(reasons) or "General match"
            logger.debug(f"Ranking reason: {ranking_reason}")
            
            ranked.append({
                "name": provider.get("name"),
                "specialty": provider.get("specialty"),
                "distance": distance,
                "availability": provider.get("availability_date"),
                "ranking_reason": ranking_reason,
                "score": score
            })
            
        except Exception as e:
            logger.error(f"Error processing provider {i}: {e}", exc_info=True)
            continue
    
    # Sort by score and return top results
    ranked.sort(key=lambda x: x["score"], reverse=True)
    top_results = ranked[:3]
    
    logger.info(f"Ranking completed - Top {len(top_results)} providers selected")
    for i, provider in enumerate(top_results):
        logger.info(f"Rank {i+1}: {provider['name']} (Score: {provider['score']:.3f})")
    
    return top_results 