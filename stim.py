import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io
 
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
 
st.set_page_config(
    page_title="Dynamic Data Visualization Dashboard",
    page_icon="📊",
    layout="wide"
)
 
st.title("📊 Dynamic Data Visualization Dashboard")
st.write(
    "Upload a CSV file, clean the data, apply filters, "
    "visualize it and view basic insights."
)
 
# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------
 
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)
 
if uploaded_file is not None:
 
    # Read CSV
    df = pd.read_csv(uploaded_file)
 
    st.success("CSV file uploaded successfully!")
 
    # --------------------------------------------------
    # DATA CLEANING
    # --------------------------------------------------
 
    st.sidebar.header("🧹 Data Cleaning")
 
    remove_duplicates = st.sidebar.checkbox(
        "Remove duplicate rows"
    )
 
    fill_missing = st.sidebar.checkbox(
        "Fill missing numeric values"
    )
 
    if remove_duplicates:
        df = df.drop_duplicates()
 
    if fill_missing:
        numeric_cols = df.select_dtypes(
            include="number"
        ).columns
 
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].mean())
 
    # --------------------------------------------------
    # DATA PREVIEW
    # --------------------------------------------------
 
    st.subheader("📋 Data Preview")
 
    st.dataframe(
        df.head(20),
        use_container_width=True
    )
 
    # Dataset information
    col1, col2, col3, col4 = st.columns(4)
 
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicate Rows", int(df.duplicated().sum()))
 
    # --------------------------------------------------
    # COLUMN TYPES
    # --------------------------------------------------
 
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()
 
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
 
    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------
 
    st.sidebar.header("🔎 Filter Options")
 
    filtered_df = df.copy()
 
    # Categorical filters
    for col in categorical_columns:
 
        unique_values = filtered_df[col].dropna().unique()
 
        if len(unique_values) <= 50:
 
            selected_values = st.sidebar.multiselect(
                f"Filter by {col}",
                options=sorted(
                    unique_values.astype(str)
                )
            )
 
            if selected_values:
                filtered_df = filtered_df[
                    filtered_df[col].astype(str).isin(
                        selected_values
                    )
                ]
 
    # --------------------------------------------------
    # VISUALIZATION
    # --------------------------------------------------
 
    st.subheader("📈 Data Visualization")
 
    if len(numeric_columns) == 0:
        st.warning(
            "The uploaded dataset must contain at least "
            "one numeric column."
        )
 
    else:
 
        # X-axis options
        all_x_columns = (
            categorical_columns + numeric_columns
        )
 
        x_axis = st.selectbox(
            "Select X-axis",
            all_x_columns
        )
 
        y_axis = st.selectbox(
            "Select Y-axis",
            numeric_columns
        )
 
        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Scatter Plot",
                "Pie Chart"
            ]
        )
 
        # --------------------------------------------------
        # BAR CHART
        # --------------------------------------------------
 
        if chart_type == "Bar Chart":
 
            fig = px.bar(
                filtered_df,
                x=x_axis,
                y=y_axis,
                title=f"{y_axis} by {x_axis}"
            )
 
            st.plotly_chart(
                fig,
                use_container_width=True
            )
 
        # --------------------------------------------------
        # LINE CHART
        # --------------------------------------------------
 
        elif chart_type == "Line Chart":
 
            fig = px.line(
                filtered_df,
                x=x_axis,
                y=y_axis,
                markers=True,
                title=f"{y_axis} Trend"
            )
 
            st.plotly_chart(
                fig,
                use_container_width=True
            )
 
        # --------------------------------------------------
        # SCATTER PLOT
        # --------------------------------------------------
 
        elif chart_type == "Scatter Plot":
 
            if len(numeric_columns) >= 2:
 
                scatter_x = st.selectbox(
                    "Select Scatter X-axis",
                    numeric_columns
                )
 
                scatter_y = st.selectbox(
                    "Select Scatter Y-axis",
                    numeric_columns,
                    index=1 if len(numeric_columns) > 1 else 0
                )
 
                fig = px.scatter(
                    filtered_df,
                    x=scatter_x,
                    y=scatter_y,
                    title=f"{scatter_y} vs {scatter_x}"
                )
 
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
 
            else:
                st.warning(
                    "At least two numeric columns "
                    "are required."
                )
 
        # --------------------------------------------------
        # PIE CHART
        # --------------------------------------------------
 
        elif chart_type == "Pie Chart":
 
            if x_axis in categorical_columns:
 
                pie_data = (
                    filtered_df
                    .groupby(x_axis)[y_axis]
                    .sum()
                    .reset_index()
                )
 
                fig = px.pie(
                    pie_data,
                    values=y_axis,
                    names=x_axis,
                    title=f"{y_axis} Distribution"
                )
 
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
 
            else:
                st.warning(
                    "Pie chart requires a categorical "
                    "column for the X-axis."
                )
 
    # --------------------------------------------------
    # CORRELATION HEATMAP
    # --------------------------------------------------
 
    st.subheader("🔥 Correlation Heatmap")
 
    show_heatmap = st.checkbox(
        "Show Correlation Heatmap"
    )
 
    if show_heatmap:
 
        if len(numeric_columns) >= 2:
 
            correlation = filtered_df[
                numeric_columns
            ].corr()
 
            fig, ax = plt.subplots(
                figsize=(10, 6)
            )
 
            sns.heatmap(
                correlation,
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                ax=ax
            )
 
            ax.set_title(
                "Correlation Between Numeric Variables"
            )
 
            st.pyplot(fig)
 
        else:
            st.warning(
                "At least two numeric columns "
                "are required for a heatmap."
            )
 
    # --------------------------------------------------
    # BASIC DATA INSIGHTS
    # --------------------------------------------------
 
    st.subheader("🤖 Basic Data Insights")
 
    with st.expander("Show Dataset Summary"):
 
        buffer = io.StringIO()
 
        filtered_df.describe(
            include="all"
        ).to_string(
            buf=buffer
        )
 
        st.text(buffer.getvalue())
 
    # --------------------------------------------------
    # DOWNLOAD FILTERED DATA
    # --------------------------------------------------
 
    st.subheader("⬇️ Download Filtered Data")
 
    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")
 
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )
 
else:
 
    st.info(
        "👆 Please upload a CSV file to start "
        "the dashboard."
    )
