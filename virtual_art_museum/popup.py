"""
===============================================
Popup.py
===============================================

This module contains a function for showing a popup on
the homepage that displays data from the aquisition pipeline.
It is kept out of mova_home.py for clarity

Functions
----------
    display_artwork_popup: Displays a popup with artwork details
Authors
----------
    Jennifer Kim and Madison Sanchez-Forman
"""
import streamlit as st
import requests

@st.dialog("Details")
def display_artwork_popup(artwork):
    """
    Display a popup with artwork details using Streamlit's dialog feature.
    No session state required.

    Parameters
    ----------
    artwork (dict): A dictionary containing artwork details

    Returns
    -------
    None
    """
    # markdown for styling the popup
    if artwork['Repository'] == "MET":
        st.image(artwork['image_url'], use_container_width=True)
        st.markdown(f"### {artwork['Title']}")
        st.markdown(f"**Artist:** {artwork['Artist']}")
        st.markdown(f"**Artist Bio:** {artwork['Artist biographic information']}")
        st.markdown(f"**Century:** {artwork['Century']}")
        st.markdown(f"**Medium:** {artwork.get('Medium', 'Unknown')}")
        st.markdown(f"**Culture:** {artwork.get('Culture', 'Unknown')}")
        st.markdown(f"**Dimensions**: {artwork.get('Dimensions')}")

    elif artwork['Repository'] == 'Europeana':
        st.image(artwork['image_url'], use_container_width=True)
        st.markdown(f"### {artwork['Title']}")
        st.markdown(f"**Artist:** {artwork['Artist']}")
        st.markdown(f"**Culture:** {artwork['Culture']}")
        st.markdown(f"**Description:** {artwork['Description']}")

    # Add a close button at the bottom
    if st.button("Close", key="close_popup"):
        st.rerun()