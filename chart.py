import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
import io

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic campaign data
n_campaigns = 120
campaign_data = {
    'marketing_spend': np.random.uniform(10, 100, n_campaigns),  # in thousands
    'conversion_rate': np.random.uniform(1, 20, n_campaigns),    # %
    'campaign_type': np.random.choice(['Social Media', 'Email', 'PPC', 'Display'], n_campaigns),
}

# Create stronger correlation between spend and conversion
for i in range(n_campaigns):
    base_conversion = campaign_data['marketing_spend'][i] * 0.15 + np.random.normal(0, 2)
    campaign_data['conversion_rate'][i] = max(0.5, min(25, base_conversion))

# Create DataFrame
df = pd.DataFrame(campaign_data)

# Set Seaborn style
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.2)

# Create barplot (✅ required for validation)
plt.figure(figsize=(8, 8))
sns.barplot(
    data=df,
    x='campaign_type',
    y='conversion_rate',
    estimator=np.mean,
    ci='sd',
    palette='Set2'
)

# Customize labels and title
plt.title('Average Conversion Rate by Campaign Type', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Campaign Type', fontsize=14, fontweight='semibold')
plt.ylabel('Conversion Rate (%)', fontsize=14, fontweight='semibold')

# Layout
plt.tight_layout()

# Save to buffer
buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=100, facecolor='white', edgecolor='none', bbox_inches='tight')
buf.seek(0)

# ✅ Resize to exactly 512x512 px
img = Image.open(buf)
img_resized = img.resize((512, 512), Image.Resampling.LANCZOS)
img_resized.save('chart.png', 'PNG', optimize=True)
buf.close()

# Print summary stats
print("Marketing Campaign Effectiveness Analysis")
print("=" * 50)
print(f"Total Campaigns: {len(df)}")
print(f"Average Marketing Spend: ${df['marketing_spend'].mean():.2f}K")
print(f"Average Conversion Rate: {df['conversion_rate'].mean():.2f}%")
