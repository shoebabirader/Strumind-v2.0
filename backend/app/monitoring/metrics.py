from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# Define metrics
api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

active_users = Gauge('active_users', 'Number of active users')
ml_predictions_total = Counter('ml_predictions_total', 'Total ML predictions', ['model_type'])
analysis_runs_total = Counter('analysis_runs_total', 'Total analysis runs', ['analysis_type'])

def track_time(metric_name: str):
    """Decorator to track execution time"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            duration = time.time() - start
            api_request_duration.labels(method='POST', endpoint=metric_name).observe(duration)
            return result
        return wrapper
    return decorator
