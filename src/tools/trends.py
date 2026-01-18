from typing import List, Optional, Any, Dict
from datetime import datetime

import pandas as pd
from fastmcp import FastMCP
from pydantic import Field
from typing_extensions import Annotated

from src.core.trends import GoogleTrendsAPI
from src.logging.logger import logger
from src.utils.markdown_formatter import format_trends_markdown

"""
Trends analysis tools for FastMCP server.
Provides Google Trends data analysis and export capabilities.
"""


def register_trends_tools(mcp: FastMCP):
    @mcp.tool
    async def trends_core(
        operation: str,
        keywords: List[str],
        timeframe: str = "today 7-d",
        geo: str = "",
        gprop: str = "",
        resolution: str = "COUNTRY",
    ) -> str:
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
                result = {
                    "success": True,
                    "data": data.to_dict("records")
                    if hasattr(data, "to_dict")
                    else data,
                }
                return format_trends_markdown(result)

            elif operation == "related":
                queries = api.get_related_queries(keywords, timeframe, geo)
                topics = api.get_related_topics(keywords, timeframe, geo)
                result = {
                    "success": True,
                    "related_queries": queries,
                    "related_topics": topics,
                }
                return format_trends_markdown(result)

            elif operation == "interest_over_time":
                data = api.get_interest_over_time(keywords, timeframe, geo, gprop)
                result = {
                    "success": True,
                    "data": data.to_dict("records")
                    if hasattr(data, "to_dict")
                    else data,
                }
                return format_trends_markdown(result)

            elif operation == "regional":
                region_data = api.get_interest_by_region(
                    keywords, resolution, timeframe, geo
                )
                searches = api.get_trending_searches(geo or "united_states")
                result = {
                    "success": True,
                    "interest_by_region": region_data.to_dict("records")
                    if hasattr(region_data, "to_dict")
                    else region_data,
                    "trending_searches": searches,
                }
                return format_trends_markdown(result)

            elif operation == "compare":
                time_data = api.get_interest_over_time(keywords, timeframe, geo, "")
                queries_data = api.get_related_queries(keywords, timeframe, geo)
                region_data = api.get_interest_by_region(
                    keywords, "COUNTRY", timeframe, geo
                )
                result = {
                    "success": True,
                    "interest_over_time": time_data.to_dict("records")
                    if hasattr(time_data, "to_dict")
                    else time_data,
                    "related_queries": queries_data,
                    "interest_by_region": region_data.to_dict("records")
                    if hasattr(region_data, "to_dict")
                    else region_data,
                }
                return format_trends_markdown(result)

            else:
                result = {"success": False, "error": f"Unknown operation: {operation}"}
                return format_trends_markdown(result)

        except Exception as e:
            logger.error(f"Trends core failed: {e}")
            result = {"success": False, "error": str(e)}
            return format_trends_markdown(result)

    @mcp.tool
    async def trends_export(
        keywords: List[str],
        timeframe: str = "today 7-d",
        geo: str = "",
        format: str = "csv",
        filename: Optional[str] = None,
    ) -> str:
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
                return "❌ **Error:** No trends data found to export"

            if not filename:
                filename = (
                    f"trends_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
                )

            df = pd.DataFrame(
                data.to_dict("records") if hasattr(data, "to_dict") else data
            )

            rows_exported = len(df)

            if format == "csv":
                df.to_csv(filename, index=False)
                file_info = f"CSV file with {rows_exported} rows"
            elif format == "json":
                import json

                with open(filename, "w") as f:
                    json.dump(
                        data.to_dict("records") if hasattr(data, "to_dict") else data,
                        f,
                        indent=2,
                        default=str,
                    )
                file_info = f"JSON file with {rows_exported} records"
            elif format == "sql":
                import sqlite3

                conn = sqlite3.connect(f"{filename}.db")
                df.to_sql("trends_data", conn, if_exists="replace", index=False)
                conn.close()
                file_info = f"SQLite database with {rows_exported} rows in 'trends_data' table"
            else:
                return f"❌ **Error:** Unsupported format '{format}'. Use 'csv', 'json', or 'sql'"

            # Format success message
            return f"""✅ **Trends Data Exported Successfully**

**File:** `{filename}`
**Format:** {format.upper()}
**Data:** {file_info}
**Keywords:** {', '.join(keywords)}
**Timeframe:** {timeframe}
{f"**Geographic Region:** {geo}" if geo else ""}

Your trends data has been exported and is ready to use in your analysis tools.

*Export completed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""

        except Exception as e:
            logger.error(f"Export failed: {e}")
            return f"❌ **Error:** Export failed - {str(e)}"
