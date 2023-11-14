import requests
import streamlit as st
from requests.auth import HTTPBasicAuth

def send_request(url, proxy, auth=None, port=None):
    try:
        if port:
            proxy = f"{proxy}:{port}"
        proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
        response = requests.get(url, proxies=proxies, auth=auth)
        return response
    except requests.exceptions.RequestException as e:
        return str(e)

def load_proxy_list(filename):
    with open(filename, 'r') as f:
        proxies = f.read().splitlines()
    return proxies

def main():
    st.title("Web Search Proxy")
    
    url = st.text_input("Enter the URL")
    selected_proxies = st.multiselect("Select Proxy Server(s)", load_proxy_list("ProxyList.txt"))
    
    manual_auth = st.checkbox("Manual Authentication")
    if manual_auth:
        manual_username = st.text_input("Enter Proxy Username")
        manual_password = st.text_input("Enter Proxy Password", type="password")
        manual_auth = HTTPBasicAuth(manual_username, manual_password)
    
    manual_port = st.text_input("Enter Proxy Port (optional)")
    
    if st.button("Send Request"):
        for i, proxy in enumerate(selected_proxies):
            response = send_request(url, proxy, manual_auth, manual_port)
            st.write(response)
            if isinstance(response, str):
                st.write(f"Proxy {i + 1}:\nError: {response}")
            else:
                response_text = f"Proxy {i + 1}:\nStatus Code: {response.status_code}\n\n{response.text}"
                st.write(response_text)
                st.write(f"Status Code: {response.status_code}")
                st.write(f"Content: {response.text}")

if __name__ == "__main__":
    main()