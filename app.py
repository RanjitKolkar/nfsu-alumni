import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="NFSU Goa Alumni Portal", layout="wide")

# -----------------------------
# Program Colors
# -----------------------------
program_colors = {
"B. SC. M. SC. FORENSIC SCIENCE": "#e52b50",
"M. SC. DIGITAL FORESNIC AND INFORMATION SECURITY": "#50c878",
"M. TECH. AIDS( SPECIALIZATION IN CYBER SECURITY)": "#b37fff",
"M. SC. CYBER SECURITY": "#ffc94f",
"M. SC. FORENSIC SCIENCE": "#00acfe"
}

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("alumni_data.xlsx")

    df["PASSING YEAR"] = pd.to_numeric(df["PASSING YEAR"], errors="coerce")
    df = df.dropna(subset=["PASSING YEAR"])
    df["PASSING YEAR"] = df["PASSING YEAR"].astype(int)

    # Clean text fields
    df["Program"] = df["Program"].str.strip()
    df["Name"] = df["Name"].str.strip()

    return df

df = load_data()

# Hide future batches
current_year = datetime.datetime.now().year
df = df[df["PASSING YEAR"] < current_year]

# Last update from file
file_time = os.path.getmtime("alumni_data.xlsx")
last_update = datetime.datetime.fromtimestamp(file_time).strftime("%d %B %Y")

# -----------------------------
# CSS Styling
# -----------------------------
st.markdown("""
<style>

.main {
background-color:#f2f5f9;
}

/* Header */
.portal-title{
color:#1a237e;
font-size:36px;
font-weight:bold;
margin-top:10px;
}

/* Cards */
.card{
background:white;
padding:16px;
border-radius:10px;
box-shadow:0 2px 8px rgba(0,0,0,0.12);
margin-bottom:14px;
text-align:center;
transition:0.2s;
}

.card:hover{
transform:translateY(-3px);
}

.name{
font-size:17px;
font-weight:bold;
color:#0d47a1;
}

.program{
font-size:14px;
color:#555;
}

.year{
font-size:12px;
color:#777;
}

/* Year Header */
.year-header{
background:#1a237e;
color:white;
padding:12px;
border-radius:8px;
font-size:20px;
font-weight:bold;
margin-top:25px;
}

/* Divider */
.program-divider{
height:4px;
border-radius:4px;
margin-bottom:15px;
}

/* Announcement */
.announce{
background:#fff3cd;
padding:14px;
border-left:5px solid #ff9800;
border-radius:6px;
margin-bottom:20px;
}

.register-btn{
display:inline-block;
background:#3949ab;
color:white !important;
padding:10px 20px;
border-radius:6px;
text-decoration:none;
font-weight:bold;
border:2px solid #3949ab;
transition:0.2s;
}

.register-btn:hover{
background:white;
color:#1a237e !important;
border:2px solid #1a237e;
text-decoration:none;
}
.register-btn:focus{
outline:none;
box-shadow:0 0 5px rgba(26,35,126,0.6);
}
/* Footer */
.footer{
text-align:center;
padding:20px;
background:#f2f4ff;
border-radius:8px;
font-size:14px;
margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
col1, col2 = st.columns([1,3])

with col1:
    st.image("logo.png", use_container_width=True)

with col2:
    st.markdown("<div class='portal-title'>🎓 NFSU Goa – Alumni Portal</div>", unsafe_allow_html=True)

# -----------------------------
# Announcements
# -----------------------------
st.subheader("📢 Announcements")

st.markdown("""
<div class="announce">
• NFSU Goa, first Alumni Meet will be scheduled in April 2026.<br>
• Update your alumni details through the registration form.<br>
• Alumni mentorship program launching soon.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Register Button
# -----------------------------
google_form_link = "YOUR_GOOGLE_FORM_LINK"

st.markdown(
f'<a href="{google_form_link}" target="_blank" class="register-btn">Register as Alumni</a>',
unsafe_allow_html=True
)

st.write("")

# -----------------------------
# Search
# -----------------------------
search = st.text_input("🔍 Search Alumni")

if search:
    df = df[df["Name"].str.contains(search, case=False)]

# -----------------------------
# Alumni Directory
# -----------------------------
st.markdown("### 🎓 Alumni Directory")
st.markdown(
f"<span style='font-size:14px;color:gray;'>Last updated: {last_update}</span>",
unsafe_allow_html=True
)

years = sorted(df["PASSING YEAR"].unique(), reverse=True)

for year in years:

    st.markdown(
        f"<div class='year-header'>🎓 Class of {year}</div>",
        unsafe_allow_html=True
    )

    with st.expander("View / Hide Alumni", expanded=True):

        year_df = df[df["PASSING YEAR"] == year]

        programs = year_df["Program"].unique()

        for program in programs:

            color = program_colors.get(program, "#00acfe")

            st.markdown(f"### {program}")

            st.markdown(
                f"<div class='program-divider' style='background:{color}'></div>",
                unsafe_allow_html=True
            )

            program_df = year_df[year_df["Program"] == program]

            # Responsive card layout
            num_cols = 4
            cols = st.columns(num_cols)

            for idx, row in enumerate(program_df.itertuples()):

                with cols[idx % num_cols]:

                    st.markdown(f"""
                    <div class="card" style="border-top:5px solid {color}">
                    <div class="name">{row.Name}</div>
                    <div class="program">{row.Program}</div>
                    <div class="year">Class of {row._3}</div>
                    </div>
                    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div class="footer">

<b>National Forensic Sciences University, Goa Campus</b><br>

Alumni Engagement Portal – Developed for NFSU Goa Alumni Network<br><br>

<b>Placement Cell – NFSU Goa</b><br>
📧 Email: <a href="mailto:placement_goa@nfsu.ac.in">placement_goa@nfsu.ac.in</a><br><br>

© 2026 National Forensic Sciences University, Goa. All Rights Reserved.

</div>
""", unsafe_allow_html=True)