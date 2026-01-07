import os
import requests
from langchain_tavily import TavilySearch


class FoursquarePlaceSearchTool:
    """Foursquare Places API integration for location-based searches."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.foursquare.com/v3/places/search"
        self.headers = {
            "Accept": "application/json",
            "Authorization": api_key
        }
    
    def _search_places(self, query: str, near: str, limit: int = 10) -> str:
        """Generic search method for Foursquare Places API."""
        try:
            params = {
                "query": query,
                "near": near,
                "limit": limit
            }
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for place in data.get("results", []):
                name = place.get("name", "Unknown")
                address = place.get("location", {}).get("formatted_address", "Address not available")
                categories = ", ".join([cat.get("name", "") for cat in place.get("categories", [])])
                results.append(f"- {name} ({categories}): {address}")
            
            return "\n".join(results) if results else "No results found."
        except Exception as e:
            return f"Error fetching data from Foursquare: {str(e)}"
    
    def search_attractions(self, place: str) -> str:
        """Search for tourist attractions in the specified place."""
        return self._search_places("tourist attractions landmarks", place, 10)
    
    def search_restaurants(self, place: str) -> str:
        """Search for restaurants in the specified place."""
        return self._search_places("restaurants", place, 10)
    
    def search_activity(self, place: str) -> str:
        """Search for activities in the specified place."""
        return self._search_places("activities entertainment", place, 10)
    
    def search_transportation(self, place: str) -> str:
        """Search for transportation options in the specified place."""
        return self._search_places("transportation bus station airport train", place, 10)


class TavilyPlaceSearchTool:
    """Fallback search using Tavily when Foursquare fails."""
    
    def __init__(self):
        pass

    def tavily_search_attractions(self, place: str) -> dict:
        """Search for attractions using TavilySearch."""
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_restaurants(self, place: str) -> dict:
        """Search for restaurants using TavilySearch."""
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_activity(self, place: str) -> dict:
        """Search for activities using TavilySearch."""
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_transportation(self, place: str) -> dict:
        """Search for transportation options using TavilySearch."""
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result