import pandas as pd

def read_specific_attributes(df, attributes):
    return df[attributes]

def route_query(analyzed_query, path):
    if analyzed_query["is_valid"]:
        df = pd.read_csv(path)
        drug_data = df[(df['Drug Name'] == analyzed_query['Drug Name']) & 
                       (df['Resolution Date'].str.contains(str(analyzed_query['year'])))]
        
        if drug_data.empty:
            return {"error": f"No data found for drug {analyzed_query['Drug Name']} in year {analyzed_query['year']}"}
        
        drug_info = drug_data.iloc[0]
        
        sub_llm_data = {
            "sub_llm_1": {
                "attributes": ["Drug Name", "Resolution Date", "Indication"],
                "data": read_specific_attributes(drug_info, ["Drug Name", "Resolution Date", "Indication"]).to_dict()
            },
            "sub_llm_2": {
                "attributes": ["Comparator Therapy", "Benefit Assessment", "Side Effects"],
                "data": read_specific_attributes(drug_info, ["Comparator Therapy", "Benefit Assessment", "Side Effects"]).to_dict()
            },
            "sub_llm_3": {
                "attributes": ["Mortality Difference", "Morbidity", "Annual Comparitive Therapy Costs", "Combination Therapy"],
                "data": read_specific_attributes(drug_info, ["Mortality Difference", "Morbidity", "Annual Comparitive Therapy Costs", "Combination Therapy"]).to_dict()
            },
            "sub_llm_4": {
                "attributes": ["Adverse Event Discontinuation", "Serious Adverse Events", "Response Rates"],
                "data": read_specific_attributes(drug_info, ["Adverse Event Discontinuation", "Serious Adverse Events", "Response Rates"]).to_dict()
            }
        }
        
        return sub_llm_data
    else:
        return {"error": analyzed_query["error"]}