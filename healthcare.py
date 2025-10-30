# healthcare.py
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Environment variables (keep your API keys in .env)
OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY")
RXNAV_BASE_URL = "https://rxnav.nlm.nih.gov/REST"

def check_health_status(symptoms):
    """
    Simple AI-based symptom check.
    (Extendable with real ML models in the future)
    """
    common_conditions = {
        "fever": "You may have an infection or flu. Stay hydrated and rest.",
        "headache": "Possible dehydration or tension. Try water and rest.",
        "cough": "Could be a cold or allergies. If persistent, see a doctor.",
        "fatigue": "Could be stress or lack of sleep. Take breaks and hydrate."
    }
    for key in common_conditions:
        if key in symptoms.lower():
            return common_conditions[key]
    return "Unable to determine condition. Please consult a medical professional."

def lookup_medication_info(drug_name):
    """
    Queries RxNav or OpenFDA API for drug details.
    """
    try:
        # First, try RxNav API
        url = f"{RXNAV_BASE_URL}/drugs?name={drug_name}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "drugGroup" in response.json():
            data = response.json()
            concepts = data.get("drugGroup", {}).get("conceptGroup", [])
            if concepts:
                meds = []
                for group in concepts:
                    for concept in group.get("conceptProperties", []):
                        meds.append({
                            "name": concept.get("name"),
                            "rxcui": concept.get("rxcui"),
                            "synonym": concept.get("synonym")
                        })
                return {
                    "source": "RxNav NIH",
                    "timestamp": datetime.utcnow().isoformat(),
                    "results": meds[:5]  # limit for readability
                }

        # Fallback: OpenFDA API (if RxNav fails)
        if OPENFDA_API_KEY:
            url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}&api_key={OPENFDA_API_KEY}"
        else:
            url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}"

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                info = results[0].get("openfda", {})
                return {
                    "source": "OpenFDA",
                    "timestamp": datetime.utcnow().isoformat(),
                    "brand_name": info.get("brand_name", ["N/A"])[0],
                    "manufacturer": info.get("manufacturer_name", ["Unknown"])[0],
                    "purpose": results[0].get("purpose", ["No info available"])[0]
                }

        return {"error": "No information found for this medication."}

    except Exception as e:
        return {"error": str(e)}

def list_supported_services():
    """
    Lists all active healthcare services.
    """
    return {
        "services": [
            "Symptom Checker",
            "Medication Lookup (RxNav + OpenFDA)",
            "Health Tips",
            "Emergency Contact Helper"
        ],
        "version": "v2.5",
        "developer_note": "Integrate securely with .env to manage API keys."
    }

if __name__ == "__main__":
    # Test block (optional)
    print("Checking symptom:")
    print(check_health_status("I have a fever and headache"))
    print("\nMedication info:")
    print(lookup_medication_info("Tylenol"))
    print("\nAvailable services:")
    print(list_supported_services())