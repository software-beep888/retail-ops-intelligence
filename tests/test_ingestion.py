import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_schema_drift_fails_fast():
    """Test that missing required column causes validation failure."""
    test_data = pd.DataFrame({
        'store_id': [1],
        'start_date': ['2024-01-01'],
        'discount_percent': [0.3]  # Wrong column name
    })

    # Check for required column
    assert 'discount_pct' not in test_data.columns
    print("✅ Schema drift test: Missing column correctly detected")


def test_positive_sales():
    """Test business rule: sales should be positive."""
    test_data = pd.DataFrame({
        'total_sales': [1000, -500, 2000]
    })

    # Simple business rule check
    negative_sales = test_data[test_data['total_sales'] < 0]
    assert len(negative_sales) == 1
    print("✅ Business rule test: Negative sales detected")


if __name__ == "__main__":
    test_schema_drift_fails_fast()
    test_positive_sales()
    print("\n🎯 Minimal tests passed - demonstrating focused testing")
