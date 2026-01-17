# OpenCode Configuration for RivalSearchMCP

This directory contains specialized agents and skills for developing and maintaining the RivalSearchMCP server.

## 🚀 Getting Started

The OpenCode configuration is automatically loaded when you work in this project directory. You can switch between agents using `Tab` or invoke subagents with `@agent-name`.

## 🤖 Available Agents

### Primary Agent
- **`mcp-developer`** - Primary agent for general MCP server development and maintenance
  - Full access to all development tools
  - Specialized knowledge of FastMCP, OpenRouter, and PyTrends
  - Professional rate limiting and error handling expertise

### Subagents
- **`@tool-developer`** - Specialized in creating new MCP tools
  - Focus on FastMCP patterns, validation, and documentation
  - Expert in async/await patterns and context management

- **`@testing-specialist`** - Comprehensive testing and quality assurance
  - pytest patterns, mocking, integration testing
  - Performance regression testing and coverage analysis

- **`@code-reviewer`** - Code quality and security auditing
  - Security best practices, performance analysis
  - MCP protocol compliance and standards adherence

- **`@performance-specialist`** - Performance monitoring and optimization
  - Response time optimization, memory management
  - Concurrent processing and load testing

## 🛠️ Available Skills

Skills provide reusable knowledge that agents can access on-demand:

- **`mcp-tool-development`** - Best practices for FastMCP tool development
- **`api-rate-limiting`** - Professional API rate limiting patterns
- **`testing-patterns`** - Comprehensive testing strategies for MCP servers
- **`performance-optimization`** - Performance monitoring and optimization techniques

## 📋 Usage Examples

### General Development
```bash
# Use primary agent for general tasks
opencode "Add a new research tool for social media analysis"
```

### Specialized Tasks
```bash
# Use tool developer for new tools
opencode "@tool-developer Create a Twitter search tool"

# Use testing specialist for comprehensive testing
opencode "@testing-specialist Add tests for the new academic search tool"

# Use code reviewer for quality assurance
opencode "@code-reviewer Review the new tool implementation"

# Use performance specialist for optimization
opencode "@performance-specialist Optimize the research workflow response time"
```

### Using Skills
```bash
# Agents automatically access relevant skills
opencode "@tool-developer Create a new MCP tool following best practices"
# Agent will load mcp-tool-development skill automatically
```

## ⚙️ Configuration

The agents are configured in `.opencode/opencode.json` with:

- **Temperature settings** optimized for each agent's purpose
- **Tool permissions** ensuring safe, controlled development
- **Model selection** using Claude Sonnet for complex reasoning
- **Rate limiting** and safety permissions

## 🔧 Customization

### Adding New Agents
1. Create a new markdown file in `.opencode/agent/`
2. Configure permissions and tools in `.opencode/opencode.json`
3. Test the agent configuration

### Creating Skills
1. Create a new directory in `.opencode/skill/`
2. Add a `SKILL.md` file with frontmatter and detailed instructions
3. Skills are automatically discovered by agents

## 📊 Agent Capabilities

| Agent | Primary Focus | Tools | Permissions |
|-------|---------------|-------|-------------|
| mcp-developer | Full development | All tools | Ask for destructive ops |
| tool-developer | Tool creation | Write/Edit/Read | Ask for changes |
| testing-specialist | Quality assurance | Test tools | Allow testing |
| code-reviewer | Quality auditing | Read-only | No modifications |
| performance-specialist | Optimization | Monitoring tools | No modifications |

## 🎯 Best Practices

1. **Use appropriate agents** for specific tasks
2. **Leverage skills** for consistent implementation patterns
3. **Ask for permission** before making significant changes
4. **Test thoroughly** using the testing specialist
5. **Review code** with the code reviewer before committing

## 🔍 Troubleshooting

- **Agent not responding**: Check `.opencode/opencode.json` syntax
- **Skills not loading**: Verify `SKILL.md` frontmatter format
- **Permission denied**: Adjust permissions in agent configuration
- **Tool unavailable**: Check tool configuration for the agent

This setup provides a comprehensive development environment tailored specifically for RivalSearchMCP server development and maintenance.