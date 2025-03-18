import streamlit as st

#add after line 135 and line 145 in mova_home
def display_image(data, i):
    #st.image(data.iloc[i, 5])
    caption = data.iloc[i, 0]
    artist = data.iloc[i, 1]
    year = data.iloc[i, 2]
    image = data.iloc[i, 5]
    st.markdown(
        f"""
        <div style="text-align: center;">
        <img src="{image}" style="width: 100%; max-width: 800px;"/>
        <p>{caption}, {artist}, {year}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(f"View details", key=f"button_{i}"):
        st.session_state["selected_image"] = image
        st.session_state["selected_title"] = caption 
        st.session_state["selected_author"] = artist
        st.session_state["selected_year"] = year
        st.session_state["show_modal"] = True  # Open the pop-up
        st.rerun()  # Refresh UI to prevent double rendering
 
# Add in line 148 in mova_home with no indentation
def display_popup(data, image):
    if st.session_state.get("show_modal", False):
        image = st.session_state["selected_image"]
        title = st.session_state["selected_title"]
        author = st.session_state["selected_author"]
        year = st.session_state["selected_year"]

        image_data = data[data['image'] == image]
        
        if image_data.empty:
            st.warning("Image not found.")
            return None
        
        medium = image_data['medium'].values[0]
        region = image_data['region'].values[0]
        
        st.markdown(
            f"""
            <div style="text-align: center; position: relative;">
                <button style="position: absolute; top: 10px; right: 10px; background-color: skyblue; color: white; border: none; padding: 10px; cursor: pointer; border-radius: 5px;">X</button>
                <img src="{image}" style="width: 100%; max-width: 800px;"/>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.write(f"### **{title}**")
        st.write(f"#### **By {author}, {year}**")
        st.write(f"Medium: {medium}")
        st.write(f"Region: {region}")

        # "Close" button (Fully resets state and refreshes UI)
        if st.button("Close"):
            st.session_state["show_modal"] = False  
            st.session_state["selected_image"] = None
            st.session_state["selected_title"] = ""
            st.session_state["selected_author"] = ""
            st.session_state["selected_year"] = ""
            st.rerun()  # Forces UI refresh to show images again