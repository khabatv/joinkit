import pandas as pd
import streamlit as st

# Title and description
st.title("File Joiner: CSV, TSV, and TXT File Merger")
st.write("Upload two files, specify the join columns, and choose a join type to merge them.")

# File uploaders
file1 = st.file_uploader("Upload first file", type=["csv", "tsv", "txt"])
file2 = st.file_uploader("Upload second file", type=["csv", "tsv", "txt"])

# Function to load files
def load_file(file):
    if file is not None:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.tsv'):
            return pd.read_csv(file, sep='\t')
        elif file.name.endswith('.txt'):
            return pd.read_csv(file, delimiter='\t')
    return None

# Load both files
df1 = load_file(file1)
df2 = load_file(file2)

# Preview files
if df1 is not None:
    st.subheader("Preview of First File:")
    st.dataframe(df1.head())

if df2 is not None:
    st.subheader("Preview of Second File:")
    st.dataframe(df2.head())

# Proceed if both files are uploaded
if df1 is not None and df2 is not None:
    # Ask the user to input the column names to join on
    st.subheader("Join Options")
    join_col1 = st.selectbox("Select the column to join from the first file", df1.columns)
    join_col2 = st.selectbox("Select the column to join from the second file", df2.columns)
    
    # Join type options
    join_type = st.selectbox("Select join type", ['inner', 'outer', 'left', 'right'])

    # Button to perform the join
    if st.button("Join Files"):
        # Perform the join
        try:
            result_df = pd.merge(df1, df2, left_on=join_col1, right_on=join_col2, how=join_type)
            st.success("Files successfully joined!")
            st.subheader("Preview of Joined File:")
            st.dataframe(result_df.head())

            # Provide download link for the joined file
            st.download_button(
                label="Download Merged File as CSV",
                data=result_df.to_csv(index=False).encode('utf-8'),
                file_name='merged_file.csv',
                mime='text/csv'
            )

        except Exception as e:
            st.error(f"Error while joining files: {e}")
