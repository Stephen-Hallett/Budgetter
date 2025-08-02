import os
from datetime import datetime

import pytz
import requests
import streamlit as st

st.set_page_config(page_title="Budgetter", layout="wide")


def set_state() -> None:
    now = datetime.now(tz=pytz.timezone("Pacific/Auckland"))
    if "today" not in st.session_state:
        st.session_state.today = now.date()
    if "start_date" not in st.session_state:
        st.session_state.start_date = now.replace(day=1).date()
    if "end_date" not in st.session_state:
        st.session_state.end_date = st.session_state.today
    if "username" not in st.session_state:
        st.session_state.username = "Stephen"  # TODO: Make this a user choice
    if "segments" not in st.session_state:
        st.session_state.segments = requests.get(
            f"{os.environ['HOST']}/segments/list",
            headers={"username": st.session_state.username},
            timeout=5,
        ).json()


def main() -> None:
    st.header("Budgetter")
    with st.container(border=True):
        filters_col, info_col = st.columns([3, 2])
        with filters_col:
            start_date_col, end_date_col, filters_col = st.columns([1, 1, 2])
            start_date_col.date_input(
                "Start Date:",
                format="DD/MM/YYYY",
                width=100,
                max_value=st.session_state.end_date,
                key="start_date",
            )
            end_date_col.date_input(
                "End Date:",
                format="DD/MM/YYYY",
                width=100,
                min_value=st.session_state.start_date,
                max_value=st.session_state.today,
                key="end_date",
            )
            filters_col.multiselect("Filters", [])
    trans_col, seg_col, plot_col = st.columns([3, 1, 2])
    with trans_col, st.container(border=True):
        st.subheader("Transactions")

    with seg_col, st.container(border=True):
        st.subheader("Segments")
        st.write(st.session_state.segments)

    with plot_col, st.container():
        metric1, metric2 = st.columns(2)
        metric1.metric("You Spent", "$69.00", border=True)
        metric2.metric("Of Monthly Income", "12.0%", border=True)


if __name__ == "__main__":
    set_state()
    main()
