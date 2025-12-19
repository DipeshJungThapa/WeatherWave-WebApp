"""
Generate Pipeline Flowchart for WeatherWave ML System
Shows the daily automated workflow from data fetch to deployment
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Configuration
OUTPUT_FILE = "figures/fig_pipeline_flowchart.png"
DPI = 300

def create_flowchart():
    """Generate clean pipeline flowchart with larger, more readable text"""
    
    fig, ax = plt.subplots(figsize=(14, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define pipeline steps
    steps = [
        ("Fetch Data", "NASA POWER API\n77 districts\nIncremental fetch", 9.5),
        ("Quality Control", "Remove invalid values\n(-999, 999)\nValidate ranges", 8.3),
        ("Interpolation", "Fill missing values\nTime-series interpolation\nPreserve continuity", 7.1),
        ("Feature Engineering", "Add target column\nEncode districts\nAdd day_of_year", 5.9),
        ("Train Model", "Random Forest (5 trees)\n80/20 train/test split\nEvaluate MAE/R²", 4.7),
        ("Serialize & Deploy", "Save model (.pkl)\nUpload to Google Drive\nOverwrite old version", 3.5),
        ("Generate Predictions", "Load latest model\nPredict next-day temps\n77 districts", 2.3),
    ]
    
    # Colors
    fetch_color = '#E3F2FD'      # Light blue
    process_color = '#FFF3E0'    # Light orange
    train_color = '#E8F5E9'      # Light green
    deploy_color = '#F3E5F5'     # Light purple
    predict_color = '#FFF9C4'    # Light yellow
    
    colors = [fetch_color, process_color, process_color, process_color, 
              train_color, deploy_color, predict_color]
    
    box_width = 6.5
    box_height = 1.0
    x_center = 5
    
    # Draw boxes and arrows
    for i, ((title, desc, y), color) in enumerate(zip(steps, colors)):
        # Box
        box = FancyBboxPatch(
            (x_center - box_width/2, y - box_height/2),
            box_width, box_height,
            boxstyle="round,pad=0.1",
            edgecolor='black',
            facecolor=color,
            linewidth=2.5
        )
        ax.add_patch(box)
        
        # Title (bold, larger)
        ax.text(x_center, y + 0.2, title, 
                ha='center', va='center', 
                fontsize=15, fontweight='bold')
        
        # Description (larger, readable)
        ax.text(x_center, y - 0.2, desc, 
                ha='center', va='center', 
                fontsize=11, style='italic', color='#444')
        
        # Arrow to next step
        if i < len(steps) - 1:
            arrow = FancyArrowPatch(
                (x_center, y - box_height/2 - 0.05),
                (x_center, steps[i+1][2] + box_height/2 + 0.05),
                arrowstyle='->,head_width=0.5,head_length=0.5',
                color='black',
                linewidth=3,
                zorder=1
            )
            ax.add_patch(arrow)
    
    # Title
    ax.text(5, 11.2, 'Daily Automated ML Pipeline', 
            ha='center', va='center', 
            fontsize=18, fontweight='bold')
    
    # Schedule indicator
    schedule_box = FancyBboxPatch(
        (0.3, 10.4), 3.2, 0.7,
        boxstyle="round,pad=0.08",
        edgecolor='#1976D2',
        facecolor='#BBDEFB',
        linewidth=2
    )
    ax.add_patch(schedule_box)
    ax.text(1.9, 10.75, 'Daily: 00:00 UTC', 
            ha='center', va='center', 
            fontsize=12, fontweight='bold')
    
    # Outcome indicator
    outcome_box = FancyBboxPatch(
        (6.5, 10.4), 3.2, 0.7,
        boxstyle="round,pad=0.08",
        edgecolor='#388E3C',
        facecolor='#C8E6C9',
        linewidth=2
    )
    ax.add_patch(outcome_box)
    ax.text(8.1, 10.75, 'Prevents Seasonal Drift', 
            ha='center', va='center', 
            fontsize=12, fontweight='bold')
    
    # Footer note
    ax.text(5, 0.8, 
            'Automated via GitHub Actions • No Manual Intervention Required', 
            ha='center', va='center', 
            fontsize=11, style='italic', color='#555')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✅ Saved: {OUTPUT_FILE}")

def main():
    print("=" * 70)
    print("GENERATING PIPELINE FLOWCHART")
    print("=" * 70)
    print()
    
    create_flowchart()
    
    print("\n" + "=" * 70)
    print("✅ FLOWCHART GENERATED SUCCESSFULLY")
    print("=" * 70)
    print("\nFile: figures/fig_pipeline_flowchart.png")
    print("Purpose: Shows daily automated ML pipeline")
    print("Usage: Methods section (System Architecture)")

if __name__ == "__main__":
    main()
