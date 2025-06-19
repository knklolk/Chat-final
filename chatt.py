import streamlit as st
from groq import Groq

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192']

def configurar_pagina():
    st.set_page_config(page_title='Mi primer chatbot con Python')
    st.title('Bienvenidos')

def crear_cliente_groq():
    groq_api_key = 'GROQ_API_KEY'
    return groq.Groq(api_key=groq_api_key)


def mostrar_sidebar():
    st.sidebar.title("Elegí tu modelo de IA")
    modelo = st.sidebar.selectbox('Elegí tu modelo', MODELOS, index=0, key="modelo_selectbox")
    st.write(f'**Modelo seleccionado:** {modelo}')
    return modelo

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

def obtener_mensaje_usuario():
    return st.chat_input("Enviá tu mensaje")

def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content if respuesta.choices else "No hubo respuesta del modelo."

def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()
    inicializar_estado_chat()
    obtener_mensajes_previos()

    mensaje_usuario = obtener_mensaje_usuario()
    if mensaje_usuario:
        agregar_mensajes_previos("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        mensaje_modelo = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        agregar_mensajes_previos("assistant", mensaje_modelo)
        mostrar_mensaje("assistant", mensaje_modelo)

if __name__ == '__main__':
    ejecutar_chat()

