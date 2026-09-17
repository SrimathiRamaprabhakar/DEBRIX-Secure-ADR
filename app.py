
import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import time
import plotly.graph_objects as go

st.set_page_config(
    page_title="DEBRIX SecureADR",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Theme ----------
st.markdown("""
<style>
.stApp {background: #090909; color: #f5f5f5;}
[data-testid="stSidebar"] {background: #111111;}
h1,h2,h3 {color: #f4c430 !important;}
.small {color:#a9a9a9;font-size:0.88rem;}
.metric-card {
    background:#151515;border:1px solid #333;border-radius:14px;
    padding:18px;height:100%;
}
.good {color:#61d095;font-weight:700;}
.bad {color:#ff5c5c;font-weight:700;}
.warn {color:#f4c430;font-weight:700;}
.codebox {
    background:#050505;border:1px solid #444;border-radius:10px;
    padding:12px;font-family:monospace;
}
</style>
""", unsafe_allow_html=True)

# ---------- State ----------
if "attack" not in st.session_state: st.session_state.attack = False
if "mission" not in st.session_state: st.session_state.mission = "READY"
if "ledger" not in st.session_state:
    st.session_state.ledger = []
if "selected" not in st.session_state: st.session_state.selected = "DX-2047"

debris = pd.DataFrame([
    ["DX-2047", 91, 760, "HIGH", 2.1, "Verified"],
    ["DX-3091", 78, 690, "HIGH", 3.7, "Verified"],
    ["DX-1182", 63, 540, "MEDIUM", 6.2, "Verified"],
    ["DX-4420", 41, 820, "LOW", 10.4, "Verified"],
    ["DX-5006", 27, 610, "LOW", 13.1, "Verified"],
], columns=["Debris ID","Risk Score","Altitude (km)","Priority","Relative Risk","Identity"])

# ---------- Helpers ----------
def add_ledger(event, status="VERIFIED"):
    prev = st.session_state.ledger[-1]["hash"] if st.session_state.ledger else "GENESIS"
    payload = f"{prev}|{event}|{status}|{time.time_ns()}"
    h = hashlib.sha256(payload.encode()).hexdigest()[:16]
    st.session_state.ledger.append({
        "time": time.strftime("%H:%M:%S"),
        "event": event,
        "status": status,
        "hash": h
    })

def orbit_figure(selected):
    t = np.linspace(0, 2*np.pi, 260)
    earth = go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers",
        marker=dict(size=20, color="#4aa3ff"),
        name="Earth"
    )
    traces = [earth]
    radii = [1.5, 2.0, 2.5, 3.0]
    for i,r in enumerate(radii):
        traces.append(go.Scatter3d(
            x=r*np.cos(t), y=r*np.sin(t), z=0.18*np.sin(2*t+i),
            mode="lines", line=dict(width=2),
            name=f"Orbit {i+1}", showlegend=False
        ))
    # Target
    angle = 0.8
    tx, ty = 2.5*np.cos(angle), 2.5*np.sin(angle)
    traces.append(go.Scatter3d(
        x=[tx], y=[ty], z=[0.18*np.sin(2*angle+2)],
        mode="markers+text",
        marker=dict(size=9, color="#f4c430"),
        text=[selected], textposition="top center",
        name="Target Debris"
    ))
    # ADR craft
    a = np.linspace(angle-0.8, angle-0.05, 60)
    traces.append(go.Scatter3d(
        x=2.5*np.cos(a), y=2.5*np.sin(a),
        z=0.18*np.sin(2*a+2)+0.12,
        mode="lines+markers",
        line=dict(width=5, color="#ffffff"),
        marker=dict(size=3),
        name="ADR spacecraft"
    ))
    fig = go.Figure(traces)
    fig.update_layout(
        height=510, margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="#090909", plot_bgcolor="#090909",
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            zaxis=dict(visible=False), bgcolor="#090909",
            aspectmode="cube"
        ),
        legend=dict(font=dict(color="white"))
    )
    return fig

# ---------- Header ----------
st.markdown("# 🚀 DEBRIX SecureADR")
st.markdown("### **SECURE THE MISSION. REMOVE THE DEBRIS.**")
st.markdown('<div class="small">Simulation-based proof of concept • Cybersecurity + Digital Twin + AI + Digital Trust</div>', unsafe_allow_html=True)
st.divider()

# ---------- Sidebar navigation ----------
screen = st.sidebar.radio(
    "MISSION CONSOLE",
    [
        "1 · Orbital Digital Twin",
        "2 · AI Priority Dashboard",
        "3 · Secure ADR Mission Planner",
        "4 · Cyberattack Simulation",
        "5 · Trusted Removal & Ledger",
    ]
)

st.sidebar.divider()
st.sidebar.markdown("**SYNERGY SEEKERS**")
st.sidebar.write("Srimathi R")
st.sidebar.write("Judith Joanna E")
st.sidebar.write("Velammal College of Engineering and Technology")
st.sidebar.divider()
st.sidebar.caption("This prototype simulates the workflow. It does not control real spacecraft.")

# ---------- Screen 1 ----------
if screen.startswith("1"):
    st.header("01 · Orbital Digital Twin")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Tracked Objects", "5")
    c2.metric("High Priority", "2")
    c3.metric("Selected Target", st.session_state.selected)
    c4.metric("Twin Status", "SYNCED")

    left,right = st.columns([2.2,1])
    with left:
        st.plotly_chart(orbit_figure(st.session_state.selected), use_container_width=True)
    with right:
        st.subheader("Target selection")
        chosen = st.selectbox("Debris object", debris["Debris ID"].tolist(), index=debris["Debris ID"].tolist().index(st.session_state.selected))
        st.session_state.selected = chosen
        row = debris[debris["Debris ID"]==chosen].iloc[0]
        st.markdown(f"""
        <div class="metric-card">
        <h3>{row['Debris ID']}</h3>
        <b>Risk:</b> {row['Risk Score']}/100<br>
        <b>Altitude:</b> {row['Altitude (km)']} km<br>
        <b>Priority:</b> {row['Priority']}<br>
        <b>Identity:</b> <span class="good">✓ VERIFIED</span>
        </div>
        """, unsafe_allow_html=True)
        st.info("Digital Twin: simulated orbital representation used to preview the mission before execution.")

# ---------- Screen 2 ----------
elif screen.startswith("2"):
    st.header("02 · AI Priority Dashboard")
    st.write("AI-assisted prioritization using simulated risk features. Scores are for demonstration.")
    st.dataframe(
        debris.sort_values("Risk Score", ascending=False),
        use_container_width=True,
        hide_index=True
    )
    st.divider()
    fig = go.Figure(go.Bar(
        x=debris["Risk Score"], y=debris["Debris ID"],
        orientation="h"
    ))
    fig.update_layout(height=380, paper_bgcolor="#090909", plot_bgcolor="#090909",
                      font=dict(color="white"), xaxis_title="Simulated Risk Score",
                      yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
    selected_row = debris[debris["Debris ID"]==st.session_state.selected].iloc[0]
    st.success(f"AI recommendation: prioritize **{st.session_state.selected}** (simulated risk score {selected_row['Risk Score']}/100).")
    st.caption("Prototype note: a production system would use validated SSA/orbital datasets and a tested ML model.")

# ---------- Screen 3 ----------
elif screen.startswith("3"):
    st.header("03 · Secure ADR Mission Planner")
    target = st.session_state.selected
    st.subheader(f"Mission target: {target}")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("#### Mission sequence")
        steps = ["Rendezvous","Approach","Capture","Stabilize","Controlled deorbit","Removal verification"]
        for i,s in enumerate(steps,1):
            st.write(f"**{i}.** {s}")
    with c2:
        st.markdown("#### Zero-Trust Command Gate")
        operator = st.text_input("Operator ID", "SYNERGY-OPS-01")
        authorized = st.checkbox("Operator authenticated", True)
        target_ok = st.checkbox("Target identity verified", True)
        plan_ok = st.checkbox("Mission plan approved", True)
        integrity_ok = st.checkbox("Command integrity valid", True)
        gate = authorized and target_ok and plan_ok and integrity_ok
        if gate:
            st.success("ACCESS: ALLOW ✓")
        else:
            st.error("ACCESS: BLOCK ✕")
    st.divider()
    if st.button("Generate Secure ADR Plan", type="primary"):
        if gate:
            st.session_state.mission = "PLAN VERIFIED"
            add_ledger(f"Mission plan approved for {target}")
            st.success("ADR plan generated and passed the Zero-Trust gate.")
        else:
            st.session_state.mission = "BLOCKED"
            add_ledger(f"ADR plan blocked for {target}", "BLOCKED")
            st.error("Mission plan blocked: trust conditions not satisfied.")
    st.info("Prototype only: the plan is a simulation and does not issue spacecraft commands.")

# ---------- Screen 4 ----------
elif screen.startswith("4"):
    st.header("04 · Cyberattack Simulation")
    st.write("Demonstrate how DEBRIX responds when a trusted mission command is tampered with.")

    target = st.session_state.selected
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("Trusted command")
        st.code(f"TARGET = {target}\nACTION = CAPTURE\nAUTH = VALID\nINTEGRITY = VALID", language="text")
    with c2:
        st.subheader("Simulated attacker")
        malicious_target = "DX-3091" if target != "DX-3091" else "DX-2047"
        st.code(f"TARGET = {malicious_target}\nACTION = CAPTURE\nAUTH = VALID\nINTEGRITY = INVALID", language="text")

    if st.button("⚠ Simulate Command Tampering", type="primary"):
        st.session_state.attack = True
        st.session_state.mission = "ATTACK BLOCKED"
        add_ledger(f"Tampered command detected for {target}", "BLOCKED")

    if st.session_state.attack:
        st.error("🚨 UNAUTHORIZED COMMAND BLOCKED")
        st.markdown("""
        **DEBRIX response**

        **PAUSE → VERIFY → REJECT → RESTORE TRUSTED PLAN → RE-AUTHENTICATE**
        """)
        st.code(f"RESTORED TARGET = {target}\nCOMMAND STATUS = VERIFIED\nMISSION STATUS = SAFE", language="text")
        if st.button("Resume Trusted Mission"):
            st.session_state.attack = False
            st.session_state.mission = "RESUMED"
            add_ledger(f"Trusted mission resumed for {target}")
            st.success("Mission resumed using the verified target and command.")
    else:
        st.success("Mission command integrity: VALID ✓")
        st.caption("Press the button above to demonstrate the cyber-physical attack scenario.")

# ---------- Screen 5 ----------
else:
    st.header("05 · Trusted Removal & Mission Ledger")
    target = st.session_state.selected
    st.subheader(f"Mission: ADR-{target}")
    st.write("Simulate capture, controlled removal and verification.")

    c1,c2,c3 = st.columns(3)
    c1.metric("Target", target)
    c2.metric("Mission Status", st.session_state.mission)
    c3.metric("Trust Status", "VERIFIED ✓" if not st.session_state.attack else "BLOCKED ✕")

    if st.button("▶ Run Removal Simulation", type="primary"):
        stages = [
            ("Rendezvous completed", "VERIFIED"),
            ("Approach corridor verified", "VERIFIED"),
            ("Target captured", "VERIFIED"),
            ("Object stabilized", "VERIFIED"),
            ("Controlled removal simulated", "VERIFIED"),
            ("Removal outcome verified", "VERIFIED"),
        ]
        bar = st.progress(0)
        status = st.empty()
        for i,(event,status_text) in enumerate(stages,1):
            status.write(f"**{event}**")
            add_ledger(f"{event} — {target}", status_text)
            bar.progress(i/len(stages))
            time.sleep(0.25)
        st.session_state.mission = "REMOVAL VERIFIED"
        st.success(f"✅ {target} removal simulation completed and recorded.")

    st.divider()
    st.subheader("Tamper-evident mission ledger")
    if st.session_state.ledger:
        st.dataframe(pd.DataFrame(st.session_state.ledger), use_container_width=True, hide_index=True)
    else:
        st.info("No mission events yet. Run the Secure ADR plan or removal simulation.")

    st.caption("Ledger uses a simple SHA-256 hash chain for prototype demonstration. A production implementation could use a permissioned ledger such as Hyperledger Fabric.")
