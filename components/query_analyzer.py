def analyze_query(user_input):
    try:
        year, drug_name = map(str.strip, user_input.split(','))
        year = int(year)
        
        if 1900 <= year <= 2100:  # Adjust range as needed
            return {"year": year, "Drug Name": drug_name, "is_valid": True}
        else:
            return {"is_valid": False, "error": "Year out of valid range"}
    except ValueError:
        return {"is_valid": False, "error": "Invalid input. Please enter a valid year and drug name, separated by a comma."}