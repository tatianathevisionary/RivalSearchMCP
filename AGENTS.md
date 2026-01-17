# RivalSearchMCP Development Guidelines

## Project Overview
RivalSearchMCP is a FastMCP-based Python server providing advanced web research tools. It features anti-detection scraping, Google Trends analysis, content processing, and scientific research capabilities.

## Tech Stack
- **Language**: Python 3.9+ with async/await patterns
- **Framework**: FastMCP for MCP protocol implementation
- **Key Libraries**: httpx, cloudscraper, pytrends, aiohttp, pydantic
- **Testing**: pytest with async support, coverage reporting
- **Linting**: ruff for formatting and linting, mypy for type checking
- **Documentation**: MkDocs with custom theme

## Code Structure
- `src/tools/`: Modular tool implementations (search, trends, analysis, research)
- `src/routes/`: Custom FastMCP routes and endpoints
- `src/resources/`: MCP resource definitions
- `src/schemas/`: Pydantic models for data validation
- `src/utils/`: Helper utilities (parsing, clients, error handling)
- `tests/`: Comprehensive test suite with fixtures
- `docs/`: MkDocs documentation

## Development Standards
### Async Patterns
- All I/O operations must use async/await
- Use `asyncio.gather()` for concurrent requests
- Implement proper timeout handling (<30s for tools)

### Error Handling
- Use `ToolError` for user-facing errors
- Log unexpected errors with context
- Implement graceful degradation for API failures

### Tool Development
- Follow FastMCP @mcp.tool decorator patterns
- Use Annotated types with Field descriptions
- Always inject CurrentContext() for logging/progress
- Include comprehensive docstrings (Args/Returns/Raises)

### Testing
- Unit tests for all tools and utilities
- Integration tests for end-to-end workflows
- Mock external APIs (Google Trends, search engines)
- Aim for >90% coverage
- Test error scenarios and edge cases

### Performance
- Monitor response times (<5-10s for typical queries)
- Implement smart caching for expensive operations
- Use connection pooling for HTTP requests
- Profile memory usage and optimize resource cleanup

## MCP Compliance
- Adhere to MCP protocol standards
- Provide accurate tool descriptions
- Implement proper progress reporting
- Handle tool parameters validation
- Support cancellation and interruption

## Security
- Never log API keys or sensitive data
- Validate all user inputs before processing
- Implement rate limiting for external APIs
- Use secure defaults for scraping operations

## Workflow Patterns
1. **New Tool Development**: Use @tool-developer agent, follow patterns in SKILL.md
2. **Code Review**: Run /lint command, use @code-reviewer for analysis
3. **Testing**: Use /test command, review coverage reports
4. **Performance**: Use /perf command, analyze bottlenecks
5. **Documentation**: Update docs/ for new features

## Quality Gates
- All tests pass before commits
- Type checking passes (mypy)
- Linting passes (ruff)
- Documentation updated
- Performance benchmarks met

## Common Patterns
- Use `ctx.report_progress()` for long operations
- Implement retry logic with exponential backoff
- Cache results when appropriate
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)

## External Resources
When researching new tools or APIs:
- Use @web-research MCP server for documentation lookup
- Use @trends-api MCP server for market analysis
- Reference docs/examples/ for implementation patterns