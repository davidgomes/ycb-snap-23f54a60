import asyncio
import threading

from asgiref.sync import async_to_sync

from django.contrib.sessions.middleware import SessionMiddleware
from django.db import connection
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.middleware.cache import (
    CacheMiddleware, FetchFromCacheMiddleware, UpdateCacheMiddleware,
)
from django.middleware.common import CommonMiddleware
from django.middleware.security import SecurityMiddleware
from django.test import SimpleTestCase
from django.utils.deprecation import MiddlewareMixin, RemovedInDjango40Warning


class MiddlewareMixinTests(SimpleTestCase):
    """
    Deprecation warning is raised when using get_response=None.
    """
    msg = 'Passing None for the middleware get_response argument is deprecated.'

    def test_deprecation(self):
        with self.assertRaisesMessage(RemovedInDjango40Warning, self.msg):
            CommonMiddleware()

    def test_passing_explicit_none(self):
        with self.assertRaisesMessage(RemovedInDjango40Warning, self.msg):
            CommonMiddleware(None)

    def test_subclass_deprecation(self):
        """
        Deprecation warning is raised in subclasses overriding __init__()
        without calling super().
        """
        for middleware in [
            SessionMiddleware,
            CacheMiddleware,
            FetchFromCacheMiddleware,
            UpdateCacheMiddleware,
            SecurityMiddleware,
        ]:
            with self.subTest(middleware=middleware):
                with self.assertRaisesMessage(RemovedInDjango40Warning, self.msg):
                    middleware()

    def test_sync_to_async_uses_base_thread_and_connection(self):
        """
        The process_request() and process_response() hooks must be called with
        the sync_to_async thread_sensitive flag enabled, so that database
        operations use the correct thread and connection.
        """
        def request_lifecycle():
            """Fake request_started/request_finished."""
            return (threading.get_ident(), id(connection))

        async def get_response(self):
            return HttpResponse()

        class SimpleMiddleWare(MiddlewareMixin):
            def process_request(self, request):
                request.thread_and_connection = request_lifecycle()

            def process_response(self, request, response):
                response.thread_and_connection = request_lifecycle()
                return response

        threads_and_connections = []
        threads_and_connections.append(request_lifecycle())

        request = HttpRequest()
        response = async_to_sync(SimpleMiddleWare(get_response))(request)
        threads_and_connections.append(request.thread_and_connection)
        threads_and_connections.append(response.thread_and_connection)

        threads_and_connections.append(request_lifecycle())

        self.assertEqual(len(threads_and_connections), 4)
        self.assertEqual(len(set(threads_and_connections)), 1)

    def test_async_capable_middleware_passes_response_not_coroutine(self):
        """
        Built-in middleware that override __init__() must still enter async
        mode. Otherwise the middleware outside them receives a coroutine in
        process_response() under ASGI.
        """
        async def get_response(request):
            return HttpResponse('ok')

        class Outer(MiddlewareMixin):
            def process_response(self, request, response):
                self.response_type = type(response)
                return response

        for middleware_class in [
            SecurityMiddleware,
            UpdateCacheMiddleware,
            FetchFromCacheMiddleware,
            CacheMiddleware,
        ]:
            with self.subTest(middleware=middleware_class):
                inner = middleware_class(get_response)
                self.assertIs(
                    getattr(inner, '_is_coroutine', None),
                    asyncio.coroutines._is_coroutine,
                )
                outer = Outer(inner)
                request = HttpRequest()
                response = async_to_sync(outer)(request)
                self.assertIs(outer.response_type, HttpResponse)
                self.assertIsInstance(response, HttpResponse)
