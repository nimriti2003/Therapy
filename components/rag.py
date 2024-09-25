import pandas as pd

class RAGSystem:
    def __init__(self, path):
        self.path = path

    def retrieve_relevant_data(self, year, drug_name):
        """
        Retrieve historical data for a specific year and drug.
        """
        try:
            data = pd.read_csv(self.path)
            relevant_data = data[(data['Year'] == year) & (data['Drug Name'] == drug_name)]
            
            if relevant_data.empty:
                return {"error": "No data available for the given year and drug."}
            
            return relevant_data.iloc[0]  # Return the first row of relevant data
        except Exception as e:
            return {"error": f"Error retrieving data: {str(e)}"}
    
    def generate_prediction(self, sub_llm_results, historical_data):
        """
        Generate a cost prediction by combining sub-LLM results and historical data.
        """
        # Weight each sub-LLM result and multiply by historical cost for final prediction
        # Assuming equal weights for simplicity (can be adjusted based on importance)
        weight_1 = 0.3
        weight_2 = 0.4
        weight_3 = 0.3
        
        # Weighted combination of sub-LLM outputs
        llm_combined_factor = (sub_llm_results["attribute_1"] * weight_1 +
                               sub_llm_results["attribute_2"] * weight_2 +
                               sub_llm_results["attribute_3"] * weight_3)
        
        # Multiply by historical cost to generate the final prediction
        prediction = llm_combined_factor * historical_data["Cost"]
        
        return prediction

    def generate_future_prediction(self, sub_llm_results, historical_data, future_year):
        """
        Generate a future cost prediction based on historical data trends and sub-LLM results.
        """
        # Estimate growth rate using historical trends
        growth_rate = self.estimate_growth_rate(historical_data, future_year)
        
        # Apply the growth rate to the most recent historical cost
        future_prediction = historical_data['Cost'] * (1 + growth_rate)
        
        # Combine future prediction with sub-LLM factors for a more accurate result
        llm_combined_factor = (sub_llm_results["attribute_1"] +
                               sub_llm_results["attribute_2"] +
                               sub_llm_results["attribute_3"]) / 3
        
        # Adjust future prediction based on LLM factors
        future_prediction *= llm_combined_factor
        
        return future_prediction

    def estimate_growth_rate(self, historical_data, future_year):
        """
        Estimate the growth rate of the drug's cost using historical data trends.
        """
        try:
            # Fetch all historical data for the given drug to calculate growth trend
            data = pd.read_csv(self.path)
            drug_name = historical_data['Drug Name']
            historical_entries = data[data['Drug Name'] == drug_name]

            # Sort the entries by year to calculate year-over-year growth
            historical_entries = historical_entries.sort_values(by='Year')
            
            # Calculate average year-over-year growth rate based on historical costs
            total_growth = 0
            num_years = 0
            previous_cost = None
            
            for index, row in historical_entries.iterrows():
                if previous_cost is not None:
                    year_growth = (row['Cost'] - previous_cost) / previous_cost
                    total_growth += year_growth
                    num_years += 1
                previous_cost = row['Cost']
            
            # Calculate average growth rate across all available years
            if num_years > 0:
                average_growth_rate = total_growth / num_years
            else:
                average_growth_rate = 0.05  # Default growth rate if no prior data
            
            # Adjust the growth rate for the future year (e.g., linear extrapolation)
            current_year = historical_entries['Year'].max()
            years_ahead = future_year - current_year
            future_growth_rate = average_growth_rate * years_ahead
            
            return future_growth_rate
        except Exception as e:
            print(f"Error estimating growth rate: {str(e)}")
            return 0.05  # Default growth rate if error occurs
