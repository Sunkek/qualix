import ssl
import aiohttp
import tempfile
import os
from django.conf import settings

class JRPCController:

    def __init__(self):
        self.api_url = settings.JSON_RPC_API_URL
        self.api_cert = settings.JSON_RPC_API_CERT
        self.api_key = settings.JSON_RPC_API_KEY
        self.aiohttp_session = None

    def create_connector(self):
        # Because ssl requires the paths to certificate and key files and not
        # file contents themselves, I have to create temporary files with them,
        # use those files to create SSL and then delete the files
        certfile = tempfile.NamedTemporaryFile(delete=False)
        certfile.write(self.api_cert.encode("utf-8"))
        certfile.close()
        keyfile = tempfile.NamedTemporaryFile(delete=False)
        keyfile.write(self.api_key.encode("utf-8"))
        keyfile.close()
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.load_cert_chain(certfile.name, keyfile.name)
        conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
        os.remove(certfile.name)
        os.remove(keyfile.name)
        return conn

    async def create_aiohttp_session(self):
        conn = self.create_connector()
        self.aiohttp_session = aiohttp.ClientSession(connector=conn)

    async def post_jrpc(self, payload):
        if not self.aiohttp_session:
            # Find a better way to initialize the session
            await self.create_aiohttp_session()
        elif not self.aiohttp_session.loop.is_running():
            # Somehow the loop dies after each request. Why?
            await self.aiohttp_session.close()
            await self.create_aiohttp_session()
        return await self.aiohttp_session.post(self.api_url, json=payload)
    
    async def test(self):
        payload = {
            "method": "auth.check",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        return await self.post_jrpc(payload)