import streamlit as st
import json
import os
import datetime
import random

WALLET_FILE = "wallet.json"

# ---------- UTILITY FUNCTIONS ----------
def load_wallet():
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "r") as file:
            return json.load(file)
    else:
        return {"actions": [], "total_credits": 0.0, "total_co2": 0.0}

def save_wallet(wallet):
    with open(WALLET_FILE, "w") as file:
        json.dump(wallet, file, indent=4)

def calculate_co2_and_credits(activity, participants, tree_count):
    if "tree" in activity.lower():
        co2 = tree_count * 22
        tip = "Plant native trees and maintain them for long-term impact."
    elif "compost" in activity.lower():
        co2 = 2.5 * participants
        tip = "Great! Encourage composting in your community."
    elif "solar" in activity.lower():
        co2 = 250 * participants
        tip = "Solar panels save energy. Consider solar water heating too."
    else:
        co2 = random.randint(50, 150)
        tip = "Try to combine this with waste reduction or tree planting."
    
    credits = round(co2, 2)
    return co2, credits, tip

# ---------- UI BEGINS ----------
st.set_page_config(page_title="ClimaDelv.AI", page_icon="🌿")
st.title("🌍 ClimaDelv.AI – Climate Action Dashboard")

# Load or initialize wallet
wallet = load_wallet()

# Show current totals
st.subheader("📊 Your Climate Impact Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Actions", len(wallet["actions"]))
col2.metric("Total CO₂ Saved", f'{wallet["total_co2"]} kg')
col3.metric("Total Credits", f'{wallet["total_credits"]} 💳')

st.markdown("---")

# ---------- Action Logger ----------
st.subheader("📝 Log New Eco-Action")

activity = st.text_area("Describe your eco-action", placeholder="e.g., Planted 30 trees in school ground.")
participants = st.number_input("Number of people involved", min_value=1, step=1)
tree_count = st.number_input("Number of trees planted", min_value=0, step=1)
location = st.text_input("Location (city, area)")

image = st.camera_input("📸 Take a photo (or upload below)")
if not image:
    image = st.file_uploader("Or upload a photo of the activity", type=["jpg", "jpeg", "png"])

if st.button("💡 Analyze & Save"):
    if not activity.strip():
        st.warning("Please enter a description.")
    else:
        co2, credits, tip = calculate_co2_and_credits(activity, participants, tree_count)
        today = str(datetime.date.today())

        new_action = {
            "date": today,
            "activity": activity,
            "participants": participants,
            "trees": tree_count,
            "location": location,
            "co2_saved": co2,
            "credits": credits,
            "tip": tip
        }

        wallet["actions"].append(new_action)
        wallet["total_co2"] += co2
        wallet["total_credits"] += credits
        save_wallet(wallet)

        st.success(f"✅ Saved! You earned {credits} carbon credits!")
        st.info(f"💡 Tip: {tip}")

st.markdown("---")

# ---------- Wallet History ----------
st.subheader("📜 Action History")
for action in reversed(wallet["actions"][-5:]):
    st.markdown(f"""
    **🗓 Date**: {action['date']}  
    **📝 Activity**: {action['activity']}  
    **📍 Location**: {action['location']}  
    **👥 People Involved**: {action['participants']}  
    **🌳 Trees**: {action['trees']}  
    **📉 CO₂ Saved**: `{action['co2_saved']} kg`  
    **💳 Credits Earned**: `{action['credits']}`  
    **💡 Tip**: {action['tip']}
    ---
    """)
st.markdown("💾 All data is stored locally in `wallet.json`")
