import streamlit as st
import pandas as pd
from openai import OpenAI

# Streamlit 앱 제목
st.title("고객 특성 기반 IPTV 추천 토크 생성기")
st.write("Made with [gptonline.ai/ko](https://gptonline.ai/ko/)")

# API 키 입력
api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

# 고객 특성 매핑
mean1_to_template = {
    "기가인터넷 사용": "고속 인터넷을 사용 중이니 IPTV 이용에 적합합니다.",
    "데이터 사용량 많음": "인터넷 사용량이 많은 편이라 IPTV 이용에 적합합니다.",
    "와이파이 사용": "SK 와이파이를 사용 중이시라면 IPTV도 함께 이용하시기 좋아요.",
    "윙즈 사용": "윙즈를 이미 이용 중이라 IPTV 연결도 원활하게 이용 가능합니다.",
    "장기고객": "장기간 이용 고객님께는 IPTV 추가 시 혜택도 더해드립니다.",
    "재약정함": "재약정을 하셨다면 IPTV 추가 시 추가 혜택을 적용받을 수 있습니다."
}

# 프롬프트 생성 함수
def build_interactive_prompt(mean1_list, mean2_list):
    mean1_str = "\n- " + "\n- ".join(mean1_list)
    mean2_str = "\n- " + "\n- ".join(mean2_list)

    return f"""
고객 특성:{mean1_str}

추천 근거:{mean2_str}

- 친절하지만 전문가답고, 과하게 영업티는 나지 않게 해줘.
- 반드시 추천 근거만 활용하고, 가족, 여가, 취향 등 추가적인 부가 설명은 넣지 마.
- 입력된 특성을 반복해서 언급하지 말고, 중복된 내용은 한 번만 언급해.
- 문장은 간결하게, 2문장 이내로 작성해.
- 반드시 고객의 특성과 추천 이유 내에 명시된 내용만 활용해 문장을 작성할 것
- 입력한 고객 특성을 모두 사용해 줘
"""

# GPT-4o-mini와 대화하는 함수
def chat_with_gpt4omini(prompt, api_key, max_tokens=150):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 sk 브로드 밴드 sales 매니저이고 고객에게 iptv를 가입 추천하려는게 목적이야"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.01
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"에러 발생: {str(e)}"

# 입력창
user_input = st.text_input("고객 특성을 입력하세요 (쉼표로 구분)")

if st.button("추천 토크 생성하기"):
    if not api_key:
        st.error("API 키를 입력해주세요.")
    elif not user_input:
        st.error("고객 특성을 입력해주세요.")
    else:
        mean1_list = [x.strip() for x in user_input.split(",")]
        mean2_list = [mean1_to_template.get(k, "적합한 추천 이유") for k in mean1_list]
        prompt = build_interactive_prompt(mean1_list, mean2_list)
        response = chat_with_gpt4omini(prompt, api_key)

        st.subheader("[Sales Talk]")
        st.success(response)
        st.write("-" * 50)

st.write("\nPowered by [gptonline.ai/ko](https://gptonline.ai/ko/)")
