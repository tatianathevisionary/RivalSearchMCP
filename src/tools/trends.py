from typing import List, Optional, Any
from datetime import datetime

import pandas as pd
from fastmcp import FastMCP
from pydantic import Field
from typing_extensions import Annotated

from src.core.trends import GoogleTrendsAPI
from src.logging.logger import logger

"""
Trends analysis tools for FastMCP server.
Provides Google Trends data analysis and export capabilities.
"""


def register_trends_tools(mcp: FastMCP):
    @mcp.tool
    async def trends_core(
        operation,
        keywords,
        timeframe="today 7-d",
        geo="",
        gprop="",
        resolution="COUNTRY",
    ):
        """
        Consolidated trends core: search, related, regional, compare operations.

        Args:
            operation: "search", "related", "interest_over_time", "regional", "compare"
            keywords: List of keywords
            timeframe: Time range (e.g., "today 7-d")
            geo: Geographic region code
            gprop: Google property
            resolution: For regional operations
        """
        try:
            logger.info(f"Trends core {operation} for: {keywords}")

            api = GoogleTrendsAPI()

            if operation == "search":
                data = api.search_trends(keywords, timeframe, geo, gprop)
                return {
                    "success": True,
                    "data": data.to_dict("records")
                    if hasattr(data, "to_dict")
                    else data,
                }

            elif operation == "related":
                queries = api.get_related_queries(keywords, timeframe, geo)
                topics = api.get_related_topics(keywords, timeframe, geo)
                return {
                    "success": True,
                    "related_queries": queries,
                    "related_topics": topics,
                }

            elif operation == "interest_over_time":
                data = api.get_interest_over_time(keywords, timeframe, geo, gprop)
                return {
                    "success": True,
                    "data": data.to_dict("records")
                    if hasattr(data, "to_dict")
                    else data,
                }

            elif operation == "regional":
                region_data = api.get_interest_by_region(
                    keywords, resolution, timeframe, geo
                )
                searches = api.get_trending_searches(geo or "united_states")
                return {
                    "success": True,
                    "interest_by_region": region_data.to_dict("records")
                    if hasattr(region_data, "to_dict")
                    else region_data,
                    "trending_searches": searches,
                }

            elif operation == "compare":
                time_data = api.get_interest_over_time(keywords, timeframe, geo, "")
                queries_data = api.get_related_queries(keywords, timeframe, geo)
                region_data = api.get_interest_by_region(
                    keywords, "COUNTRY", timeframe, geo
                )
                return {
                    "success": True,
                    "interest_over_time": time_data.to_dict("records")
                    if hasattr(time_data, "to_dict")
                    else time_data,
                    "related_queries": queries_data,
                    "interest_by_region": region_data.to_dict("records")
                    if hasattr(region_data, "to_dict")
                    else region_data,
                }

            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}

        except Exception as e:
            logger.error(f"Trends core failed: {e}")
            return {"success": False, "error": str(e)}

    @mcp.tool
    async def trends_export(
        keywords,
        timeframe="today 7-d",
        geo="",
        format="csv",
        filename=None,
    ):
        """
        Export trends data to various formats.

        Args:
            keywords: Keywords to export
            timeframe: Time range
            geo: Geographic region
            format: "csv", "json", "sql"
            filename: Output filename (auto-generated if None)
        """
        try:
            logger.info(f"Exporting trends to {format}")

            api = GoogleTrendsAPI()
            data = api.search_trends(keywords, timeframe, geo, "")

            if data is None or len(data) == 0:
                return {"success": False, "error": "No data found"}

            if not filename:
                filename = (
                    f"trends_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
                )

            df = pd.DataFrame(
                data.to_dict("records") if hasattr(data, "to_dict") else data
            )

            if format == "csv":
                df.to_csv(filename, index=False)
            elif format == "json":
                import json

                with open(filename, "w") as f:
                    json.dump(
                        data.to_dict("records") if hasattr(data, "to_dict") else data,
                        f,
                        indent=2,
                        default=str,
                    )
            elif format == "sql":
                import sqlite3

                conn = sqlite3.connect(f"{filename}.db")
                df.to_sql("trends_data", conn, if_exists="replace", index=False)
                conn.close()

            return {"success": True, "filename": filename, "format": format}

        except Exception as e:
            logger.error(f"Export failed: {e}")
            return {"success": False, "error": str(e)}
