import os
from utils.place_info_search import FoursquarePlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv


class PlaceSearchTool:
    """Place search tool using Foursquare API with Tavily fallback."""
    
    def __init__(self):
        load_dotenv()
        self.foursquare_api_key = os.environ.get("FOURSQUARE_API_KEY")
        self.foursquare_search = FoursquarePlaceSearchTool(self.foursquare_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            try:
                attraction_result = self.foursquare_search.search_attractions(place)
                if attraction_result and "Error" not in attraction_result:
                    return f"Following are the attractions of {place} from Foursquare:\n{attraction_result}"
            except Exception as e:
                pass
            # Fallback to Tavily
            tavily_result = self.tavily_search.tavily_search_attractions(place)
            return f"Following are the attractions of {place}:\n{tavily_result}"
        
        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            try:
                restaurants_result = self.foursquare_search.search_restaurants(place)
                if restaurants_result and "Error" not in restaurants_result:
                    return f"Following are the restaurants of {place} from Foursquare:\n{restaurants_result}"
            except Exception as e:
                pass
            # Fallback to Tavily
            tavily_result = self.tavily_search.tavily_search_restaurants(place)
            return f"Following are the restaurants of {place}:\n{tavily_result}"
        
        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            try:
                activities_result = self.foursquare_search.search_activity(place)
                if activities_result and "Error" not in activities_result:
                    return f"Following are the activities in and around {place} from Foursquare:\n{activities_result}"
            except Exception as e:
                pass
            # Fallback to Tavily
            tavily_result = self.tavily_search.tavily_search_activity(place)
            return f"Following are the activities of {place}:\n{tavily_result}"
        
        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                transport_result = self.foursquare_search.search_transportation(place)
                if transport_result and "Error" not in transport_result:
                    return f"Following are the transportation options in {place} from Foursquare:\n{transport_result}"
            except Exception as e:
                pass
            # Fallback to Tavily
            tavily_result = self.tavily_search.tavily_search_transportation(place)
            return f"Following are the transportation options in {place}:\n{tavily_result}"
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]