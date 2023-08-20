import streamlit as st

import vizpage

st.set_page_config(page_title="Apartment Science", layout="centered")


# class MultiPage:
#     def __init__(self) -> None:
#         self.pages = []

#     def add_page(self, title, func) -> None:
#         self.pages.append({"title": title, "function": func})

#     def run(self):
#         # page = st.sidebar.selectbox("Pages", self.pages, format_func=lambda page: page["title"])
#         if page is not None:
#             page["function"]()


# app = MultiPage()
# app.add_page("Visualization", vizpage.app)
# app.run()

vizpage.app()

st.markdown(
    """
<style>
    #MainMenu {
        visibility: hidden
    }

    footer {
        visibility: hidden
    }
    
    .mapboxgl-control-container {
        visibility: hidden
    }

    .stMarkdown p {
        margin: 0;
    }
</style>
""",
    unsafe_allow_html=True,
)
