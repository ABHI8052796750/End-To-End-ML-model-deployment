import streamlit as st
import pandas as pd

# ===== PAGE CONFIG =====
st.set_page_config(page_title="AI Fitness Coach Pro", layout="wide")

# ===== STYLE =====
st.markdown("""
<style>
body { background-color: #0e1117; }
.stButton>button {
    background: linear-gradient(90deg, #ff4b4b, #ff884b);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🔥 AI Fitness Coach PRO")

# ===== SESSION =====
if "user" not in st.session_state:
    st.session_state.user = None

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

# ===== HABIT DATA =====
if "habit_data" not in st.session_state:
    habits = [
        "Water", "Gym", "Diet", "Study", "Project",
        "NoFap", "Social_skill", "Dating", "Business"
    ]
    st.session_state.habit_data = pd.DataFrame(
        0,
        index=habits,
        columns=[f"Day {i}" for i in range(1, 32)]
    )

# ================= LOGIN =================
if st.session_state.user is None:

    st.subheader("🔐 Login / Signup")

    choice = st.selectbox("Select Option", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if email and password:
            st.session_state.user = email
            st.success("Logged in 🚀")
        else:
            st.error("Fill all fields")

# ================= MAIN APP =================
else:

    if st.button("Logout"):
        st.session_state.user = None
        st.stop()

    st.subheader("👤 User Details")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (kg)", 30, 150)

    with col2:
        height = st.number_input("Height (cm)", 100, 250)
        goal = st.selectbox("Goal", ["Fat Loss", "Muscle Gain", "Lean Bulk", "Shredded"])

    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])

    # ===== PLAN BUTTON =====
    if st.button("Generate Plan 🚀"):
        st.session_state.plan_generated = True

        if gender == "Male":
            st.session_state.calories = 10 * weight + 6.25 * height - 5 * 25 + 5
        else:
            st.session_state.calories = 10 * weight + 6.25 * height - 5 * 25 - 161

    # ===== PLAN SECTION =====
    if st.session_state.plan_generated:

        calories = st.session_state.calories

        if goal == "Fat Loss":
            calories -= 400
            protein = weight * 2
        elif goal == "Muscle Gain":
            calories += 300
            protein = weight * 2.2
        elif goal == "Lean Bulk":
            calories += 200
            protein = weight * 2.2
        else:
            calories -= 500
            protein = weight * 2.3

        st.metric("🔥 Calories", int(calories))
        st.metric("💪 Protein", int(protein))

        # ===== DIET =====
        st.markdown("## 🍽 Diet Plan")

        if diet_type == "Vegetarian":
            st.info(f"""
🥣 Breakfast: Oats + Milk + Peanut Butter  
🍛 Lunch: Dal + Rice + Paneer  
🌙 Dinner: Roti + Paneer + Sabji  
🍌 Snacks: Fruits / Soy / Curd  

👉 Protein Target: {int(protein)}g
""")
        else:
            st.info(f"""
🥚 Breakfast: Eggs + Toast  
🍗 Lunch: Chicken + Rice  
🍽 Dinner: Roti + Chicken / Fish  
🥛 Snacks: Curd / Whey Protein  

👉 Protein Target: {int(protein)}g
""")

        # ===== 🏋️ AI WORKOUT TRAINER =====
        st.markdown("## 🏋️ AI Workout Trainer")

        def get_weekly_workout(goal):
            if goal == "Fat Loss":
                return {
                    "Monday": "Full Body + Cardio",
                    "Tuesday": "HIIT + Abs",
                    "Wednesday": "Upper Body + Cardio",
                    "Thursday": "HIIT + Core",
                    "Friday": "Lower Body + Cardio",
                    "Saturday": "Light Cardio + Abs",
                    "Sunday": "Rest"
                }
            elif goal == "Muscle Gain":
                return {
                    "Monday": "Push",
                    "Tuesday": "Pull",
                    "Wednesday": "Legs",
                    "Thursday": "Push",
                    "Friday": "Pull",
                    "Saturday": "Legs",
                    "Sunday": "Rest"
                }
            elif goal == "Lean Bulk":
                return {
                    "Monday": "Upper Body",
                    "Tuesday": "Lower Body",
                    "Wednesday": "Rest",
                    "Thursday": "Upper Body",
                    "Friday": "Lower Body",
                    "Saturday": "Arms + Abs",
                    "Sunday": "Rest"
                }
            elif goal == "Shredded":
                return {
                    "Monday": "Push + Cardio",
                    "Tuesday": "Pull + Cardio",
                    "Wednesday": "Legs + HIIT",
                    "Thursday": "Upper + Cardio",
                    "Friday": "Lower + HIIT",
                    "Saturday": "Full Body + Cardio",
                    "Sunday": "Rest"
                }
            return {}

        plan = get_weekly_workout(goal)

        for day, workout in plan.items():
            st.write(f"**{day}:** {workout}")

        # ===== VIDEO =====
        st.markdown("## 🎥 Video Guide")
        st.video("https://www.youtube.com/watch?v=NYviEOTnFaA")

        # ===== PAYMENT =====
        st.markdown("## 💳 Premium")
        if st.button("Unlock Premium 🚀"):
            st.markdown("[Pay Now](https://rzp.io/l/YOUR_LINK)")

    # ===== HABIT TRACKER =====
    st.markdown("## 📊 Habit Tracker")

    habit = st.selectbox("Habit", st.session_state.habit_data.index)
    day = st.selectbox("Day", st.session_state.habit_data.columns)
    value = st.selectbox("Done?", [0, 1])

    if st.button("Save Habit"):
        st.session_state.habit_data.loc[habit, day] = value
        st.success("Saved ✔")

    st.dataframe(st.session_state.habit_data, use_container_width=True)