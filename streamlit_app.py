# ==============================================================
# 🔹 SECTION 6: IMPLEMENTATION ROADMAP – DIGITAL OVERSIGHT PILOT
# ==============================================================

import plotly.figure_factory as ff
import plotly.io as pio
import pandas as pd

# Use a consistent theme with the rest of your dashboard (dark mode for clarity)
pio.templates.default = "plotly_dark"

# Define the pilot roadmap phases (aligned with your earlier project scope)
phases = [
    dict(Task='Phase 1: Project Planning & Vendor Setup', 
         Start='2025-01-01', Finish='2025-02-28', Resource='Planning'),
    
    dict(Task='Phase 2: Shop-Floor Telemetry Installation', 
         Start='2025-03-01', Finish='2025-04-30', Resource='Implementation'),
    
    dict(Task='Phase 3: Supplier Telemetry Integration', 
         Start='2025-05-01', Finish='2025-06-30', Resource='Integration'),
    
    dict(Task='Phase 4: Pilot Operations & Predictive Analytics', 
         Start='2025-07-01', Finish='2025-12-31', Resource='Analytics'),
    
    dict(Task='Phase 5: Unified KPI Dashboards Deployment', 
         Start='2025-07-01', Finish='2025-12-31', Resource='Dashboard'),
    
    dict(Task='Phase 6: Results Review & Scale-Up Decision', 
         Start='2025-12-31', Finish='2025-12-31', Resource='Review')
]

# Custom color palette for better visual contrast
colors = {
    'Planning': '#00BFFF',       # Bright blue
    'Implementation': '#2ECC71', # Green
    'Integration': '#9B59B6',    # Purple
    'Analytics': '#F39C12',      # Orange
    'Dashboard': '#1ABC9C',      # Cyan
    'Review': '#E74C3C'          # Red
}

# Create Gantt chart with Plotly
fig = ff.create_gantt(
    phases,
    index_col='Resource',
    colors=colors,
    show_colorbar=True,
    group_tasks=True,
    title='🚀 Digital Production Oversight Pilot – Implementation Roadmap (2025)',
    bar_width=0.4,
    showgrid_x=True,
    showgrid_y=True,
    height=550
)

# Style improvements
fig.update_layout(
    title_font=dict(size=22, family='Arial Black', color='#00BFFF'),
    plot_bgcolor='#0f1117',
    paper_bgcolor='#0f1117',
    font=dict(color='white', size=12),
    xaxis=dict(
        title='Timeline (Months)',
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        tickangle=-30
    ),
    yaxis=dict(
        title='Project Phases',
        showgrid=False
    ),
    hoverlabel=dict(bgcolor='white', font_size=12, font_family="Arial"),
    margin=dict(l=180, r=60, t=100, b=50)
)

# Optional transparency and smooth hover interaction
fig.update_traces(opacity=0.9, selector=dict(type='bar'))

# Display the interactive roadmap
fig.show()
