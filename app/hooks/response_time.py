# app/hooks/response_time.py
import time

from sanic import Request

from app.utils.logger_utils import get_logger

logger = get_logger('Middleware')


async def add_start_time(request: Request):
    request.headers['start_time'] = time.time()


async def add_spent_time(request: Request, response):
    try:
        if 'start_time' in request.headers:
            timestamp = request.headers['start_time']
            spend_time = round((time.time() - timestamp), 3)
            response.headers['latency'] = spend_time

            msg = "{status} {method} {path} {query} {latency}s".format(
                status=response.status,
                method=request.method,
                path=request.path,
                query=request.query_string,
                latency=spend_time
            )
            if response.status >= 400:
                logger.error(msg)
            elif response.status >= 300:
                logger.warning(msg)
            else:
                logger.info(msg)
    except Exception as ex:
        logger.exception(ex)