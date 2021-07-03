from django.http import JsonResponse
from jsonrpc import JRPC

async def index(request):
    res = await JRPC.test()
    return JsonResponse(await res.json())