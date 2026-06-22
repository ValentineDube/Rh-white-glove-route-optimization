# -*- coding: utf-8 -*-
"""Generate portfolio visuals from the real optimized results (Team 8 dataset)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- Real per-day results (from notebook cell 86 daily_summary) ----
days   = ["Tue", "Wed", "Thu", "Fri", "Sat"]
labor  = [904.647, 735.516, 671.253, 832.351, 509.350]
truck  = [78.874, 49.909, 58.299, 60.372, 34.256]
co2_dr = [110.620, 69.997, 81.763, 84.671, 48.043]
co2_id = [24.349, 21.074, 17.700, 22.100, 14.160]
miles  = [65.456, 41.418, 48.381, 50.101, 28.428]
util   = [0.9665, 0.7858, 0.7172, 0.8893, 0.5442]
stops  = [3, 2, 4, 3, 2]
total_cost = [l+t for l, t in zip(labor, truck)]
total_co2  = [d+i for d, i in zip(co2_dr, co2_id)]

NAVY="#1F3864"; GOLD="#F2C811"; GREEN="#2EA44F"; SLATE="#5B6B7B"; LIGHT="#AEB6BF"; INK="#16202E"
plt.rcParams.update({"font.family":"DejaVu Sans","axes.edgecolor":"#D5DBE1",
                     "axes.grid":True,"grid.color":"#EEF1F4","grid.linewidth":1,
                     "axes.axisbelow":True})

# ============ 1. HERO BANNER ============
fig = plt.figure(figsize=(12, 3.4), dpi=200)
fig.patch.set_facecolor(INK)
ax = fig.add_axes([0,0,1,1]); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,3.4)
# subtle accent bar
ax.add_patch(plt.Rectangle((0,0),0.16,3.4, color=GOLD))
ax.text(0.55,2.5,"RH White-Glove Delivery Route Optimization",
        color="white",fontsize=23,fontweight="bold",va="center")
ax.text(0.57,1.95,"Cost- & CO₂-minimized delivery scheduling  ·  Python + Google OR-Tools  ·  Power BI",
        color=LIGHT,fontsize=12.5,va="center")
chips=[("233.8","miles / week"),("$3,935","weekly cost"),("494.5 kg","CO₂ tracked"),
       ("~$281","cost / delivery"),("78%","avg utilization")]
x=0.57
for big,small in chips:
    w=2.18
    ax.add_patch(FancyBboxPatch((x,0.35),w,1.05,boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc="#243447",ec=GOLD,lw=1.1))
    ax.text(x+w/2,1.02,big,color=GOLD,fontsize=15.5,fontweight="bold",ha="center",va="center")
    ax.text(x+w/2,0.6,small,color=LIGHT,fontsize=9.5,ha="center",va="center")
    x+=w+0.18
fig.savefig(os.path.join(OUT,"hero_banner.png"),facecolor=INK,bbox_inches="tight")
plt.close(fig)

# ============ 2. RESULTS OVERVIEW (2x2) ============
fig,axs=plt.subplots(2,2,figsize=(12,8),dpi=160)
fig.suptitle("Optimized Weekly Delivery Plan — Results Overview",
             fontsize=16,fontweight="bold",color=NAVY,y=0.98)
x=np.arange(len(days))

# (a) cost stacked
a=axs[0,0]
a.bar(x,labor,color=NAVY,label="Labor")
a.bar(x,truck,bottom=labor,color=GOLD,label="Truck / Fuel")
for i,t in enumerate(total_cost):
    a.text(i,t+25,f"${t:,.0f}",ha="center",fontsize=9,fontweight="bold",color=INK)
a.set_title("Daily Operating Cost",fontweight="bold",color=INK)
a.set_ylabel("USD"); a.set_xticks(x); a.set_xticklabels(days); a.legend(frameon=False,fontsize=9)
a.set_ylim(0,1100)

# (b) CO2 stacked
b=axs[0,1]
b.bar(x,co2_dr,color=GREEN,label="Driving")
b.bar(x,co2_id,bottom=co2_dr,color="#9CD3A8",label="Idling")
for i,t in enumerate(total_co2):
    b.text(i,t+3,f"{t:,.0f}",ha="center",fontsize=9,fontweight="bold",color=INK)
b.set_title("Daily CO₂ Emissions",fontweight="bold",color=INK)
b.set_ylabel("kg CO₂"); b.set_xticks(x); b.set_xticklabels(days); b.legend(frameon=False,fontsize=9)
b.set_ylim(0,160)

# (c) utilization
c=axs[1,0]
bars=c.bar(x,[u*100 for u in util],color=[GOLD if u<0.6 else NAVY for u in util])
c.axhline(100,color=SLATE,ls="--",lw=1.2)
c.text(4.4,101,"capacity (9h)",fontsize=8,color=SLATE,ha="right")
avg=np.mean(util)*100
c.axhline(avg,color=GREEN,ls=":",lw=1.5)
c.text(-0.45,avg+2,f"avg {avg:.0f}%",fontsize=8,color=GREEN)
for i,u in enumerate(util):
    c.text(i,u*100+2,f"{u*100:.0f}%",ha="center",fontsize=9,fontweight="bold",color=INK)
c.set_title("Truck & Crew Utilization",fontweight="bold",color=INK)
c.set_ylabel("% of 9-hour day"); c.set_xticks(x); c.set_xticklabels(days); c.set_ylim(0,115)

# (d) miles + cumulative cost
d=axs[1,1]
d.bar(x,miles,color="#6C8EBF",label="Drive miles")
d.set_ylabel("Miles",color="#3A5A8C"); d.set_xticks(x); d.set_xticklabels(days)
for i,m in enumerate(miles):
    d.text(i,m+1,f"{m:.0f}",ha="center",fontsize=9,color=INK)
d2=d.twinx(); d2.grid(False)
cum=np.cumsum(total_cost)
d2.plot(x,cum,color=NAVY,marker="o",lw=2,label="Cumulative cost")
d2.set_ylabel("Cumulative $",color=NAVY)
for i,cc in enumerate(cum):
    d2.text(i,cc+90,f"${cc:,.0f}",ha="center",fontsize=8,color=NAVY)
d.set_title("Distance & Cumulative Cost",fontweight="bold",color=INK)
d2.set_ylim(0,4600)
fig.tight_layout(rect=[0,0,1,0.96])
fig.savefig(os.path.join(OUT,"results_overview.png"),facecolor="white",bbox_inches="tight")
plt.close(fig)

# ============ 3. COST-PER-DELIVERY vs $299 FEE ============
fig,ax=plt.subplots(figsize=(11,4.3),dpi=160)
# approx cost per delivery on each day = total_cost/stops (illustrative)
cpd=[t/s for t,s in zip(total_cost,stops)]
order_labels=[f"{d}\n({s} stops)" for d,s in zip(days,stops)]
bars=ax.bar(x,cpd,color=[GREEN if v<=299 else "#C0392B" for v in cpd])
ax.axhline(299,color=NAVY,lw=2,ls="--")
ax.text(4.45,309,"$299 flat fee",color=NAVY,fontweight="bold",ha="right",fontsize=10)
for i,v in enumerate(cpd):
    ax.text(i,v+6,f"${v:,.0f}",ha="center",fontsize=10,fontweight="bold",color=INK)
ax.set_title("Avg Cost per Delivery vs. $299 Flat Fee  (by day / load)",
             fontsize=13,fontweight="bold",color=NAVY)
ax.set_ylabel("USD per delivery"); ax.set_xticks(x); ax.set_xticklabels(order_labels)
ax.set_ylim(0,420)
fig.tight_layout()
fig.savefig(os.path.join(OUT,"cost_per_delivery.png"),facecolor="white",bbox_inches="tight")
plt.close(fig)

print("Generated:",[f for f in os.listdir(OUT) if f.endswith(".png")])
