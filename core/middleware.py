import logging
import time


class RequestLatencyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        logger = logging.getLogger("django.request")
        latency = time.time() - start_time
        logger.info(f"Request to {request.path} took {latency:.4f} seconds.")
        return response


def simple_middleware(get_response):
    # One-time configuration and initialization.
    print("one time test")

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print("func middleware")
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
