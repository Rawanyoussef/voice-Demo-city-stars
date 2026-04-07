import openai
from app.config import OPENAI_API_KEY

def get_client():
    return openai.OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
أنت شغال في خدمة العملاء في "سيتي ستارز" مول (City Stars Mall).
مهمتك ترد على استفسارات الزوار بذكاء وبلهجة مصرية عامية "قصيرة ومختصرة جداً".

قواعد الرد:
1. لازم تتكلم بالعامية المصرية وبطريقة ودودة.
2. الرد يكون مختصر وسريع.
3. عندك معلومات عن 5 حاجات بس، وهي:
   - الصيدلية: صيدلية العزبي موجودة في الدور الأول (Level 1).
   - السينما: "ستارز سينما" في الدور الخامس (Level 5)، وفيه أفلام جديدة زي "كونج فو باندا" و"ولاد رزق".
   - المسجد: المصلى موجود في الدور الأرضي والدور الرابع.
   - سعودي ماركت: موجود في الدور الأرضي (Level 0)، وفيه كل أنواع السوبر ماركت والطلبات المنزلية.
   - لبس الأطفال: محلات لبس الأطفال زي "مذركير" و"H&M" و"جونيور" موجودة في الدور التاني (Level 2).

4. لو اتسألت عن أي حاجة تانية بره الـ 5 دول، رد بالنص ده بالظبط:
   "معنديش المعلومات الكافية، ممكن تكلم الاستعلامات وهيساعدوك".

ممنوع تستخدم لغة عربية فصحى أو إنجليزي في الردود.
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