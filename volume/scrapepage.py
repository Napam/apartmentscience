import streamlit as st


def app():
    st.markdown(
        """
    # Webscraping 101
    *Webscraping handler om å hente ut data fra nettsider og putte disse dataene inn i en samlet og strukturert format*
    """
    )

    st.markdown(""" ## Noen måter å gjøre det på """)

    with st.expander("Metode 1"):
        st.markdown(
            """
        ### CTRL+C &rarr; CTRL+V
        Webscraping trenger ikke å være automatisert ;)
        """
        )
        st.image("https://i.imgur.com/ZoKPU0I.jpeg")
        st.markdown(
            """
        **Pros**:
        - Lav terskel, krever ingen programmering
        - Får øvd på programmering
        **Cons**:
        - Tregt
        - Manuelt
        """
        )

    with st.expander("Metode 2"):
        st.markdown(
            """
        ### Trykke på "Last ned CSV" og lignende i sider som har det.

        E.g.
        """
        )
        st.download_button("Last ned CSV", data="bingbong", file_name="data.csv")
        st.markdown(
            """
        **Pros**:
        - Veldig fint om man bare kan bruke en nedlastningslink
        **Cons**:
        - Få sider har det
        """
        )

    with st.expander("Metode 3"):
        st.markdown(
            """
        ### HTML parsing
        ```html
        <table>
        <tr>
            <th>Company</th>
            <th>Contact</th>
            <th>Country</th>
        </tr>
        <tr>
            <td>Alfreds Futterkiste</td>
            <td>Maria Anders</td>
            <td>Germany</td>
        </tr>
        <tr>
            <td>Centro comercial Moctezuma</td>
            <td>Francisco Chang</td>
            <td>Mexico</td>
        </tr>
        </table>
        ```
        ```python
        from bs4 import BeautifulSoup
        with open("test.html", "r") as f:
            html = f.read()

        bs = BeautifulSoup(html, "html.parser")
        tds = bs.find_all("td")
        ```
        **Pros**:
        - Fungerer veldig generelt, så lenge du klarer å se det i nettleseren så vet du at du kan scrape det.

        **Cons**:
        - Kan bli mye å kode hvis HTMLen er vanskelig/rotete
        """
        )

    with st.expander("Metode 4"):
        st.markdown(
            """
        HTTP kall
        ```
        curl\\ 
        -d "param1=value1&param2=value2"\\
        -H "Content-Type: application/x-www-form-urlencoded"\\
        -X POST http://localhost:3000/data
        ```
        **Pros**:
        - Enkel å gjøre programmatisk, enkelt å automatisere
        - Respons er ofte enkelt å parse
        **Cons**:
        - Ikke alltid tilgjengelig
        - Kan være vanskelig å finne HTTP kall
        """
        )

    with st.expander("Metode 5"):
        st.markdown(
            """
        Computer Vision 
        """
        )
        st.image("https://miro.medium.com/max/2268/1*xg4e0_c-JRw26l0QcZhQ0g.png")
        st.markdown(
            """
        **Pros:**
        - Kan scrape mer spesifikke ting som bilder av bestemte ting, og evt scrape tekst fra bilder
        **Cons:**
        - Kan være tungt å prosessere
        """)

    with st.expander("Noe å tenke på"):
        st.markdown(
            """
        - Noen sider kan være vanskelige å scrape og å skaffe data fra.
            - Det kan bli problemer med autentisering etc
            - Veldig obfuskert

        En brute "brute force" metode å tvinge data til å vises er å bruke verktøy som:
        #### Selenium

        Det er et browser automatiserings verktøy som kan brukes for e.g. klikk testing i en browser (e.g. headless chromium)        
        <br/>
        Med det så kan man også skaffe authorization headers ganske enkelt 
        ```python
        from seleniumwire import webdriver

        driver = webdriver.Chrome()
        driver.get('https://www.google.com')

        # Access requests via the `requests` attribute
        for request in driver.requests:
            if request.response:
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type']
                )
        ```
        Ellers så kan man bruke en eller annen proxy
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    ## Eksempel fremgangsmåte
    https://www.elkjop.no/
    """
    )


if __name__ == "__main__":
    app()

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
