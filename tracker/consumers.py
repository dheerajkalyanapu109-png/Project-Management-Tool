from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ProjectConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user, pid = self.scope["user"], self.scope["url_route"]["kwargs"]["pid"]
        if not user.is_authenticated or not await self.is_member(user, pid):
            return await self.close()
        self.group = f"project_{pid}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        if hasattr(self, "group"): await self.channel_layer.group_discard(self.group, self.channel_name)
    async def changed(self, event): await self.send_json({"type": "changed"})
    @database_sync_to_async
    def is_member(self, user, pid): return user.projects.filter(pk=pid).exists()

class NotifyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated: return await self.close()
        self.group = f"user_{user.id}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        if hasattr(self, "group"): await self.channel_layer.group_discard(self.group, self.channel_name)
    async def notify(self, event): await self.send_json(event["data"])
