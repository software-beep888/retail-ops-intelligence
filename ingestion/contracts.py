"""
Simple data contracts - fail-fast validation only.
NO over-engineering, NO auto-healing of schema drift.
"""

from typing import Dict, List, Tuple
import pandas as pd


class DataContract:
    """Simple data contract that fails fast on validation issues."""

    # Define expected schemas for each data type
    SCHEMAS = {
        'promotions': {
            'required_columns': [
                'promotion_id', 'store_id', 'start_date', 'end_date',
                'discount_pct', 'promotion_type'  # NOTE: discount_pct is required
            ],
            'business_rules': {
                'discount_pct': lambda x: (x >= 0) & (x <= 1)
            }
        },
        'sales': {
            'required_columns': ['date', 'store_id', 'total_sales'],
            'business_rules': {
                'total_sales': lambda x: x >= 0
            }
        },
        'inventory': {
            'required_columns': ['date', 'store_id'],
            'business_rules': {}
        },
        'stores': {
            'required_columns': ['store_id', 'store_name', 'region'],
            'business_rules': {}
        }
    }

    def __init__(self, data_type: str):
        self.data_type = data_type
        self.schema = self.SCHEMAS.get(data_type, {})

    def validate(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate data against contract.
        Returns: (is_valid, list_of_errors)
        """
        errors = []

        # 1. Check required columns
        required_columns = self.schema.get('required_columns', [])
        missing_columns = [
            col for col in required_columns if col not in df.columns]

        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")

            # CRITICAL: If discount_pct is missing from promotions, fail hard
            if self.data_type == 'promotions' and 'discount_pct' in missing_columns:
                errors.append(
                    "SCHEMA DRIFT DETECTED: discount_pct column missing. "
                    "Pipeline stopped to protect data trust. "
                    "Contact upstream team to resolve column name change."
                )

        # 2. Check business rules
        business_rules = self.schema.get('business_rules', {})
        for column, rule in business_rules.items():
            if column in df.columns:
                try:
                    violations = df[~rule(df[column])]
                    if len(violations) > 0:
                        errors.append(
                            f"Business rule violation in {column}: "
                            f"{len(violations)} records failed"
                        )
                except Exception as e:
                    errors.append(
                        f"Error checking rule for {column}: {str(e)}")

        return len(errors) == 0, errors
