"""
Simple storage utilities - CSV-based for minimal dependencies.
"""

import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)


class SimpleStorage:
    """Minimal storage class using CSV files."""

    @staticmethod
    def save_to_csv(df: pd.DataFrame, filepath: str) -> bool:
        """
        Save DataFrame to CSV file.

        Args:
            df: DataFrame to save
            filepath: Path to save CSV file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # Save to CSV
            df.to_csv(filepath, index=False)
            logger.info(f"✅ Saved {len(df)} rows to {filepath}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to save {filepath}: {str(e)}")
            return False

    @staticmethod
    def load_from_csv(filepath: str) -> pd.DataFrame:
        """
        Load DataFrame from CSV file.

        Args:
            filepath: Path to CSV file

        Returns:
            Loaded DataFrame

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file cannot be parsed
        """
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")

            # Load CSV with appropriate date parsing
            if 'date' in filepath or 'promotions' in filepath:
                # Try to parse dates
                try:
                    df = pd.read_csv(filepath, parse_dates=True)
                except:
                    df = pd.read_csv(filepath)
            else:
                df = pd.read_csv(filepath)

            logger.info(f"📥 Loaded {len(df)} rows from {filepath}")
            return df
        except FileNotFoundError:
            logger.error(f"📂 File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to load {filepath}: {str(e)}")
            raise ValueError(f"Could not parse {filepath}: {str(e)}")

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: list) -> tuple[bool, list]:
        """
        Validate DataFrame has required columns.

        Args:
            df: DataFrame to validate
            required_columns: List of required column names

        Returns:
            Tuple of (is_valid, list_of_missing_columns)
        """
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            logger.warning(f"⚠️ Missing columns: {missing}")
            return False, missing

        logger.info(f"✅ All required columns present")
        return True, []

    @staticmethod
    def check_data_quality(df: pd.DataFrame, column_rules: dict = None) -> dict:
        """
        Perform basic data quality checks.

        Args:
            df: DataFrame to check
            column_rules: Dict of {column_name: (min_value, max_value)}

        Returns:
            Dict with quality metrics
        """
        quality_report = {
            'total_rows': len(df),
            'null_counts': {},
            'value_ranges': {},
            'issues': []
        }

        # Check for nulls
        for column in df.columns:
            null_count = df[column].isnull().sum()
            if null_count > 0:
                quality_report['null_counts'][column] = null_count
                quality_report['issues'].append(
                    f"Column {column} has {null_count} null values")

        # Check value ranges if rules provided
        if column_rules:
            for column, (min_val, max_val) in column_rules.items():
                if column in df.columns:
                    col_min = df[column].min()
                    col_max = df[column].max()
                    quality_report['value_ranges'][column] = {
                        'min': col_min,
                        'max': col_max,
                        'expected_min': min_val,
                        'expected_max': max_val
                    }

                    if col_min < min_val or col_max > max_val:
                        quality_report['issues'].append(
                            f"Column {column} outside expected range "
                            f"[{min_val}, {max_val}]: [{col_min}, {col_max}]"
                        )

        logger.info(
            f"📊 Data quality check: {len(df)} rows, {len(quality_report['issues'])} issues")
        return quality_report

    @staticmethod
    def backup_file(filepath: str, backup_dir: str = 'backups') -> str:
        """
        Create a backup of a file.

        Args:
            filepath: Path to file to backup
            backup_dir: Directory to store backups

        Returns:
            Path to backup file
        """
        import shutil
        from datetime import datetime

        os.makedirs(backup_dir, exist_ok=True)

        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f"{timestamp}_{filename}")

        try:
            shutil.copy2(filepath, backup_path)
            logger.info(f"💾 Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"❌ Failed to create backup: {str(e)}")
            return None
