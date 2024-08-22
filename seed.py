import climate_data_summarizer as cds   
import webapp_data_writer as wd

location = {"city_name":"Mumbai", "country":"India"}
query_type = "num_days_above_90"

response = cds.summarize_climate_data(location, query_type)
wd.write(location, response["llm"]["replies"][0], query_type)
