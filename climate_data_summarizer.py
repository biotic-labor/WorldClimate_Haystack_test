import warnings
from helper import load_env
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators.openai import OpenAIGenerator
from components.climate_service_api_fetcher import ClimateServiceAPIFetcher
import json
warnings.filterwarnings('ignore')
load_env()

query_types = {
    "num_days_above_80":{
        "prompt_value": "Number of days above 80 degrees farhenheit",
    }, "num_days_above_90":{
        "prompt_value": "Number of days above 90 degrees farhenheit",
    }, "num_days_above_100":{
        "prompt_value": "Number of days above 100 degrees farhenheit",
    }, "precip":{
        "prompt_value": "Cumulative Annual precipitation",
    }, "tempmax":{
        "prompt_value": "Maximum Temperature",
    }, "tempmin":{
        "prompt_value": "Minimum Temperature",
    }
}

def summarize_climate_data(location: object, query_type: str) :
    template=f"""You are a climate scientist. You will be given a dataframe with the following columns:datetime, data 
                where datetime represents a year in the future and data represents projected {query_types[query_type]["prompt_value"]} for that year.
                Analyze the data over the entire date range, provide analysis and climate risks related to that analysis. Calculate the rate of change of the data over the entire date range, provide output.
                Also, list 5 suggestions for how to prepare property owners for the projected change to the {query_types[query_type]["prompt_value"]} in future.
                Provide your response in JSON format similar to the following:{{analysis: string, risks: string, suggestions: string[]}}.
                {{{{dataframe}}}}"""
    prompt = PromptBuilder(template=template)
    llm = OpenAIGenerator()
    climateServiceAPIFetcher = ClimateServiceAPIFetcher()

    climate_suggester = Pipeline()
    climate_suggester.add_component("climateServiceAPIFetcher", climateServiceAPIFetcher)
    climate_suggester.add_component("prompt", prompt)
    climate_suggester.add_component("llm", llm)

    climate_suggester.connect("climateServiceAPIFetcher.dataframe", "prompt.dataframe")
    climate_suggester.connect("prompt", "llm")
    output = climate_suggester.run({"climateServiceAPIFetcher": {"location":location, "query_type": query_type}})

    print(output["llm"]["replies"][0])
    return output["llm"]["replies"][0]




