---
name: api-rate-limiting
description: Professional API rate limiting patterns for external services like Google Trends, OpenRouter, and web APIs
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: performance
---

## Professional API Rate Limiting Patterns

### Core Principles
1. **Respect API Limits**: Never exceed documented rate limits
2. **Exponential Backoff**: Implement smart retry with increasing delays
3. **Request Tracking**: Monitor usage and predict limit approaches
4. **Graceful Degradation**: Handle rate limits without breaking functionality
5. **User Transparency**: Inform users about rate limiting when appropriate

### Implementation Pattern

```python
class ProfessionalAPILimiter:
    def __init__(self):
        self.last_request_time = None
        self.request_count = 0
        self.rate_limit_hits = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests
        self.rate_limit_sleep = 60  # 60 seconds sleep when rate limited

    def _rate_limit_check(self):
        """Enforce rate limiting before making requests."""
        current_time = time.time()

        # Minimum interval enforcement
        if self.last_request_time:
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.min_request_interval:
                sleep_time = self.min_request_interval - time_since_last
                logger.debug(f"Rate limiting: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)

        # Exponential backoff for recent rate limit hits
        if self.rate_limit_hits > 0:
            sleep_time = min(
                self.rate_limit_sleep * (2 ** (self.rate_limit_hits - 1)),
                300  # Max 5 minutes
            )
            logger.warning(f"Rate limit protection: sleeping {sleep_time}s")
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_count += 1

    def _handle_rate_limit_error(self, error):
        """Detect and handle rate limit errors."""
        error_str = str(error).lower()
        if any(indicator in error_str for indicator in [
            '429', 'too many requests', 'rate limit', 'quota exceeded'
        ]):
            self.rate_limit_hits += 1
            logger.warning(f"Rate limit detected (hit #{self.rate_limit_hits})")
            return True
        return False

    def make_request(self, request_func, *args, **kwargs):
        """Make a rate-limited API request with automatic retry."""
        self._rate_limit_check()

        try:
            result = request_func(*args, **kwargs)
            # Reset rate limit counter on success
            self.rate_limit_hits = max(0, self.rate_limit_hits - 1)
            return result
        except Exception as e:
            if self._handle_rate_limit_error(e):
                # Retry once with fresh rate limiting
                logger.info("Retrying after rate limit handling...")
                self._rate_limit_check()
                try:
                    return request_func(*args, **kwargs)
                except Exception as retry_error:
                    logger.error(f"Retry also failed: {retry_error}")
                    raise retry_error
            else:
                raise e
```

### Google Trends Specific Handling

```python
# PyTrends requires special handling for initialization
def initialize_trends_client():
    """Initialize Google Trends client with proper error handling."""
    try:
        # Set SSL certificate path for some environments
        if 'REQUESTS_CA_BUNDLE' not in os.environ:
            try:
                import certifi
                os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
            except ImportError:
                pass

        # Initialize with only compatible parameters
        trendreq_kwargs = {
            "hl": "en-US",
            "tz": 360,
            "timeout": (10, 25),
            "retries": 3,
            "backoff_factor": 0.3,
        }

        # Only add proxies if available
        if proxies:
            trendreq_kwargs["proxies"] = proxies

        return TrendReq(**trendreq_kwargs)
    except Exception as e:
        if "NoneType" in str(e):
            logger.error("PyTrends initialization failed - likely proxy parameter issue")
        raise e
```

### Rate Limit Monitoring

```python
def get_rate_limit_status(self):
    """Get current rate limiting status for monitoring."""
    return {
        "request_count": self.request_count,
        "rate_limit_hits": self.rate_limit_hits,
        "last_request_time": self.last_request_time,
        "current_backoff_level": (
            self.rate_limit_sleep * (2 ** (self.rate_limit_hits - 1))
            if self.rate_limit_hits > 0 else 0
        ),
        "is_rate_limited": self.rate_limit_hits > 0,
    }
```

### Best Practices

#### 1. Service-Specific Limits
- **Google Trends**: ~1,400 requests per 4-hour window
- **OpenRouter**: Varies by model, monitor usage
- **Web APIs**: Check documentation for specific limits

#### 2. Error Detection
```python
RATE_LIMIT_INDICATORS = [
    '429', 'too many requests', 'rate limit exceeded',
    'quota exceeded', 'request rate exceeded'
]
```

#### 3. Backoff Strategy
- Start with 60 seconds on first hit
- Double delay for each subsequent hit
- Cap maximum delay (e.g., 5 minutes)
- Gradually reduce penalty after successful requests

#### 4. User Communication
```python
if self.rate_limit_hits > 0:
    await ctx.warning(
        f"Service is rate limited. Operations may be slower. "
        f"Please wait {estimated_delay}s before retrying."
    )
```

### When to Use This Skill
- Implementing new external API integrations
- Debugging rate limiting issues
- Optimizing API usage patterns
- Adding resilience to existing API calls
- Monitoring API usage and costs

Focus on creating robust, respectful API clients that maintain good relationships with service providers while providing reliable functionality to users.