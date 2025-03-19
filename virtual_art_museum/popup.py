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
    st.markdown("""
        <style>
            .artwork-popup {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .artwork-image {
                width: 100%;
                max-height: 60vh;
                object-fit: contain;
            }
            .artwork-title {
                font-size: 24px;
                font-weight: bold;
                margin: 15px 0;
            }
            .artwork-details {
                font-size: 16px;
                color: #4A4A4A;
                margin: 10px 0;
            }
            .artwork-metadata {
                background-color: #F8F9FA;
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # container for the popup
    with st.container():
        # if the artwork is from the MET, display the following details
        if artwork['Repository'] == "MET":
            st.markdown(f"### {artwork['Title']}")
            st.markdown(f"**Artist:** {artwork['Artist']}")
            st.markdown(f"**Artist Bio:** {artwork['Artist biographic information']}")
            st.markdown(f"**Century:** {artwork['Century']}")
            st.markdown(f"**Medium:** {artwork.get('Medium', 'Unknown')}")
            st.markdown(f"**Culture:** {artwork.get('Culture', 'Unknown')}")
            st.markdown(f"**Dimensions**: {artwork.get('Dimensions')}")

        # if the artwork is from Europeana, display the following details
        elif artwork['Repository'] == 'Europeana':
            st.markdown(f"### {artwork['Title']}")
            st.markdown(f"**Artist:** {artwork['Artist']}")
            st.markdown(f"**Culture:** {artwork['Culture']}")
            st.markdown(f"**Description:** {artwork['Description']}")

        # close button
            if st.button("Close", key="close_popup"):
                st.rerun()
