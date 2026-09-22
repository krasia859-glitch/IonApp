import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Ион — Ваш ИИ-ассистент",
    page_icon="icon.png", 
    layout="centered",
)

col1, col2 = st.columns([1, 8])
with col1:
  st.image("icon.png", width=65)
with col2:
  st.title("Ион")
st.write("Ваш персональный интеллектуальный ассистент с доступом к сети.")

st.sidebar.header("🔑 Настройки API")
api_key = st.secrets.get("OPENROUTER_API_KEY") or st.sidebar.text_input(
    "API-ключ OpenRouter", type="password"
)
base_url = st.sidebar.text_input(
    "Базовый URL", value="https://openrouter.ai/api/v1"
)
model_name = st.sidebar.text_input(
    "Название модели", value="openrouter/free"
)

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Очистить историю чата"):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напишите ваш запрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    llm_messages = [
        {
            "role": "system",
            "content": (
                "Ты — Ион, полезный, вежливый и умный персональный ИИ-ассистент."
            ),
        }
    ]
    for m in st.session_state.messages:
        llm_messages.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        ai_response = ""
        try:
            if not api_key:
                raise ValueError("Не указан API-ключ OpenRouter в боковой панели!")

            client = OpenAI(api_key=api_key, base_url=base_url.strip())

            with st.spinner("Ion думает над ответом..."):
                response = client.chat.completions.create(
                    model=model_name, messages=llm_messages
                )
                ai_response = response.choices[0].message.content
        except Exception as e:
            ai_response = f"❌ Произошла ошибка при обращении к API модели: {e}"

        st.markdown(ai_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response}
        )