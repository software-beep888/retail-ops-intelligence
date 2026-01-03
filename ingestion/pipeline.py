"""
Simple data pipeline demonstrating fail-fast validation.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
import shutil
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_promotions(df: pd.DataFrame) -> tuple[bool, list]:
    """Validate promotions data - FAIL FAST on schema drift."""
    errors = []

    # CRITICAL: Check for required column
    if 'discount_pct' not in df.columns:
        error_msg = "SCHEMA DRIFT: Expected 'discount_pct' column not found"
        errors.append(error_msg)
        logger.error(error_msg)

    # Additional validations
    if 'discount_pct' in df.columns:
        try:
            # Convert to numeric
            df['discount_pct'] = pd.to_numeric(
                df['discount_pct'], errors='coerce')

            # Check range
            invalid_discounts = df[~df['discount_pct'].between(0, 1)]
            if len(invalid_discounts) > 0:
                errors.append(
                    f"Found {len(invalid_discounts)} invalid discount values (not between 0-1)")
        except Exception as e:
            errors.append(f"Could not validate discount_pct: {str(e)}")

    return len(errors) == 0, errors


def validate_sales(df: pd.DataFrame) -> tuple[bool, list]:
    """Validate sales data."""
    errors = []

    if 'total_sales' in df.columns:
        # Check for negative sales
        negative_sales = df[df['total_sales'] < 0]
        if len(negative_sales) > 0:
            errors.append(
                f"Found {len(negative_sales)} records with negative sales")

    if 'transaction_count' in df.columns:
        # Check for negative transaction counts
        negative_transactions = df[df['transaction_count'] < 0]
        if len(negative_transactions) > 0:
            errors.append(
                f"Found {len(negative_transactions)} records with negative transaction count")

    return len(errors) == 0, errors


def quarantine_file(filepath: str, errors: list) -> str:
    """Move problematic file to quarantine."""
    try:
        quarantine_dir = 'data/quarantine'
        os.makedirs(quarantine_dir, exist_ok=True)

        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        quarantine_path = os.path.join(
            quarantine_dir, f"{timestamp}_{filename}")

        shutil.move(filepath, quarantine_path)

        # Save error log
        error_log = quarantine_path + '.errors.json'
        with open(error_log, 'w') as f:
            json.dump({
                'original_path': filepath,
                'quarantine_path': quarantine_path,
                'timestamp': datetime.now().isoformat(),
                'errors': errors
            }, f, indent=2)

        logger.warning(f"File quarantined: {filepath} -> {quarantine_path}")
        return quarantine_path

    except Exception as e:
        logger.error(f"Failed to quarantine {filepath}: {str(e)}")
        return filepath


def process_file(filepath: str, data_type: str) -> dict:
    """Process a single data file."""
    logger.info(f"Processing {filepath}")

    try:
        # Load data
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} records from {filepath}")

        # Validate based on data type
        if data_type == 'promotions':
            is_valid, errors = validate_promotions(df)
        elif data_type == 'sales':
            is_valid, errors = validate_sales(df)
        else:
            is_valid, errors = True, []

        if not is_valid:
            logger.error(f"Validation failed: {errors}")
            quarantine_path = quarantine_file(filepath, errors)
            return {
                'status': 'failed',
                'reason': 'validation_failed',
                'errors': errors,
                'quarantine_path': quarantine_path
            }

        # Add metadata
        df['_ingested_at'] = datetime.now().isoformat()
        df['_batch_id'] = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save validated version
        validated_path = filepath.replace('.csv', '_validated.csv')
        df.to_csv(validated_path, index=False)

        logger.info(f"Successfully processed {filepath}")
        return {
            'status': 'success',
            'records': len(df),
            'validated_path': validated_path
        }

    except Exception as e:
        logger.error(f"Failed to process {filepath}: {str(e)}")
        quarantine_path = quarantine_file(filepath, [str(e)])
        return {
            'status': 'error',
            'reason': str(e),
            'quarantine_path': quarantine_path
        }


def run_pipeline(data_dir: str = './data'):
    """Run the complete data pipeline."""
    start_time = datetime.now()
    logger.info("Starting data pipeline")

    # Files to process
    files_to_process = [
        ('stores.csv', 'stores'),
        ('daily_sales.csv', 'sales'),
        ('inventory_snapshots.csv', 'inventory'),
        ('promotions.csv', 'promotions')
    ]

    results = {}
    total_records = 0

    for filename, data_type in files_to_process:
        filepath = os.path.join(data_dir, filename)

        if os.path.exists(filepath):
            result = process_file(filepath, data_type)
            results[filename] = result

            if result['status'] == 'success':
                total_records += result['records']
        else:
            logger.warning(f"File not found: {filepath}")
            results[filename] = {
                'status': 'skipped',
                'reason': 'file_not_found'
            }

    # Calculate duration
    duration = (datetime.now() - start_time).total_seconds()

    # Create summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'duration_seconds': duration,
        'files_processed': len([r for r in results.values() if r['status'] == 'success']),
        'records_processed': total_records,
        'results': results
    }

    # Save summary
    os.makedirs('logs', exist_ok=True)
    with open('logs/pipeline_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "="*50)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*50)
    print(f"Duration: {duration:.1f} seconds")
    print(f"Files successfully processed: {summary['files_processed']}")
    print(f"Total records: {total_records:,}")

    failures = [(f, r.get('reason', 'unknown'))
                for f, r in results.items() if r['status'] != 'success']

    if failures:
        print(f"\n⚠️  Issues detected: {len(failures)}")
        for file, reason in failures:
            print(f"  • {file}: {reason}")
    else:
        print("\n✅ All files processed successfully")

    print(f"\nDetailed logs available in logs directory")
    print(f"Pipeline summary: logs/pipeline_summary.json")

    return summary


if __name__ == "__main__":
    run_pipeline()
