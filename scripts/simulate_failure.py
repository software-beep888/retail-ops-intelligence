#!/usr/bin/env python3
"""
Simulate schema drift failure for Loom demo.
This script intentionally breaks the promotions data to demonstrate fail-fast validation.
"""

import pandas as pd
import os
from datetime import datetime


def simulate_schema_drift():
    """Rename discount_pct column to simulate upstream schema change."""
    print("🚨 Simulating schema drift for Loom demo...")

    # Read the promotions data
    promotions_path = "data/promotions.csv"

    if not os.path.exists(promotions_path):
        print(f"❌ File not found: {promotions_path}")
        return False

    # Load the data
    df = pd.read_csv(promotions_path)

    # Check if discount_pct exists
    if 'discount_pct' not in df.columns:
        print("❌ discount_pct column already missing. Nothing to simulate.")
        return False

    # Rename the column to simulate schema drift
    df = df.rename(columns={'discount_pct': 'discount_percent'})

    # Save backup of original
    backup_path = f"data/promotions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    pd.read_csv(promotions_path).to_csv(backup_path, index=False)

    # Save modified file
    df.to_csv(promotions_path, index=False)

    print(f"✅ Schema drift simulated:")
    print(f"   • Renamed 'discount_pct' → 'discount_percent'")
    print(f"   • Original backed up to: {backup_path}")
    print(f"\n🎬 For Loom demo:")
    print(f"   1. Run pipeline: python -m ingestion.pipeline --data-dir ./data")
    print(f"   2. It will FAIL with schema drift error")
    print(f"   3. Dashboard will show 'Promotion diagnostics unavailable'")

    return True


def restore_original():
    """Restore the original promotions data."""
    import glob

    # Find the most recent backup
    backups = glob.glob("data/promotions_backup_*.csv")

    if not backups:
        print("❌ No backups found")
        return False

    latest_backup = max(backups, key=os.path.getctime)

    # Restore from backup
    df = pd.read_csv(latest_backup)
    df.to_csv("data/promotions.csv", index=False)

    print(f"✅ Original data restored from: {latest_backup}")

    # Clean up backup
    os.remove(latest_backup)

    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Simulate schema drift for demo')
    parser.add_argument('--restore', action='store_true',
                        help='Restore original data')

    args = parser.parse_args()

    if args.restore:
        restore_original()
    else:
        simulate_schema_drift()
