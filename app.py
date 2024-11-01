import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide",page_title="Analysis")
st.header("STUDENT ANALYSIS")
st.subheader("By KAVUCIKA P")

#cache to read data only once
@st.cache_data
def load_data():
    url="D:\\Downloads\\assignmentocc.csv"
    data=pd.read_csv(url)
    return data
data=load_data()
st.dataframe(data)

#top 10 ranks
top_10_ranks=data.nsmallest(10,'Rank')
top_10_ranks['Inverse Rank']=top_10_ranks['Rank'].max()-top_10_ranks['Rank']+1
fig_top_10=px.bar(top_10_ranks, x='Name of the Students', y='Inverse Rank', title='Top 10 rank holders', color='Rank', height=400, labels={'Inverse Rank':'Performance(Higher=Better)'},color_continuous_scale=px.colors.sequential.Blues[::-1])
st.plotly_chart(fig_top_10)

#least 10 ranks
least_10_ranks=data.nlargest(10,'Rank')
least_10_ranks['Inverse Rank']=least_10_ranks['Rank'].max()-least_10_ranks['Rank']+1
fig_least_100=px.bar(least_10_ranks, x='Name of the Students', y='Inverse Rank', title="Least 10 rank holders",color="Rank",height=400, labels={'Inverse Rank':'Performance(Higher=Better)'},color_continuous_scale=px.colors.sequential.Blues[::-1])
st.plotly_chart(fig_least_100)

#subject mark visualization
st.write("subject mark visualization")
subject_choice=st.selectbox(label="Select subject",options=['S1','S2','S3','S4','S5'])
fig_submark=px.bar(data,x='Name of the Students',y=subject_choice,title=" subject mark visualization",color=subject_choice,height=400)
st.plotly_chart(fig_submark)

total_pass=data['Pass'].sum()
total_fail=data['Fail'].sum()
df=pd.DataFrame({'Status':['Pass','Fail'],'Count':[total_pass,total_fail]})

pie_df = pd.DataFrame({
    'Status': ['Pass', 'Fail'],
    'Count': [total_pass, total_fail]
})

fig_pie = px.pie(pie_df, values='Count', names='Status', title='Overall Pass/Fail Distribution', color_discrete_sequence=['green', 'red'])
st.plotly_chart(fig_pie)

# If your dataset contains multiple tests like 'Test1_S1', 'Test2_S1', etc.
test_columns = ['S1', 'S2', 'S3','S4','S5']

# Select a specific student to analyze their performance progress
student_name = st.selectbox("Select Student", data['Name of the Students'].unique())

# Filter data for the selected student
student_data = data[data['Name of the Students'] == student_name][test_columns].T
student_data.columns = ['Marks']

# Create a line chart to show performance over time
fig_progress = px.line(student_data, y='Marks', 
                       title=f'Performance Progress of {student_name}', 
                       labels={'index':'Test', 'Marks':'Marks'})

st.plotly_chart(fig_progress)

# Define the passing mark
passing_mark = 35

# Calculate the overall pass and fail counts (based on 'Pass' and 'Fail' columns in the data)
total_pass_count = int(data['Pass'].sum())
total_fail_count = int(data['Fail'].sum())

# Display total number of passes and fails overall
st.write(f"Overall Total Pass: {total_pass_count}")
st.write(f"Overall Total Fail: {total_fail_count}")

# Initialize a dictionary to store pass/fail counts for each subject
subject_pass_fail = {}

# Loop through each subject to calculate pass/fail counts
for subject in ['S1', 'S2', 'S3', 'S4', 'S5']:
    subject_pass_count = int((data[subject] > passing_mark).sum())
    subject_fail_count = int((data[subject] <= passing_mark).sum())
    subject_pass_fail[subject] = {'Pass': subject_pass_count, 'Fail': subject_fail_count}
    
    # Display pass/fail counts for the subject
    st.write(f"{subject} - Pass: {subject_pass_count}, Fail: {subject_fail_count}")

    # Correlation matrix of subject marks
subject_correlation = data[['S1', 'S2', 'S3', 'S4', 'S5']].corr()

# Heatmap of subject correlations
fig_correlation = px.imshow(subject_correlation, title='Correlation Between Subjects', color_continuous_scale='Blues')
st.plotly_chart(fig_correlation)

# Calculate average marks for each subject
avg_marks = data[['S1', 'S2', 'S3', 'S4', 'S5']].mean()

# Create a bar chart to visualize the average marks per subject
fig_avg_marks = px.bar(x=avg_marks.index, y=avg_marks.values, title='Average Marks per Subject', 
                       labels={'x': 'Subject', 'y': 'Average Marks'}, height=400)

st.plotly_chart(fig_avg_marks)

# Create a box plot to show the distribution of marks for each subject
fig_box = px.box(data[['S1', 'S2', 'S3', 'S4', 'S5']], 
                 title='Subject-wise Distribution of Marks', 
                 labels={'variable':'Subject', 'value':'Marks'}, 
                 height=400)

st.plotly_chart(fig_box)


subject_columns = ['S1', 'S2', 'S3', 'S4', 'S5']

# 1. Consistency Analysis: Calculate standard deviation for each student
data['Consistency (Std Dev)'] = data[subject_columns].std(axis=1)

# Sort by consistency (lower standard deviation = more consistent)
data_sorted_by_consistency = data[['Name of the Students', 'Consistency (Std Dev)']].sort_values(by='Consistency (Std Dev)')

# Plot consistency
fig_consistency = px.bar(data_sorted_by_consistency, x='Name of the Students', y='Consistency (Std Dev)',
                         title='Student Performance Consistency (Lower = More Consistent)',
                         color='Consistency (Std Dev)', height=400, color_continuous_scale=px.colors.sequential.Teal)
st.plotly_chart(fig_consistency)

# 2. Correlation Analysis: Correlation between subjects
correlation_matrix = data[subject_columns].corr()

# Plot correlation matrix as heatmap
fig_correlation = px.imshow(correlation_matrix, text_auto=True, 
                            title='Correlation Between Subjects',
                            labels=dict(x="Subjects", y="Subjects", color="Correlation"))
st.plotly_chart(fig_correlation)

# 3. Subject Strength/Weakness Analysis: Identify strongest and weakest subjects
data['Strongest Subject'] = data[subject_columns].idxmax(axis=1)
data['Weakest Subject'] = data[subject_columns].idxmin(axis=1)

# Count how many students have each subject as strongest/weakest
strongest_subject_count = data['Strongest Subject'].value_counts().reset_index()
strongest_subject_count.columns = ['Subject', 'Count']

weakest_subject_count = data['Weakest Subject'].value_counts().reset_index()
weakest_subject_count.columns = ['Subject', 'Count']

# Plot strongest subjects
fig_strongest = px.bar(strongest_subject_count, x='Subject', y='Count', 
                       title='Most Common Strongest Subjects',
                       labels={'Subject': 'Subject', 'Count': 'Number of Students'}, color='Count')
st.plotly_chart(fig_strongest)

# Plot weakest subjects
fig_weakest = px.bar(weakest_subject_count, x='Subject', y='Count', 
                     title='Most Common Weakest Subjects',
                     labels={'Subject': 'Subject', 'Count': 'Number of Students'}, color='Count')
st.plotly_chart(fig_weakest)