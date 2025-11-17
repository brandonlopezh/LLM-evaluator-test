import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

st.set_page_config(page_title="LLM Quality Dashboard", layout="wide", page_icon="📊")

# Title and description
st.title("🎓 Educational LLM Quality Dashboard")
st.markdown("Interactive dashboard for monitoring LLM response quality and evaluator performance")

# Sidebar for file selection
st.sidebar.header("Select Results File")

# Get all results files
results_dir = Path("results")
results_files = sorted(results_dir.glob("results_*.csv"), key=lambda x: int(x.stem.split('_')[1]))

if not results_files:
    st.error("No results files found in the results/ folder. Please run evaluate.py first.")
    st.stop()

# File selector
selected_file = st.sidebar.selectbox(
    "Choose a results file:",
    results_files,
    format_func=lambda x: x.name
)

# Load data
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

df = load_data(selected_file)

# Check which columns exist
has_expected_quality = 'Expected_Quality' in df.columns
has_matches = 'Matches_Expected' in df.columns

# Display file info
st.sidebar.markdown("---")
st.sidebar.metric("Total Responses", len(df))
st.sidebar.metric("Average Quality Score", f"{df['Educational_Quality'].mean():.2f}")
if has_matches:
    st.sidebar.metric("Evaluator Accuracy", f"{(df['Matches_Expected'].sum() / len(df) * 100):.1f}%")

# Main dashboard content
if has_expected_quality:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Quality Analysis", "🎯 Evaluator Performance", "📋 Detailed Results"])
else:
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Quality Analysis", "📋 Detailed Results"])

with tab1:
    st.header("Quality Distribution Overview")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    excellent = (df['Overall_Rating'] == 'Excellent').sum()
    good = (df['Overall_Rating'] == 'Good').sum()
    review = (df['Overall_Rating'] == 'Needs Review').sum()
    poor = (df['Overall_Rating'] == 'Poor').sum()
    
    col1.metric("Excellent", excellent, delta=f"{excellent/len(df)*100:.1f}%")
    col2.metric("Good", good, delta=f"{good/len(df)*100:.1f}%")
    col3.metric("Needs Review", review, delta=f"{review/len(df)*100:.1f}%")
    col4.metric("Poor", poor, delta=f"{poor/len(df)*100:.1f}%")
    
    # Rating distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        rating_counts = df['Overall_Rating'].value_counts()
        fig_pie = px.pie(
            values=rating_counts.values,
            names=rating_counts.index,
            title="Response Quality Distribution",
            color=rating_counts.index,
            color_discrete_map={
                'Excellent': '#28a745',
                'Good': '#17a2b8',
                'Needs Review': '#ffc107',
                'Poor': '#dc3545'
            }
        )
        st.plotly_chart(fig_pie, width='stretch')
    
    with col2:
        fig_bar = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            title="Response Counts by Rating",
            labels={'x': 'Rating', 'y': 'Count'},
            color=rating_counts.index,
            color_discrete_map={
                'Excellent': '#28a745',
                'Good': '#17a2b8',
                'Needs Review': '#ffc107',
                'Poor': '#dc3545'
            }
        )
        st.plotly_chart(fig_bar, width='stretch')

with tab2:
    st.header("Educational Quality Analysis")
    
    # Quality score distribution
    fig_hist = px.histogram(
        df,
        x='Educational_Quality',
        nbins=20,
        title="Educational Quality Score Distribution",
        labels={'Educational_Quality': 'Quality Score'},
        color_discrete_sequence=['#6f42c1']
    )
    st.plotly_chart(fig_hist, width='stretch')
    
    # Quality by grade level
    grade_quality = df.groupby('Grade_Level')['Educational_Quality'].agg(['mean', 'min', 'max', 'count']).reset_index()
    grade_quality = grade_quality.sort_values('mean', ascending=False)
    
    fig_grade = go.Figure()
    fig_grade.add_trace(go.Bar(
        x=grade_quality['Grade_Level'],
        y=grade_quality['mean'],
        name='Average Quality',
        marker_color='lightblue',
        error_y=dict(
            type='data',
            symmetric=False,
            array=grade_quality['max'] - grade_quality['mean'],
            arrayminus=grade_quality['mean'] - grade_quality['min']
        )
    ))
    fig_grade.update_layout(
        title="Average Quality Score by Grade Level (with min/max range)",
        xaxis_title="Grade Level",
        yaxis_title="Quality Score"
    )
    st.plotly_chart(fig_grade, width='stretch')
    
    # Low quality responses
    st.subheader("⚠️ Low Quality Responses (Score < 0.7)")
    low_quality = df[df['Educational_Quality'] < 0.7][['Prompt', 'Overall_Rating', 'Educational_Quality', 'Grade_Level']]
    if len(low_quality) > 0:
        st.dataframe(low_quality, width='stretch')
    else:
        st.success("No low quality responses found! 🎉")

if has_expected_quality:
    with tab3:
        st.header("Evaluator Performance")
        
        # Evaluator accuracy metrics
        col1, col2 = st.columns(2)
        
        with col1:
            if has_matches:
                matches = df['Matches_Expected'].value_counts()
                fig_accuracy = px.pie(
                    values=matches.values,
                    names=['Match' if x else 'Mismatch' for x in matches.index],
                    title="Evaluator Accuracy",
                    color=['Match' if x else 'Mismatch' for x in matches.index],
                    color_discrete_map={'Match': '#28a745', 'Mismatch': '#dc3545'}
                )
                st.plotly_chart(fig_accuracy, width='stretch')
        
        with col2:
            # Rating comparison bar chart
            comparison_data = df.groupby(['Expected_Quality', 'Overall_Rating']).size().reset_index(name='count')
            fig_comparison = px.bar(
                comparison_data,
                x='Expected_Quality',
                y='count',
                color='Overall_Rating',
                title="Expected vs Actual Ratings Distribution",
                labels={'Expected_Quality': 'Expected Rating', 'count': 'Count'},
                color_discrete_map={
                    'Excellent': '#28a745',
                    'Good': '#17a2b8',
                    'Needs Review': '#ffc107',
                    'Poor': '#dc3545'
                },
                barmode='group'
            )
            st.plotly_chart(fig_comparison, width='stretch')
        
        # Rating match statistics
        st.subheader("📊 Rating Match Analysis")
        col1, col2, col3 = st.columns(3)
        
        if has_matches:
            matches_count = df['Matches_Expected'].sum()
            col1.metric("Exact Matches", f"{matches_count} / {len(df)}")
            col2.metric("Match Rate", f"{(matches_count / len(df) * 100):.1f}%")
            col3.metric("Mismatches", f"{len(df) - matches_count}")
        
        # Mismatches table
        if has_matches:
            st.subheader("🔍 Evaluator Mismatches")
            mismatches = df[df['Matches_Expected'] == False][['Prompt', 'Expected_Quality', 'Educational_Quality', 'Overall_Rating', 'Notes']]
            if len(mismatches) > 0:
                st.dataframe(mismatches, width='stretch')
            else:
                st.success("Perfect evaluator accuracy! 🎯")

# Detailed Results tab (always present)
detailed_tab = tab4 if has_expected_quality else tab3
with detailed_tab:
    st.header("Detailed Results")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rating_filter = st.multiselect(
            "Filter by Rating:",
            options=df['Overall_Rating'].unique(),
            default=df['Overall_Rating'].unique()
        )
    
    with col2:
        grade_filter = st.multiselect(
            "Filter by Grade Level:",
            options=sorted(df['Grade_Level'].unique()),
            default=sorted(df['Grade_Level'].unique())
        )
    
    with col3:
        quality_threshold = st.slider(
            "Min Quality Score:",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1
        )
    
    # Apply filters
    filtered_df = df[
        (df['Overall_Rating'].isin(rating_filter)) &
        (df['Grade_Level'].isin(grade_filter)) &
        (df['Educational_Quality'] >= quality_threshold)
    ]
    
    st.metric("Filtered Results", len(filtered_df))
    
    # Select columns to display
    display_cols = ['Test_ID', 'Prompt', 'Overall_Rating', 'Educational_Quality', 'Grade_Level']
    if has_matches:
        display_cols.append('Matches_Expected')
    if has_expected_quality:
        display_cols.insert(4, 'Expected_Quality')
    
    # Display filtered data
    st.dataframe(
        filtered_df[display_cols],
        width='stretch',
        height=400
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Results as CSV",
        data=csv,
        file_name=f"filtered_{selected_file.name}",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("Built with ❤️ for Educational LLM Quality Analysis")