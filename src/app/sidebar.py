import streamlit as st

# ------------------------------------------------------- Sidebar
def draw_sidebar():
    st.sidebar.header('📋 TODO')

    now_box = st.sidebar.container(border=True)
    next_box = st.sidebar.container(border=True)
    later_box = st.sidebar.container(border=True)
    with now_box:
        st.subheader("Now")

        st.checkbox(
            "[Feature] URL scraper",
            key="task6")
        st.checkbox(
            "[Bug] Session state doesn't save. https://github.com/Mohamed-512/Extra-Streamlit-Components",
            key="task1")

        st.markdown(" ")
    with next_box:
        st.subheader("Next")
        
        st.checkbox(
            "[Aesthetic] Chat window height should fill the screen height",
            key="task4")
        st.checkbox(
            "[Bug] AI text disappears if interrupted",
            key="task2")
        st.checkbox(
            "[Feature] Ollama API",
            key="task5")
        
        st.markdown(" ")
    with later_box:
        st.subheader("Later")

        st.checkbox(
            "[Feature] PDF upload",
            key="task7")
        
        st.checkbox(
            "[Feature] Pause/play button: for Audio",
            key="task3")
        st.checkbox(
            "[Feature] Pause/play button: for Text",
            key="task8")
        
        st.markdown(" ")