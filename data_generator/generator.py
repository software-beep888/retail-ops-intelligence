import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


class RetailDataGenerator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        self.STORE_COUNT = 150
        self.DAYS_HISTORY = 180

    def generate_stores(self):
        stores = []
        for i in range(self.STORE_COUNT):
            stores.append({
                'store_id': i + 1,
                'store_name': f'Store_{i+1:03d}',
                'region': np.random.choice(['North', 'South', 'East', 'West', 'Central']),
            })
        return pd.DataFrame(stores)

    def generate_daily_sales(self, stores_df):
        all_sales = []
        start_date = datetime.now() - timedelta(days=self.DAYS_HISTORY)

        for _, store in stores_df.iterrows():
            base_sales = np.random.lognormal(8, 0.5)

            for day_offset in range(self.DAYS_HISTORY):
                current_date = start_date + timedelta(days=day_offset)

                daily_sales = base_sales
                # Weekend effect
                if current_date.weekday() >= 5:
                    daily_sales *= 1.2

                # Random variation
                daily_sales *= np.random.normal(1.0, 0.1)
                daily_sales = max(0, daily_sales)

                all_sales.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'store_id': store['store_id'],
                    'total_sales': round(daily_sales, 2),
                    'transaction_count': int(daily_sales / 50),
                })

        return pd.DataFrame(all_sales)

    def generate_promotions(self):
        promotions = []

        # Old schema
        for i in range(50):
            promotions.append({
                'promotion_id': f'PROMO_OLD_{i:03d}',
                'store_id': np.random.randint(1, self.STORE_COUNT + 1),
                'start_date': (datetime.now() - timedelta(days=120 + i)).strftime('%Y-%m-%d'),
                'end_date': (datetime.now() - timedelta(days=120 + i + 7)).strftime('%Y-%m-%d'),
                'discount_pct': np.random.uniform(0.1, 0.4),
                'promotion_type': np.random.choice(['Clearance', 'Seasonal'])
            })

        # New schema (simulating drift)
        for i in range(30):
            promotions.append({
                'promotion_id': f'PROMO_NEW_{i:03d}',
                'store_id': np.random.randint(1, self.STORE_COUNT + 1),
                'start_date': (datetime.now() - timedelta(days=30 + i)).strftime('%Y-%m-%d'),
                'end_date': (datetime.now() - timedelta(days=30 + i + 7)).strftime('%Y-%m-%d'),
                # Different column name
                'discount_percent': np.random.uniform(0.1, 0.4),
                'promotion_type': np.random.choice(['Clearance', 'Seasonal'])
            })

        return pd.DataFrame(promotions)

    def save_to_csv(self, output_dir='./data'):
        import os
        os.makedirs(output_dir, exist_ok=True)

        stores = self.generate_stores()
        sales = self.generate_daily_sales(stores)
        promotions = self.generate_promotions()

        stores.to_csv(f'{output_dir}/stores.csv', index=False)
        sales.to_csv(f'{output_dir}/daily_sales.csv', index=False)
        promotions.to_csv(f'{output_dir}/promotions.csv', index=False)

        # Simple inventory flags
        inventory = pd.DataFrame({
            'date': [(datetime.now() - timedelta(days=d)).strftime('%Y-%m-%d')
                     for d in range(30)],
            'store_id': np.random.randint(1, 151, 4500),
            'stockout_flag': np.random.choice([True, False], 4500, p=[0.05, 0.95]),
            'low_stock_flag': np.random.choice([True, False], 4500, p=[0.1, 0.9])
        })
        inventory.to_csv(f'{output_dir}/inventory_snapshots.csv', index=False)

        print(f"✅ Generated {len(sales):,} sales records")
        return {'stores': stores, 'sales': sales, 'promotions': promotions}


if __name__ == "__main__":
    generator = RetailDataGenerator()
    generator.save_to_csv()
