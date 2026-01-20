def generate_alerts(demo_df, bio_df):
    alerts = []

    # 🔴 Critical: biometric activity
    if len(bio_df) > 0:
        alerts.append({
            "severity": "CRITICAL",
            "reason": "Biometric update activity detected",
            "count": len(bio_df)
        })

    # 🟠 Warning: high demographic burst
    if demo_df["total_updates"].max() > demo_df["total_updates"].mean() * 3:
        alerts.append({
            "severity": "WARNING",
            "reason": "Demographic update spike",
            "count": demo_df["total_updates"].max()
        })

    return alerts
