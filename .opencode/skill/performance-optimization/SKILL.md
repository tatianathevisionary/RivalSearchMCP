---
name: performance-optimization
description: Performance monitoring, optimization techniques, and benchmarking for MCP servers
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: performance
---

## MCP Server Performance Optimization

### Key Performance Metrics

1. **Response Time**: Tool calls should complete within 5-10 seconds
2. **Memory Usage**: Monitor for memory leaks and efficient resource usage
3. **Concurrent Requests**: Support multiple simultaneous users
4. **API Efficiency**: Minimize external API calls and optimize usage
5. **Startup Time**: Fast server initialization and tool registration

### Performance Monitoring

```python
import time
import psutil
import asyncio
from contextlib import asynccontextmanager

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'requests_total': 0,
            'requests_failed': 0,
            'avg_response_time': 0,
            'peak_memory_usage': 0,
            'active_connections': 0
        }

    @asynccontextmanager
    async def measure_request(self, request_name: str):
        """Context manager to measure request performance."""
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

        try:
            self.metrics['active_connections'] += 1
            yield
        finally:
            duration = time.time() - start_time
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            memory_delta = end_memory - start_memory

            self.metrics['requests_total'] += 1
            self.metrics['avg_response_time'] = (
                (self.metrics['avg_response_time'] * (self.metrics['requests_total'] - 1)) + duration
            ) / self.metrics['requests_total']

            self.metrics['peak_memory_usage'] = max(
                self.metrics['peak_memory_usage'], end_memory
            )

            logger.info(f"Request {request_name}: {duration:.2f}s, Memory: {memory_delta:+.1f}MB")
            self.metrics['active_connections'] -= 1

    def get_metrics(self):
        """Get current performance metrics."""
        return self.metrics.copy()
```

### Async Optimization Patterns

#### 1. Concurrent API Calls
```python
async def fetch_multiple_sources(query: str) -> List[dict]:
    """Fetch data from multiple sources concurrently."""
    tasks = [
        fetch_google_trends(query),
        fetch_duckduckgo_results(query),
        fetch_academic_sources(query),
    ]

    # Execute all requests concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle results and exceptions
    successful_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.warning(f"Source {i} failed: {result}")
        else:
            successful_results.append(result)

    return successful_results
```

#### 2. Connection Pooling
```python
import aiohttp

class ConnectionPool:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            self.session = None

# Usage
async def make_api_call(url: str) -> dict:
    async with ConnectionPool() as session:
        async with session.get(url) as response:
            return await response.json()
```

#### 3. Smart Caching
```python
from functools import lru_cache
import asyncio
from typing import Dict, Any

class SmartCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache: Dict[str, Dict] = {}
        self.ttl = ttl_seconds

    def _is_expired(self, cache_entry: Dict) -> bool:
        return time.time() - cache_entry['timestamp'] > self.ttl

    def get(self, key: str) -> Any:
        if key in self.cache:
            entry = self.cache[key]
            if not self._is_expired(entry):
                return entry['data']
            else:
                del self.cache[key]
        return None

    def set(self, key: str, data: Any):
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }

    def clear_expired(self):
        """Remove expired cache entries."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time - entry['timestamp'] > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]

# Global cache instance
api_cache = SmartCache(ttl_seconds=600)  # 10 minutes

async def cached_api_call(key: str, api_func, *args, **kwargs):
    """Make cached API call."""
    cached_result = api_cache.get(key)
    if cached_result:
        logger.debug(f"Cache hit for {key}")
        return cached_result

    result = await api_func(*args, **kwargs)
    api_cache.set(key, result)
    return result
```

### Memory Management

```python
import gc
import weakref

class ResourceManager:
    def __init__(self):
        self.resources = set()

    def track_resource(self, resource):
        """Track a resource for cleanup."""
        self.resources.add(weakref.ref(resource, self._cleanup_resource))

    def _cleanup_resource(self, weak_ref):
        """Clean up when resource is garbage collected."""
        self.resources.discard(weak_ref)

    def force_cleanup(self):
        """Force cleanup of all tracked resources."""
        for ref in list(self.resources):
            resource = ref()
            if resource and hasattr(resource, 'close'):
                try:
                    if asyncio.iscoroutinefunction(resource.close):
                        # Schedule async cleanup
                        asyncio.create_task(resource.close())
                    else:
                        resource.close()
                except Exception as e:
                    logger.warning(f"Error closing resource: {e}")

        self.resources.clear()
        gc.collect()  # Force garbage collection
```

### Performance Profiling

```python
import cProfile
import pstats
from io import StringIO

def profile_function(func):
    """Decorator to profile function performance."""
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()

        result = func(*args, **kwargs)

        pr.disable()
        s = StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(10)  # Top 10 functions

        logger.info(f"Performance profile for {func.__name__}:\n{s.getvalue()}")
        return result
    return wrapper

# Usage
@profile_function
async def expensive_operation():
    # Your code here
    pass
```

### Load Testing

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

async def load_test_tool(client, tool_name: str, params: dict, num_requests: int = 10):
    """Load test a specific tool."""
    async def single_request(request_id: int):
        start_time = time.time()
        try:
            result = await client.call_tool(tool_name, params)
            duration = time.time() - start_time
            return {'success': True, 'duration': duration, 'request_id': request_id}
        except Exception as e:
            duration = time.time() - start_time
            return {'success': False, 'duration': duration, 'error': str(e), 'request_id': request_id}

    # Execute concurrent requests
    tasks = [single_request(i) for i in range(num_requests)]
    results = await asyncio.gather(*tasks)

    # Analyze results
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    avg_duration = sum(r['duration'] for r in successful) / len(successful) if successful else 0
    success_rate = len(successful) / num_requests * 100

    logger.info(f"Load test results for {tool_name}:")
    logger.info(f"  Success rate: {success_rate:.1f}%")
    logger.info(f"  Average response time: {avg_duration:.2f}s")
    logger.info(f"  Total requests: {num_requests}")
    logger.info(f"  Successful: {len(successful)}")
    logger.info(f"  Failed: {len(failed)}")

    return {
        'success_rate': success_rate,
        'avg_duration': avg_duration,
        'total_requests': num_requests,
        'successful': len(successful),
        'failed': len(failed),
        'results': results
    }
```

### Optimization Checklist

- [ ] **Async/Await**: All I/O operations are properly async
- [ ] **Connection Reuse**: HTTP connections are pooled and reused
- [ ] **Caching**: Expensive operations are cached appropriately
- [ ] **Memory Management**: Resources are properly cleaned up
- [ ] **Error Handling**: Errors don't break performance monitoring
- [ ] **Concurrent Processing**: Multiple requests can be handled simultaneously
- [ ] **Rate Limiting**: API calls respect rate limits with smart backoff
- [ ] **Profiling**: Performance bottlenecks are identified and addressed

### When to Use This Skill
- Optimizing slow-performing tools
- Debugging memory leaks or resource issues
- Implementing performance monitoring
- Conducting load testing and benchmarking
- Improving concurrent request handling
- Reducing API costs through smart caching

Focus on delivering fast, efficient MCP server tools that scale well and provide excellent user experience.