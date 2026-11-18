"""Generate deterministic synthetic training data. Not human learner data."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(47)
rows = []
labels = ["التصيد الإلكتروني", "حماية الخصوصية", "كلمات المرور"]
for _ in range(900):
    scores = rng.integers(20, 101, size=3)
    # deterministic educational rule: weakest domain is the target; ties resolved by fixed order
    idx = int(np.argmin(scores))
    errors = int(round((300 - scores.sum()) / 20 + rng.integers(0, 4)))
    rows.append([*map(int, scores), max(0, errors), labels[idx]])
df = pd.DataFrame(rows, columns=["phishing_score","privacy_score","password_score","errors","recommended_topic"])
df.to_csv(Path(__file__).resolve().parent / "data.csv", index=False, encoding="utf-8-sig")
print(f"Wrote {len(df)} synthetic rows to data.csv")
