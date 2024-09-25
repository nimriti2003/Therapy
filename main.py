from components.query_analyzer import analyze_query
from components.re_router import route_query
from components.sub_llm import process_sub_llm
from components.rag import RAGSystem
from components.response_aggregate import aggregate_response

def main():
    # Input user query
    user_query = input("Enter the year and drug name for cost prediction (e.g., '2025, Aspirin'): ")
    
    # Analyze the query to extract year and drug name
    analyzed_query = analyze_query(user_query)
    if not analyzed_query["is_valid"]:
        print(f"Error: {analyzed_query['error']}")
        return
    
    print(analyzed_query)
    
    # Define the path to the CSV file
    path = r'data/sample.csv'
    
    # Route the query to check if the drug exists and retrieve relevant data
    routed_query = route_query(analyzed_query, path)
    
    if "error" in routed_query:
        print(f"Error: {routed_query['error']}")
        return
    
    # Process sub-LLMs outputs (various attributes that influence the prediction)
    sub_llm_results = process_sub_llm(routed_query, path)
    
    print("yes working")
    # Instantiate the RAG system to fetch historical data and perform predictions
    rag = RAGSystem(path)
    historical_data = rag.retrieve_relevant_data(analyzed_query["year"], analyzed_query["Drug Name"])
    
    # Check if the data for the future year is available, if not, use historical data
    if analyzed_query["year"] > 2023:  # Assuming 2023 is the latest year in the dataset
        print(f"Data for the year {analyzed_query['year']} does not exist. Using historical data for predictions.")
    else:
        if 'error' in historical_data:
            print(f"Error: {historical_data['error']}")
            return
    
    # Generate the final prediction
    rag_prediction = rag.generate_prediction(sub_llm_results, historical_data)
    
    # Aggregate the response and print it
    final_response = aggregate_response(analyzed_query["year"], analyzed_query["Drug Name"], sub_llm_results, rag_prediction)
    print(final_response)

if __name__ == "__main__":
    main()
