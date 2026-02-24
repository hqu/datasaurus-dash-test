import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Datasaurus Dashboard", layout="wide")

st.title("🦕 Datasaurus Dozen — Interactive Dashboard")
st.markdown(
    "All shapes share nearly identical summary statistics (mean, std, correlation), "
    "yet look completely different. Select a shape to explore!"
)

@st.cache_data
def load_data():
    return pd.read_csv("datasaurus_all_-_datasaurus__1_.csv")

df = load_data()
shapes = sorted(df["shape"].unique())

# Sidebar controls
st.sidebar.header("Controls")
selected_shapes = st.sidebar.multiselect(
    "Select shape(s) to display",
    options=shapes,
    default=["dino"],
)

show_stats = st.sidebar.checkbox("Show summary statistics", value=True)
point_size = st.sidebar.slider("Point size", min_value=3, max_value=15, value=7)
color_points = st.sidebar.checkbox("Color by shape", value=True)

if not selected_shapes:
    st.warning("Please select at least one shape from the sidebar.")
    st.stop()

filtered = df[df["shape"].isin(selected_shapes)]

# Layout: plot + stats
col1, col2 = st.columns([3, 1])

with col1:
    fig = px.scatter(
        filtered,
        x="x",
        y="y",
        color="shape" if color_points else None,
        facet_col="shape" if len(selected_shapes) > 1 else None,
        facet_col_wrap=3,
        title=f"Scatterplot — {', '.join(selected_shapes)}",
        template="plotly_white",
        opacity=0.85,
    )
    fig.update_traces(marker=dict(size=point_size))
    fig.update_layout(height=500, legend_title_text="Shape")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    if show_stats:
        st.subheader("📊 Summary Stats")
        stats = (
            filtered.groupby("shape")[["x", "y"]]
            .agg(
                x_mean=("x", "mean"),
                x_std=("x", "std"),
                y_mean=("y", "mean"),
                y_std=("y", "std"),
                correlation=("x", lambda s: s.corr(filtered.loc[s.index, "y"])),
            )
            .round(2)
            .T
        )
        st.dataframe(stats, use_container_width=True)
        st.caption(
            "Notice how the statistics are nearly identical across all shapes — "
            "a powerful reminder to always visualize your data!"
        )

# All-shapes comparison at the bottom
if st.checkbox("Show all shapes at once"):
    st.subheader("All Shapes Side-by-Side")
    fig_all = px.scatter(
        df,
        x="x",
        y="y",
        facet_col="shape",
        facet_col_wrap=4,
        template="plotly_white",
        opacity=0.7,
        color="shape",
    )
    fig_all.update_traces(marker=dict(size=4))
    fig_all.update_layout(height=800, showlegend=False)
    st.plotly_chart(fig_all, use_container_width=True)
