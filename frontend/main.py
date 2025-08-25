import os
from datetime import datetime

import plotly.express as px
import polars as pl
import pytz
import requests
import streamlit as st

st.set_page_config(page_title="Budgetter", layout="wide")


def update_segment(segment: dict) -> None:
    _ = requests.put(
        f"{os.environ['HOST']}/segments/update", json=segment, timeout=15
    ).json()


def make_colour_callback(segment: dict, key: str) -> callable:
    new_colour = st.session_state[key]
    segment["colour"] = new_colour
    update_segment(segment)


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
    if "trans_limit" not in st.session_state:
        st.session_state.trans_limit = 100
    if "offset" not in st.session_state:
        st.session_state.offset = 0


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
    trans_col, seg_col, plot_col = st.columns([2, 1, 3])
    with trans_col, st.container(border=True):
        st.subheader("Transactions")
        transactions = requests.get(
            f"{os.environ['HOST']}/summary/transactions",
            params={
                "limit": st.session_state.trans_limit,
                "offset": st.session_state.offset,
                "start_date": st.session_state.start_date,
                "end_date": st.session_state.end_date,
            },
            headers={"username": st.session_state.username},
            timeout=5,
        ).json()

        with st.container(height=800):
            for idx, trans in enumerate(transactions):
                left, right = st.columns([4, 1])
                with left:
                    st.markdown(
                        f"""
                        <div style="
                            display: flex;
                            flex-direction: row;
                            align-items: center;
                            border-left: 16px solid {trans.get("colour", "#ccc")};
                            background: #f9f9f9;
                            padding: 12px 16px;
                            margin-bottom: 10px;
                            border-radius: 10px;
                            box-shadow: 0 1px 2px rgba(0,0,0,0.07);
                        ">
                            <div style="flex: 1;">
                                <div style="font-size: 0.95em; color: #555;">
                                    <b>{trans.get("date", "")[:10]}</b>
                                </div>
                                <div style="margin: 4px 0 2px 0; font-size: 1.05em;">
                                    {trans.get("description", "")}
                                </div>
                                <div style="font-size: 0.85em; color: #888;">
                                    Segment ID: {trans.get("segment_id", "")}
                                </div>
                            </div>
                            <div style="display: flex; align-items: center; justify-content: center; min-width: 120px;">
                                <span style="font-size: 1.5em; font-weight: bold; color:{"#d20f39" if trans.get("amount", 0) < 0 else "#40a02b"};">
                                    ${abs(trans.get("amount", 0)):.2f}
                                </span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with right:
                    segment_names = [seg["name"] for seg in st.session_state.segments]
                    st.selectbox(
                        " ",
                        options=[seg["name"] for seg in st.session_state.segments],
                        placeholder=trans["segment"],
                        index=None
                        if not trans["confirmed"]
                        else segment_names.index(trans["segment"]),
                        key=f"trans_btn_{idx}",
                    )

    with seg_col, st.container(border=True):
        st.subheader("Segments")
        for idx, segment in enumerate(st.session_state.segments):
            with st.container():
                colour, name = st.columns([1, 4])
                colour_key = f"segment_colour_{idx}"
                with colour:
                    st.color_picker(
                        " ",
                        value=segment["colour"],
                        label_visibility="hidden",
                        key=colour_key,
                        on_change=make_colour_callback,
                        args=(segment, colour_key),
                    )
                with name:
                    st.markdown(f"\n\n#### {segment['name']}")

    with plot_col, st.container():
        transactions_df = pl.DataFrame(transactions)
        outgoing = transactions_df.filter(pl.col("amount") < 0)
        incoming = transactions_df.filter(pl.col("amount") > 0)
        spend = outgoing["amount"].sum() * -1
        income = incoming["amount"].sum()
        segmented = outgoing.group_by("segment", "colour").agg(
            pl.col("amount").sum() * -1
        )
        segmented_pd = segmented.to_pandas()
        segmented_pd["amount"] = segmented_pd["amount"].astype(float).fillna(0)

        fig = px.pie(
            segmented_pd,
            values="amount",
            names="segment",
            color="segment",
            color_discrete_map={
                row["segment"]: row["colour"] for _, row in segmented_pd.iterrows()
            },
            hole=0.4,  # 0 for pie, >0 for donut
            hover_data=["amount"],
            height=800,
        )
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Spend: $%{value:.2f}<br>Percent: %{percent}<extra></extra>",
            textinfo="percent",
            textfont_size=24,  # Make text inside the donut larger
        )
        fig.update_layout(
            margin={"t": 0, "b": 0, "l": 0, "r": 0},
            legend={
                "font": {"size": 30},
                "orientation": "h",  # Horizontal legend
                "yanchor": "bottom",
                "y": -0.15,  # Move legend below the chart
                "xanchor": "center",
                "x": 0.5,
            },
            hoverlabel={"font_size": 20},
        )

        st.plotly_chart(fig, use_container_width=True)

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("You Spent", f"${spend:.2f}", border=True)
        metric2.metric("You Earnt", f"${income:.2f}", border=True)
        metric3.metric(
            "Spending as a % of Income", f"{100 * spend / income:.2f}%", border=True
        )


if __name__ == "__main__":
    with open("style.css") as f:
        st.html(f"<style>{f.read()}</style>")
    set_state()
    main()
