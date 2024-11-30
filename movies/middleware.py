import redis
from django.conf import settings
# import threading


class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
    
    def __call__(self, request):
        self.redis_client.incr('request_count')
        
        response = self.get_response(request)
        return response




# request_count = 0

# counter_lock = threading.Lock()

# class RequestCountMiddleware:

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         global request_count
#         with counter_lock:
#             request_count += 1

#         response = self.get_response(request)
#         return response
