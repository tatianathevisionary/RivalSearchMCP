---
name: testing-patterns
description: Comprehensive testing patterns for MCP servers including unit tests, integration tests, and async testing
license: MIT
compatibility: opencode
metadata:
  audience: developers
  framework: pytest
---

## MCP Server Testing Patterns

### Test Structure
```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_server.py          # Server initialization tests
├── test_tools.py            # Tool functionality tests
├── test_integration.py      # Integration and workflow tests
├── test_performance.py      # Performance regression tests
└── test_rate_limiting.py    # API rate limiting tests
```

### Basic Test Setup

```python
import pytest
from fastmcp.client import Client
import asyncio

@pytest.fixture
async def mcp_client():
    """Fixture providing an MCP client connected to test server."""
    from server import app
    async with Client(app) as client:
        yield client

@pytest.mark.asyncio
async def test_tool_basic_functionality(mcp_client):
    """Test basic tool functionality."""
    result = await mcp_client.call_tool("tool_name", {"param": "value"})
    assert result.content
    content = result.content[0].text
    assert "expected_result" in content
```

### Tool Testing Patterns

#### 1. Parameter Validation Testing
```python
@pytest.mark.asyncio
async def test_tool_parameter_validation(mcp_client):
    """Test tool parameter validation."""
    # Test valid parameters
    result = await mcp_client.call_tool("academic_search", {
        "query": "machine learning",
        "max_results": 5
    })
    assert result.content

    # Test invalid parameters
    with pytest.raises(Exception):  # Should raise ToolError
        await mcp_client.call_tool("academic_search", {
            "query": "",  # Empty query should fail
            "max_results": 5
        })
```

#### 2. Error Handling Testing
```python
@pytest.mark.asyncio
async def test_tool_error_handling(mcp_client):
    """Test tool error handling."""
    # Test with invalid API key or network error
    result = await mcp_client.call_tool("research_workflow", {
        "topic": "test topic",
        "max_sources": 1,
        "enable_ai_insights": False  # Disable AI to avoid API calls
    })
    # Should handle errors gracefully, not crash
    assert result.content  # Should return error message, not exception
```

#### 3. Async Testing
```python
@pytest.mark.asyncio
async def test_async_tool_operations(mcp_client):
    """Test async operations complete properly."""
    import time
    start_time = time.time()

    result = await mcp_client.call_tool("research_workflow", {
        "topic": "async test",
        "max_sources": 3,
        "research_depth": "basic"
    })

    duration = time.time() - start_time
    assert duration < 30  # Should complete within reasonable time
    assert result.content
```

### Mocking External APIs

```python
import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_trends_with_mock(mcp_client):
    """Test trends functionality with mocked Google Trends API."""

    # Mock the GoogleTrendsAPI
    with patch('src.core.trends.api.GoogleTrendsAPI.search_trends') as mock_search:
        # Configure mock to return sample data
        mock_search.return_value = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'value': [50, 60]
        })

        result = await mcp_client.call_tool("search_trends", {
            "keywords": ["test"],
            "timeframe": "today 7-d"
        })

        assert result.content
        mock_search.assert_called_once()
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_full_research_workflow(mcp_client):
    """Test complete research workflow integration."""

    # Mock external dependencies
    with patch('src.core.trends.api.GoogleTrendsAPI.search_trends') as mock_trends, \
         patch('src.core.search.api.DuckDuckGoAPI.search') as mock_search:

        # Configure mocks
        mock_trends.return_value = pd.DataFrame({'test': [1, 2, 3]})
        mock_search.return_value = {"results": [], "content": "test content"}

        # Test the full workflow
        result = await mcp_client.call_tool("research_workflow", {
            "topic": "integration test",
            "max_sources": 2,
            "include_trends": True,
            "include_website_analysis": False,
            "enable_ai_insights": False
        })

        assert result.content
        content = result.content[0].text

        # Verify workflow completed
        assert "research_20" in content  # Research ID
        assert "Integration test" in content  # Topic
```

### Performance Testing

```python
@pytest.mark.asyncio
async def test_performance_regression(mcp_client):
    """Test for performance regressions."""

    import time

    start_time = time.time()

    result = await mcp_client.call_tool("academic_search", {
        "query": "performance test",
        "max_results": 3
    })

    duration = time.time() - start_time

    # Should complete within 10 seconds
    assert duration < 10.0, f"Query took {duration:.2f}s, expected < 10.0s"

    assert result.content
```

### Rate Limiting Testing

```python
@pytest.mark.asyncio
async def test_rate_limit_handling(mcp_client):
    """Test rate limit detection and handling."""

    # Mock API to return rate limit error
    with patch('src.core.trends.api.GoogleTrendsAPI.search_trends') as mock_search:
        # First call - rate limit error
        mock_search.side_effect = [
            Exception("429 Too Many Requests"),  # First call fails
            pd.DataFrame({'success': [1]})       # Retry succeeds
        ]

        result = await mcp_client.call_tool("search_trends", {
            "keywords": ["rate limit test"],
            "timeframe": "today 1-d"
        })

        # Should eventually succeed after retry
        assert result.content
        assert mock_search.call_count == 2  # Should have retried
```

### Test Configuration

```python
# conftest.py
import pytest
import asyncio
from fastmcp.client import Client
from server import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mcp_client():
    """Provide MCP client for tests."""
    async with Client(app) as client:
        yield client

# pytest.ini
[tool:pytest.ini_options]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --asyncio-mode=auto
    -v
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
```

### Best Practices

1. **Test Isolation**: Each test should be independent
2. **Mock External APIs**: Don't rely on real network calls
3. **Comprehensive Coverage**: Test success and failure paths
4. **Performance Monitoring**: Include timing assertions
5. **Async Testing**: Use pytest.mark.asyncio for async tests
6. **Error Scenarios**: Test error handling and edge cases

### When to Use This Skill
- Writing new tests for MCP tools
- Debugging test failures
- Setting up test infrastructure
- Reviewing test coverage and quality
- Optimizing test performance

Focus on creating reliable, maintainable tests that ensure MCP server quality and prevent regressions.