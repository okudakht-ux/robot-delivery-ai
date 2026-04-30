import streamlit as st
import pandas as pd

st.set_page_config(page_title="Robot Delivery AI", layout="wide")

st.title("Multi-Agent Robot Delivery Optimization")
st.write("AI prototype for smart coordination of delivery robots in urban logistics.")

st.markdown("---")

# -----------------------
# Robots Data
# -----------------------
st.header("1. Available Robots")

robots = pd.DataFrame({
    "Robot": ["R1", "R2", "R3"],
    "Battery (%)": [25, 90, 60],
    "Distance to Order (miles)": [0.4, 1.2, 0.8],
    "Traffic Risk": ["Low", "Medium", "High"],
    "Status": ["Available", "Available", "Available"]
})

st.dataframe(robots, use_container_width=True)

# -----------------------
# Orders Data
# -----------------------
st.header("2. Current Order")

orders = pd.DataFrame({
    "Order": ["O1"],
    "Priority": ["Normal"],
    "Destination": ["Mission District"],
    "Type": ["Food Delivery"]
})

st.dataframe(orders, use_container_width=True)

# -----------------------
# Optimization Logic
# -----------------------
def traffic_score(level):
    mapping = {"Low": 1, "Medium": 2, "High": 3}
    return mapping[level]

def calculate_score(row):
    distance = row["Distance to Order (miles)"]
    battery_penalty = (100 - row["Battery (%)"]) / 100
    traffic = traffic_score(row["Traffic Risk"])

    score = (0.5 * distance) + (0.3 * battery_penalty) + (0.2 * traffic)
    return round(score, 3)

robots["Optimization Score"] = robots.apply(calculate_score, axis=1)

# -----------------------
# Optimize Button
# -----------------------
st.header("3. Optimize Assignment")

if st.button("Optimize Delivery"):
    best_robot = robots.sort_values("Optimization Score").iloc[0]

    st.success(f"Selected Robot: {best_robot['Robot']}")

    st.subheader("AI Decision Explanation")
    st.write(
        f"Robot {best_robot['Robot']} was selected after evaluating multiple constraints: "
        f"distance, battery level, and traffic risk. "
        f"The system does not simply choose the closest robot. It prioritizes the robot "
        f"with the best balance of efficiency and reliability."
    )

    st.subheader("Robot Comparison")
    st.dataframe(
        robots.sort_values("Optimization Score"),
        use_container_width=True
    )

    st.info(
        "AI insight: The selected robot has the lowest operational risk for the current order. "
        "This demonstrates task allocation based on multi-agent coordination rather than manual selection."
    )

st.markdown("---")

# -----------------------
# Conflict Scenario
# -----------------------
st.header("4. Dynamic Conflict Scenario")

st.write(
    "A new urgent hospital delivery appears while the system is already handling the normal order."
)

urgent_order = pd.DataFrame({
    "Order": ["O2"],
    "Priority": ["Urgent"],
    "Destination": ["Hospital"],
    "Type": ["Medical Delivery"]
})

st.dataframe(urgent_order, use_container_width=True)

if st.button("Run Conflict Resolution"):
    conflict_result = pd.DataFrame({
        "Order": ["O1", "O2"],
        "Priority": ["Normal", "Urgent"],
        "Assigned Robot": ["R1", "R2"],
        "Reason": [
            "R1 is close enough for the normal-priority delivery.",
            "R2 has high battery and is more reliable for the urgent hospital delivery."
        ]
    })

    st.success("System re-optimized assignments due to priority change.")

    st.subheader("Re-Optimized Assignment")
    st.dataframe(conflict_result, use_container_width=True)

    st.subheader("AI Conflict Explanation")
    st.write(
        "The system detected a conflict: a normal delivery and an urgent hospital delivery "
        "require robot assignment at the same time. Instead of keeping the original assignment, "
        "the system re-optimized the plan. R2 was assigned to the urgent hospital order because "
        "it has the highest battery level and lower operational risk. R1 was assigned to the normal "
        "delivery because the route is shorter and the order is less time-sensitive."
    )

    st.warning(
        "This shows dynamic decision-making: the system adapts when priorities change."
    )

st.markdown("---")

# -----------------------
# Technology Explanation
# -----------------------
st.header("5. Technology Concept")

st.write(
    "This prototype represents a simplified multi-agent AI system. "
    "Robot agents provide status data, the task allocation agent compares possible assignments, "
    "the energy agent evaluates battery risk, and the traffic agent evaluates route conditions. "
    "The orchestrator coordinates these agents and selects the best delivery plan."
)

st.write(
    "In a full IBM watsonx implementation, IBM Granite or watsonx.ai can generate richer explanations, "
    "while watsonx Orchestrate can coordinate multiple agents and tools."
)