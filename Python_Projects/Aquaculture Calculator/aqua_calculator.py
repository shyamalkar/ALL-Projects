import streamlit as st
import pandas as pd


# page confirm

st.set_page_config(
    page_title="Aqua Culture Calculator",
    page_icon="🐟",
    layout="wide"
)


# titile 
st.title("🐟 Aqua Culture Calculator")

st.caption(
    "Fish farming load capacity, feed estimation and ROI calculator"
)



# Side bar

st.sidebar.header("Farming Assumptions")



# load capacity 

st.sidebar.subheader("🐠 Load Capacity")

area_per_unit = st.sidebar.number_input(
    "Standard Pond Area",
    min_value=1.0,
    value=1000.0,
    step=100.0
)

fish_per_unit = st.sidebar.number_input(
    "Baby Pin per Standard Area",
    min_value=1,
    value=85000,
    step=1000
)


# feed asumption 

st.sidebar.subheader("🌾 Feed")

feed_ratio = st.sidebar.number_input(
    "Feed Ratio (kg feed / kg biomass)",
    min_value=0.01,
    value=1.30,
    step=0.05
)


# tabs 

tab1, tab2 = st.tabs(
    [
        "🐟 Load Capacity",
        "💰 ROI Calculator"
    ]
)


# Load capacity 

with tab1:

    st.header("🐟 Pond Load Capacity Calculator")

    st.write(
        "Calculate recommended baby-pin quantity, "
        "underwater biomass and estimated feed requirement."
    )


# pond area 

    pond_area = st.number_input(
        "📐 Enter Pond Area",
        min_value=0.0,
        value=1000.0,
        step=100.0
    )


# baby pin 

    baby_pin = st.number_input(
        "🐠 Actual Baby Pin Quantity",
        min_value=0,
        value=85000,
        step=1000
    )


# average fish weight 

    average_weight = st.number_input(
        "⚖️ Average Fish Weight (kg)",
        min_value=0.001,
        value=1.0,
        step=0.1,
        format="%.3f"
    )


    st.divider()

# recommend baby pin 

    recommended_pin = (
        pond_area / area_per_unit
    ) * fish_per_unit


# biomass

    underwater_biomass = (
        baby_pin * average_weight
    )


# feed requirement 

    estimated_feed = (
        underwater_biomass * feed_ratio
    )


# results  

    st.subheader("📊 Calculation Results")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🐠 Recommended Baby Pin",
            f"{recommended_pin:,.0f}"
        )


    with col2:

        st.metric(
            "⚖️ Underwater Biomass",
            f"{underwater_biomass:,.2f} kg"
        )


    with col3:

        st.metric(
            "🌾 Estimated Feed",
            f"{estimated_feed:,.2f} kg"
        )


    st.divider()


# Compare actual vs predict. 

    st.subheader(
        "📌 Baby Pin Capacity Check"
    )


    difference = (
        baby_pin - recommended_pin
    )


    if difference > 0:

        st.warning(
            f"⚠️ Actual baby pin is "
            f"**{abs(difference):,.0f}** above "
            f"the calculated capacity."
        )

    elif difference < 0:

        st.info(
            f"ℹ️ Actual baby pin is "
            f"**{abs(difference):,.0f}** below "
            f"the calculated capacity."
        )

    else:

        st.success(
            "✅ Actual baby pin matches "
            "the calculated capacity."
        )

# ROI calculator 

with tab2:

    st.header("💰 Aqua Culture ROI Calculator")

    st.write(
        "Calculate revenue, total expenses, profit/loss "
        "and return on investment."
    )


# Revenu  e

    st.subheader("🐟 Revenue")


    col1, col2 = st.columns(2)


    with col1:

        production = st.number_input(
            "🐠 Total Production (kg)",
            min_value=0.0,
            value=1000.0,
            step=100.0
        )


    with col2:

        selling_price = st.number_input(
            "💵 Selling Price per kg (₹)",
            min_value=0.0,
            value=180.0,
            step=5.0
        )


    total_revenue = (
        production * selling_price
    )


    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.2f}"
    )


    st.divider()


# Expenses 

    st.subheader("💸 Expenses")


# Disel 

    st.markdown("### Diesel")


    col1, col2 = st.columns(2)


    with col1:

        diesel_litre = st.number_input(
            "Diesel Quantity (litres)",
            min_value=0.0,
            value=0.0,
            step=10.0
        )


    with col2:

        diesel_price = st.number_input(
            "Diesel Price per Litre (₹)",
            min_value=0.0,
            value=93.34,
            step=0.01
        )


    diesel_cost = (
        diesel_litre * diesel_price
    )


# labour 
    labour = st.number_input(
        "Labour Cost (₹)",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


# Electrictiy / lich

    electricity = st.number_input(
        "Electricity / Other Utility Cost (₹)",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


# medicine 

    medicine = st.number_input(
        "Medicine Cost (₹)",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


# Feed 

    feed_cost = st.number_input(
        "Feed Cost (₹)",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


# baby pin 

    pin_cost = st.number_input(
        "Baby Pin Cost (₹)",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


    # --------------------------------------------------------
    # OTHER
    # --------------------------------------------------------

    other_cost = st.number_input(
        "📦 Other Expenses (₹)",
        min_value=0.0,
        value=0.0,
        step=1000.0
    )


    # ========================================================
    # EXPENSE CALCULATION
    # ========================================================

    total_expenses = (
        diesel_cost
        + labour
        + electricity
        + medicine
        + feed_cost
        + pin_cost
        + other_cost
    )


    # ========================================================
    # PROFIT / LOSS
    # ========================================================

    net_profit = (
        total_revenue
        - total_expenses
    )


    # ========================================================
    # ROI
    # ========================================================

    if total_expenses > 0:

        roi = (
            net_profit
            / total_expenses
        ) * 100

    else:

        roi = 0


    # ========================================================
    # COST PER KG
    # ========================================================

    if production > 0:

        cost_per_kg = (
            total_expenses
            / production
        )

    else:

        cost_per_kg = 0


    # ========================================================
    # BREAK-EVEN PRICE
    # ========================================================

    break_even_price = cost_per_kg


    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.subheader("📊 Financial Results")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "💰 Revenue",
            f"₹{total_revenue:,.2f}"
        )


    with col2:

        st.metric(
            "💸 Total Expenses",
            f"₹{total_expenses:,.2f}"
        )


    with col3:

        st.metric(
            "📦 Cost / kg",
            f"₹{cost_per_kg:,.2f}"
        )


    with col4:

        st.metric(
            "📈 ROI",
            f"{roi:.2f}%"
        )


    # ========================================================
    # PROFIT / LOSS
    # ========================================================

    st.divider()


    if net_profit > 0:

        st.success(
            f"🟢 **NET PROFIT: "
            f"₹{net_profit:,.2f}**"
        )


    elif net_profit < 0:

        st.error(
            f"🔴 **NET LOSS: "
            f"₹{abs(net_profit):,.2f}**"
        )


    else:

        st.warning(
            "⚪ **BREAK-EVEN: No profit, no loss.**"
        )


    # ========================================================
    # BREAK-EVEN
    # ========================================================

    st.info(
        f"🎯 Break-even selling price: "
        f"**₹{break_even_price:,.2f} / kg**"
    )


    # ========================================================
    # EXPENSE BREAKDOWN
    # ========================================================

    st.divider()

    st.subheader("📊 Expense Breakdown")


    expense_data = {

        "Expense": [
            "Diesel",
            "Labour",
            "Electricity / Utility",
            "Medicine",
            "Feed",
            "Baby Pin",
            "Other"
        ],

        "Amount": [
            diesel_cost,
            labour,
            electricity,
            medicine,
            feed_cost,
            pin_cost,
            other_cost
        ]
    }


    expense_df = pd.DataFrame(
        expense_data
    )


    # Remove zero expenses from chart

    chart_df = expense_df[
        expense_df["Amount"] > 0
    ]


    if not chart_df.empty:

        st.bar_chart(
            chart_df.set_index("Expense")
        )

    else:

        st.info(
            "Enter expense values to see the chart."
        )


    # ========================================================
    # EXPENSE TABLE
    # ========================================================

    st.dataframe(
        expense_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # FORMULAS
    # ========================================================

    with st.expander("🧮 Show ROI Formulas"):

        st.write("### Total Revenue")

        st.code(
            "Revenue = Production × Selling Price"
        )


        st.write("### Diesel Cost")

        st.code(
            "Diesel Cost = Litres × Price per Litre"
        )


        st.write("### Total Expenses")

        st.code(
            "Total Expenses = "
            "Diesel + Labour + Utility + Medicine "
            "+ Feed + Pin + Other"
        )


        st.write("### Net Profit / Loss")

        st.code(
            "Net Profit = Revenue - Total Expenses"
        )


        st.write("### ROI")

        st.code(
            "ROI = (Net Profit / Total Expenses) × 100"
        )


        st.write("### Cost per kg")

        st.code(
            "Cost per kg = Total Expenses / Production"
        )


        st.write("### Break-even Price")

        st.code(
            "Break-even Price = Cost per kg"
        )