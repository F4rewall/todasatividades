import openai

openai.api_key = "SUA_CHAVE_AQUI"

def conversar_com_openai(pergunta):
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pergunta}],
            temperature=0.7
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"[Erro] {str(e)}"