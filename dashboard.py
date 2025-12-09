import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# LOAD CSV FILES

def load_csv(path):
    """Load any CSV file and return DataFrame."""
    return pd.read_csv(path)


def run():
    st.title("📊 Welcome to your Dashboard")
    st.markdown("<h1 style='text-align: center; color: black;'>MY BEST DATA APP</h1>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("📁 Select your dataset")

    # List CSV files inside /data folder
  
    data_folder = "data"
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

    if not csv_files:
        st.error("❌ No CSV files found in /data folder!")
        return

    # Dropdown to select CSV
    dataset_choice = st.selectbox(
        "Choose a cleaned CSV dataset",
        csv_files
    )

  
    # Load selected CSV file
  
    if dataset_choice:
        path = os.path.join(data_folder, dataset_choice)
        df = load_csv(path)

        st.success(f"Loaded dataset: {dataset_choice}")
        st.write("### Preview of data")
        st.dataframe(df.head())


        # KPI Section
      
        st.write("---")
        st.subheader(" Key Performance Indicators (KPIs)")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Rows", len(df))

        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:
            num_col = numeric_cols[0]

            with col2:
                st.metric("Average Value", round(df[num_col].mean(), 2))

            with col3:
                st.metric("Max Value", round(df[num_col].max(), 2))
        else:
            st.info("No numeric columns found for KPIs.")

       
        # Data Visualization
      
        st.write("---")
        st.subheader("📉 Data Visualization")

        if len(numeric_cols) > 0:
            column = st.selectbox("Select numeric column to analyze", numeric_cols)

            # Histogram
            st.write("###  Histogram")
            fig, ax = plt.subplots()
            ax.hist(df[column], bins=20)
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Histogram of {column}")
            st.pyplot(fig)

            # Bar Chart Value Counts
            st.write("### Bar Chart (Value Counts)")
            fig2, ax2 = plt.subplots()
            df[column].value_counts().plot(kind="bar", ax=ax2)
            ax2.set_title(f"Bar Chart of {column}")
            st.pyplot(fig2)

            # Scatter plot
            st.write("###  Scatter Plot")

            if len(numeric_cols) > 1:
                col_x = st.selectbox("X-axis", numeric_cols, index=0)
                col_y = st.selectbox("Y-axis", numeric_cols, index=1)

                fig3, ax3 = plt.subplots()
                ax3.scatter(df[col_x], df[col_y])
                ax3.set_xlabel(col_x)
                ax3.set_ylabel(col_y)
                ax3.set_title(f"Scatter Plot: {col_x} vs {col_y}")
                st.pyplot(fig3)

        else:
            st.warning("No numeric columns available for plotting.")

      
        # Pie Chart (Categorical)

        st.write("---")
        st.subheader("🥧 Pie Chart (Categorical Column)")

        categ_cols = df.select_dtypes(include="object").columns

        if len(categ_cols) > 0:
            col_cat = st.selectbox("Select a categorical column", categ_cols)

            fig4, ax4 = plt.subplots()
            df[col_cat].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax4)
            ax4.set_ylabel("")
            ax4.set_title(f"Distribution of {col_cat}")
            st.pyplot(fig4)
        else:
            st.info("No categorical columns available for a pie chart.")
