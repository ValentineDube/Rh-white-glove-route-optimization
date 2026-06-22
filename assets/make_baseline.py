# -*- coding: utf-8 -*-
"""Naive baseline vs optimized — same cost/CO2 model, only routing differs."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, os
OUT=os.path.dirname(os.path.abspath(__file__))

# ---- cost model (identical to notebook) ----
LABOR=104.0; TRUCK_MI=1.205; CO2_MI=1.69; CO2_IDLE_HR=3.97; PREP=23.0

# Per-customer one-way warehouse distance (notebook cell 66/70) — 14 regular customers
wh_miles=[3.279987,3.279987,4.538845,8.003364,9.715911,11.284318,11.899661,
          12.203277,12.410272,12.806799,16.534681,17.270519,19.731367,20.135882]
SERVICE_MIN=1502.0            # total service/idle minutes (same in both scenarios)
IDLE_CO2=(SERVICE_MIN/60)*CO2_IDLE_HR

def scenario(drive_miles, trips):
    drive_min=drive_miles*2          # 30 mph (notebook: minutes = miles*2)
    work_min=trips*PREP + drive_min + SERVICE_MIN
    labor=work_min/60*LABOR
    truck=drive_miles*TRUCK_MI
    co2=drive_miles*CO2_MI + IDLE_CO2
    return dict(miles=drive_miles, cost=labor+truck, co2=co2, trips=trips,
                labor=labor, truck=truck)

# OPTIMIZED — official reported results (notebook daily_summary)
opt=scenario(233.783948, 6)
# NAIVE — one dedicated round trip per order (no consolidation, no sequencing)
naive=scenario(sum(wh_miles)*2, 14)

def pct(a,b): return (b-a)/b*100
print("            OPTIMIZED     NAIVE      SAVED      %")
for k,unit in [("miles","mi"),("cost","$"),("co2","kg")]:
    print(f"{k:8} {opt[k]:10.1f} {naive[k]:10.1f} {naive[k]-opt[k]:9.1f}  {pct(opt[k],naive[k]):6.1f}%")
print(f"Annualized cost saved (x52): ${ (naive['cost']-opt['cost'])*52:,.0f}")
print(f"Annualized CO2 saved (x52): { (naive['co2']-opt['co2'])*52:,.0f} kg")

# ---- comparison chart ----
NAVY="#1F3864"; GOLD="#F2C811"; GREEN="#2EA44F"; RED="#C0392B"; INK="#16202E"; GREY="#9AA6B2"
plt.rcParams.update({"font.family":"DejaVu Sans","axes.grid":True,"grid.color":"#EEF1F4",
                     "axes.axisbelow":True,"axes.edgecolor":"#D5DBE1"})
metrics=[("Drive Miles","miles","mi",""),("Operating Cost","cost","$","$"),("CO₂ Emissions","co2","kg","")]
fig,axs=plt.subplots(1,3,figsize=(12,4.4),dpi=160)
fig.suptitle("Optimization Impact — Optimized vs. Naive (no-consolidation) Baseline",
             fontsize=15,fontweight="bold",color=NAVY,y=1.02)
for ax,(title,key,unit,pre) in zip(axs,metrics):
    vals=[naive[key],opt[key]]
    bars=ax.bar([0,1],vals,color=[RED,GREEN],width=0.62)
    ax.set_xticks([0,1]); ax.set_xticklabels(["Naive","Optimized"],fontweight="bold")
    ax.set_title(title,fontweight="bold",color=INK)
    for x,v in zip([0,1],vals):
        lab=f"{pre}{v:,.0f}" if key!="miles" else f"{v:,.1f}"
        ax.text(x,v*1.02,lab,ha="center",fontweight="bold",fontsize=11,color=INK)
    ax.set_ylim(0,max(vals)*1.22)
    # savings arrow/badge
    s=pct(opt[key],naive[key])
    ax.text(0.5,max(vals)*1.13,f"▼ {s:.0f}%",ha="center",fontsize=14,fontweight="bold",color=GREEN)
    ax.set_xlim(-0.6,1.6)
fig.tight_layout(rect=[0,0,1,0.96])
fig.savefig(os.path.join(OUT,"optimization_impact.png"),facecolor="white",bbox_inches="tight")
print("\nSaved optimization_impact.png")
