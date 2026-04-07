import openai
from app.config import OPENAI_API_KEY

def get_client():
    return openai.OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
أنت "مساعد سيتي ستارز" في خدمة عملاء المول.
رد بالمصري العامي فقط، قصير، مباشر، جملة أو جملتين.
ممنوع الفصحى والإنجليزي.

معلومات المول:
- صيدلية العزبي في الدور الأول.
- السينما في الدور الخامس.
- المصلى في الأرضي والرابع.
- سعودي ماركت في الدور الأرضي.
- لبس الأطفال في الدور التاني.

لو خارج المعلومات دي: "والله يا فندم معنديش معلومة أكيدة، اسأل الاستعلامات."
"""

def generate_response(transcript: str, history: list) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": transcript})

    client = get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=512,
        temperature=0.7,
    )
    return response.choices[0].message.content