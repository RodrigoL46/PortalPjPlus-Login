# IMPORTING LIBRARIES
import os
from numpy import void
import streamlit as st
import asyncio
# https://frankie567.github.io/httpx-oauth/oauth2/
from httpx_oauth.clients.google import GoogleOAuth2
from dotenv import load_dotenv

load_dotenv('.env')

CLIENT_ID = st.secrets["google-clientId"]
CLIENT_SECRET = st.secrets["google-clientSecret"]
REDIRECT_URI = st.secrets["google-redirectUrl"]


async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["profile", "email"])
    return authorization_url


async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str):
    token = await client.get_access_token(code, redirect_uri)
    return token


async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def get_login_str():
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    authorization_url = asyncio.run(
        get_authorization_url(client, REDIRECT_URI))
    st.image('logos/rationiric.png', width=250)
    st.markdown("---")
    return f''' <a target = "_self" href = "{authorization_url}"> Google login </a> '''


def display_user() -> void:
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    # get the code from the url
    code = st.experimental_get_query_params()['code']
    token = asyncio.run(get_access_token(
        client, REDIRECT_URI, code))
    user_id, user_email = asyncio.run(
        get_email(client, token['access_token']))
    st.write(
        f"You're logged in as {user_email} and id is {user_id}")
