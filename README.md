# DEBRIX SecureADR — 5-Screen Prototype

A simulation-based proof of concept for the DEBRIX SecureADR ideathon concept.

## Screens
1. Orbital Digital Twin
2. AI Priority Dashboard
3. Secure ADR Mission Planner
4. Cyberattack Simulation
5. Trusted Removal & Mission Ledger

## Run on Windows
1. Install Python 3.11 or 3.12.
2. Open PowerShell in this folder.
3. Create a virtual environment:
   `py -m venv .venv`
4. Activate it:
   `.venv\Scripts\Activate.ps1`
5. Install packages:
   `pip install -r requirements.txt`
6. Start:
   `streamlit run app.py`

## Demo sequence for judges
1. Open Orbital Digital Twin and select DX-2047.
2. Show its simulated risk and orbital position.
3. Open AI Priority Dashboard and explain prioritization.
4. Open Secure ADR Mission Planner and generate a verified plan.
5. Open Cyberattack Simulation and click "Simulate Command Tampering".
6. Show "UNAUTHORIZED COMMAND BLOCKED".
7. Resume the trusted mission.
8. Open Trusted Removal & Mission Ledger and run the removal simulation.
9. Explain that the ledger provides tamper-evident evidence of mission events.

## Important
This is a simulation/prototype. It does not connect to or control real spacecraft.
