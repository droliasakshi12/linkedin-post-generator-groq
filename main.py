import streamlit as st 
from few_shot_post import fewshot
from post_generation import generate_post 

def main():
    st.title("LINKDIN POST GENERATOR")
    col1,col2,col3 = st.columns(3)
    with col1:
        fs = fewshot()
        select_tags = st.selectbox("TOPIC",options = fs.get_unique_tags())
    with col2:
        select_length = st.selectbox("LENGTH",options =['Short','Medium','Long'])
    with col3:
        select_language = st.selectbox("LANGUAGE",options = ['English','Hinglish'])

    generate_button = st.button("GENERATE")

    if generate_button:
        post = generate_post(select_language,select_length,select_tags)
        st.write(post)



if __name__ == "__main__":
    main()