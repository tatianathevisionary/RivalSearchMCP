---
name: mcp-tool-development
description: Best practices for developing FastMCP tools with proper error handling, validation, and documentation
license: MIT
compatibility: opencode
metadata:
  audience: developers
  framework: fastmcp
---

## MCP Tool Development Best Practices

### Tool Structure
```python
@mcp.tool(
    name="tool_name",
    description="Brief description of what the tool does",
    tags={"category", "subcategory"}
)
async def tool_name(
    param1: Annotated[str, Field(description="Parameter description")],
    param2: Optional[int] = None,
    ctx: Context = CurrentContext()
) -> str:
    """
    Comprehensive docstring explaining the tool.

    Args:
        param1: Detailed parameter description
        param2: Optional parameter with default behavior
        ctx: MCP context for logging and progress

    Returns:
        Description of return value format

    Raises:
        ToolError: When user input is invalid
        Exception: For unexpected errors
    """
    pass
```

### Key Patterns

#### 1. Context Usage
Always use CurrentContext() for modern FastMCP:
```python
ctx: Context = CurrentContext()
await ctx.info("Starting operation...")
await ctx.report_progress(progress=50, total=100)
```

#### 2. Error Handling
```python
try:
    # Tool implementation
    result = await external_api_call()
    return format_result(result)
except ValidationError as e:
    await ctx.error(f"Invalid input: {e}")
    raise ToolError(f"Input validation failed: {str(e)}")
except APIError as e:
    await ctx.error(f"External API error: {e}")
    raise ToolError(f"Service temporarily unavailable: {str(e)}")
except Exception as e:
    logger.error(f"Unexpected error in tool_name: {e}")
    await ctx.error("An unexpected error occurred")
    raise ToolError("Operation failed due to unexpected error")
```

#### 3. Input Validation
```python
def validate_param(param: str) -> str:
    """Validate and sanitize input parameter."""
    if not param or len(param.strip()) < 1:
        raise ToolError("Parameter cannot be empty")
    if len(param) > 1000:
        raise ToolError("Parameter too long (max 1000 characters)")
    return param.strip()
```

#### 4. Progress Reporting
```python
await ctx.report_progress(progress=0, total=100)
# Phase 1
await ctx.report_progress(progress=25, total=100)
# Phase 2
await ctx.report_progress(progress=75, total=100)
# Complete
await ctx.report_progress(progress=100, total=100)
```

#### 5. Logging
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Detailed debug information")
logger.info("Important operational messages")
logger.warning("Warning about potential issues")
logger.error("Error conditions")
```

### When to Use This Skill
- Creating new MCP tools
- Refactoring existing tools
- Ensuring consistency across the codebase
- Debugging tool issues
- Reviewing tool implementations

Ask clarifying questions about the specific tool requirements, expected parameters, and integration points.