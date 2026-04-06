# import json
# import redis.asyncio as aioredis
# from app.config import REDIS_URL
# from app.stt import transcribe
# from app.llm import generate_response
# from app.tts import synthesize

# redis = aioredis.from_url(REDIS_URL)

# async def run_pipeline(audio_bytes: bytes, session_id: str) -> tuple[bytes, str]:
#     # 1. Load conversation history from Redis
#     history_raw = await redis.get(f"session:{session_id}")
#     history = json.loads(history_raw) if history_raw else []

#     # 2. Speech → Text
#     transcript = transcribe(audio_bytes)

#     # 3. Text → LLM reply
#     reply_text = generate_response(transcript, history)

#     # 4. Reply text → Voice
#     reply_audio = synthesize(reply_text)

#     # 5. Save updated history (keep last 8 turns = 16 messages)
#     history.extend([
#         {"role": "user",      "content": transcript},
#         {"role": "assistant", "content": reply_text},
#     ])
#     await redis.setex(
#         f"session:{session_id}",
#         3600,                          # expires after 1 hour
#         json.dumps(history[-16:])
#     )

#     return reply_audio, transcript
from app.stt import transcribe
from app.llm import generate_response
from app.tts import synthesize

# Simple in-memory storage instead of Redis
sessions = {}

async def run_pipeline(audio_bytes: bytes, session_id: str) -> tuple[bytes, str]:
    # Load conversation history from memory
    history = sessions.get(session_id, [])

    # Speech → Text
    transcript = transcribe(audio_bytes)

    # Text → LLM reply
    reply_text = generate_response(transcript, history)

    # Reply text → Voice
    reply_audio = synthesize(reply_text)

    # Save updated history (keep last 8 turns = 16 messages)
    history.extend([
        {"role": "user",      "content": transcript},
        {"role": "assistant", "content": reply_text},
    ])
    sessions[session_id] = history[-16:]

    return reply_audio, transcript