# generate_charts.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'sales': [100, 120, 140, 110, 160],
    'profit': [20, 25, 30, 22, 35]
})

# Chart 1: Line chart
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['month'], y=df['sales'], name='Sales'))
fig1.add_trace(go.Scatter(x=df['month'], y=df['profit'], name='Profit'))
fig1.update_layout(title='Sales vs Profit', xaxis_title='Month', yaxis_title='Amount')
fig1.write_html("visual/chart1.html")

# Chart 2: Bar chart
fig2 = px.bar(df, x='month', y='sales', title='Monthly Sales')
fig2.write_html("visual/chart2.html")

print("Charts generated successfully!")
