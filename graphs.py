import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# ACTUAL DATA FROM YOUR SIMULATION RUNS
# ============================================================

scenarios = ['S1\nNormal', 'S2\nHigh Load', 'S3\nQoS', 'S4\nTCP/UDP', 'S5\nFirewall']

# Packets received at server
student_pkts  = [445,   6817,  6925,  1083,  94]
teacher_pkts  = [93,    373,   361,   218,   0]
admin_pkts    = [0,     0,     268,   0,     0]

# Total events per scenario
events        = [22137, 537977, 552422, 2046233, 3692]

# Messages created
messages      = [13030, 341137, 349216, 1087478, 2157]

# Real-time duration (seconds)
realtime      = [0.158, 2.793, 2.685, 12.620, 0.037]

colors = ['#2196F3', '#F44336', '#FF9800', '#4CAF50', '#9C27B0']

# ============================================================
# GRAPH 1: Packets Received at Server (Grouped Bar)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(scenarios))
width = 0.25

bars1 = ax.bar(x - width, student_pkts, width, label='Student (app[0])', color='#2196F3')
bars2 = ax.bar(x,         teacher_pkts, width, label='Teacher (app[1])', color='#4CAF50')
bars3 = ax.bar(x + width, admin_pkts,   width, label='Admin (app[2])',   color='#FF9800')

ax.set_title('Packets Received at Campus Server per Scenario', fontsize=14, fontweight='bold')
ax.set_xlabel('Scenario')
ax.set_ylabel('Number of Packets Received')
ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar in bars1:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2, h + 50, str(int(h)),
                ha='center', va='bottom', fontsize=8)
for bar in bars2:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2, h + 50, str(int(h)),
                ha='center', va='bottom', fontsize=8)
for bar in bars3:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x() + bar.get_width()/2, h + 50, str(int(h)),
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('graph1_packets_received.png', dpi=150)
plt.show()
print("Graph 1 saved!")

# ============================================================
# GRAPH 2: Total Simulation Events (Bar Chart)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(scenarios, events, color=colors, edgecolor='black', linewidth=0.5)

ax.set_title('Total Simulation Events per Scenario\n(Higher = More Network Activity)', 
             fontsize=14, fontweight='bold')
ax.set_xlabel('Scenario')
ax.set_ylabel('Number of Events (Log Scale)')
ax.set_yscale('log')
ax.grid(axis='y', alpha=0.3)

for bar, val in zip(bars, events):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.1,
            f'{val:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('graph2_total_events.png', dpi=150)
plt.show()
print("Graph 2 saved!")

# ============================================================
# GRAPH 3: Real-Time Simulation Duration (Bar Chart)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(scenarios, realtime, color=colors, edgecolor='black', linewidth=0.5)

ax.set_title('Real-Time Simulation Duration per Scenario\n(Higher = More Computational Load)', 
             fontsize=14, fontweight='bold')
ax.set_xlabel('Scenario')
ax.set_ylabel('Real Time Elapsed (seconds)')
ax.grid(axis='y', alpha=0.3)

for bar, val in zip(bars, realtime):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f'{val}s', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('graph3_realtime_duration.png', dpi=150)
plt.show()
print("Graph 3 saved!")

# ============================================================
# GRAPH 4: Network Load Comparison (S1 vs S2 vs S3)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: Student packets S1 vs S2 vs S3
s_names = ['S1\nNormal', 'S2\nHigh Load', 'S3\nQoS']
s_student = [445, 6817, 6925]
s_teacher = [93, 373, 361]
s_admin   = [0, 0, 268]

x = np.arange(3)
w = 0.25
axes[0].bar(x - w, s_student, w, label='Student', color='#2196F3')
axes[0].bar(x,     s_teacher, w, label='Teacher', color='#4CAF50')
axes[0].bar(x + w, s_admin,   w, label='Admin',   color='#FF9800')
axes[0].set_title('S1 vs S2 vs S3: Packet Delivery', fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(s_names)
axes[0].set_ylabel('Packets Received')
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Right: QoS effect - Admin gets 268 in S3, 0 in S2
categories = ['S2: High Load\n(No QoS)', 'S3: QoS Active\n(DSCP Priority)']
admin_vals = [0, 268]
bar_colors = ['#F44336', '#4CAF50']
axes[1].bar(categories, admin_vals, color=bar_colors, edgecolor='black', width=0.4)
axes[1].set_title('QoS Effect on Admin Traffic\n(app[2] packets received)', fontweight='bold')
axes[1].set_ylabel('Admin Packets Received at Server')
axes[1].grid(axis='y', alpha=0.3)
for i, v in enumerate(admin_vals):
    axes[1].text(i, v + 5, str(v), ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('graph4_qos_comparison.png', dpi=150)
plt.show()
print("Graph 4 saved!")

# ============================================================
# GRAPH 5: TCP vs UDP (Scenario 4 breakdown)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: Data volume comparison
labels = ['student1\n(TCP)', 'student2\n(TCP)', 'student3+4\n(UDP)']
data_received = [10.85, 11.85, 0]   # MB received (TCP gets large replies)
data_sent     = [0.058, 0.053, 1.083*1.0/1000*1024]  # approx MB sent

x = np.arange(3)
w = 0.35
axes[0].bar(x - w/2, data_received, w, label='Data Received (MB)', color='#2196F3')
axes[0].bar(x + w/2, data_sent,     w, label='Data Sent (MB)',     color='#FF9800')
axes[0].set_title('Scenario 4: TCP vs UDP Data Volume', fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(labels)
axes[0].set_ylabel('Data (MB)')
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Right: TCP sessions opened
tcp_labels = ['student1\n(TCP)', 'student2\n(TCP)']
sessions = [20, 17]
axes[1].bar(tcp_labels, sessions, color=['#2196F3', '#1565C0'], edgecolor='black', width=0.4)
axes[1].set_title('Scenario 4: TCP Sessions Opened\n(in 60 simulated seconds)', fontweight='bold')
axes[1].set_ylabel('Number of TCP Sessions')
axes[1].grid(axis='y', alpha=0.3)
for i, v in enumerate(sessions):
    axes[1].text(i, v + 0.3, str(v), ha='center', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('graph5_tcp_vs_udp.png', dpi=150)
plt.show()
print("Graph 5 saved!")

print("\n✓ All 5 graphs saved as PNG files in the same folder as this script!")