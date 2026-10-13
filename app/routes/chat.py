from quart import Blueprint, Response, request, render_template
import asyncio, json, time

bp = Blueprint("main", __name__)

messages = []

# Condition() allows for a client to wait until something is produced rather than polling the endpoint repeatedly
cond = asyncio.Condition() # lets streams sleep

@bp.post("/send")
async def send():
    data = await request.get_json()
    async with cond:
        msg = {
                "id":   len(messages),
                "user": data.get("user") or "anon",
                "text": data["text"],
                "ts":   time.time(),
        }
        messages.append(msg)
        cond.notify_all() # wake every stream
    return "", 204 # 204 is successful with no content

@bp.get("/stream")
async def stream():
    last_id = int(request.headers.get("Last-Event-ID", -1))

    async def gen():
        nonlocal last_id

        while True:
            async with cond:
                try:
                    await asyncio.wait_for(
                        cond.wait_for(lambda: len(messages) > last_id + 1),
                        timeout = 15,
                    )
                except asyncio.TimeoutError:
                    pass
                new = messages[last_id + 1:]

            if not new:
                yield b": keepalive\n\n"
                continue

            for m in new:
                last_id = m["id"]
                yield f"id: {m['id']}\ndata: {json.dumps(m)}\n\n".encode()

    return Response(
        gen(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

@bp.get("/")
async def index():
    return await render_template("chat.html")
