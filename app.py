import pandas as pd
import plotly.express as px
import streamlit as st

# ── Load data ──────────────────────────────────────────────
df = pd.read_csv('dataset/iphone_sales_dataset.csv')

# Clean column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Create revenue column
df['revenue'] = df['price'] * df['quantity']

# Convert date column
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['year'] = df['sale_date'].dt.year

# ── Page config ────────────────────────────────────────────
st.set_page_config(page_title='iPhone Sales Dashboard', layout='wide')
st.title('📱 iPhone Sales Analytics Dashboard')

# ── Sidebar filters ────────────────────────────────────────
st.sidebar.header('Filters')

all_models = ['All'] + sorted(df['iphone_model'].unique().tolist())
all_countries = ['All'] + sorted(df['country'].unique().tolist())
all_years = ['All'] + sorted(df['year'].unique().tolist())

selected_model = st.sidebar.selectbox('iPhone Model', all_models)
selected_country = st.sidebar.selectbox('Country', all_countries)
selected_year = st.sidebar.selectbox('Year', all_years)

# ── Apply filters ──────────────────────────────────────────
filtered = df.copy()

if selected_model != 'All':
    filtered = filtered[filtered['iphone_model'] == selected_model]
if selected_country != 'All':
    filtered = filtered[filtered['country'] == selected_country]
if selected_year != 'All':
    filtered = filtered[filtered['year'] == selected_year]

# ── KPI cards ──────────────────────────────────────────────
st.subheader('Overview')
col1, col2, col3 = st.columns(3)

col1.metric('Total Units Sold', f"{filtered['quantity'].sum():,.0f}")
col2.metric('Total Revenue', f"${filtered['revenue'].sum():,.0f}")
col3.metric('Avg Price', f"${filtered['price'].mean():,.0f}")

st.divider()

# ── Charts ─────────────────────────────────────────────────
col4, col5 = st.columns(2)

with col4:
    st.subheader('Units sold by model')
    fig1 = px.bar(
        filtered.groupby('iphone_model')['quantity'].sum().reset_index(),
        x='iphone_model', y='quantity', color='iphone_model',
        labels={'quantity': 'Units Sold', 'iphone_model': 'Model'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    st.subheader('Revenue over time')
    fig2 = px.line(
        filtered.groupby('sale_date')['revenue'].sum().reset_index(),
        x='sale_date', y='revenue',
        labels={'revenue': 'Revenue ($)', 'sale_date': 'Date'}
    )
    st.plotly_chart(fig2, use_container_width=True)

col6, col7 = st.columns(2)

with col6:
    st.subheader('Sales by country')
    fig3 = px.pie(
        filtered.groupby('country')['quantity'].sum().reset_index(),
        names='country', values='quantity'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col7:
    st.subheader('Sales by payment method')
    fig4 = px.bar(
        filtered.groupby('payment_method')['quantity'].sum().reset_index(),
        x='payment_method', y='quantity', color='payment_method',
        labels={'quantity': 'Units Sold', 'payment_method': 'Payment Method'}
    )
    st.plotly_chart(fig4, use_container_width=True)

# ── Bonus: Sales by storage size ───────────────────────────
st.subheader('Sales by storage size')
fig5 = px.bar(
    filtered.groupby('storage')['quantity'].sum().reset_index(),
    x='storage', y='quantity', color='storage',
    labels={'quantity': 'Units Sold', 'storage': 'Storage'}
)
st.plotly_chart(fig5, use_container_width=True)

# ── Raw data toggle ────────────────────────────────────────
st.divider()
if st.checkbox('Show raw data'):
    st.dataframe(filtered)