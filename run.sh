#!/bin/bash
set -e

echo "🚀 Retail Ops Intelligence - Setup"
echo "=================================="

mkdir -p data logs

echo "📊 Generating sample data..."
python3 -c "
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate simple stores
stores = pd.DataFrame({
    'store_id': range(1, 151),
    'store_name': [f'Store_{i:03d}' for i in range(1, 151)],
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], 150)
})
stores.to_csv('data/stores.csv', index=False)

print('✅ Generated 150 stores')
"

echo "🐳 Starting services..."
docker-compose up -d

echo "⏳ Waiting for PostgreSQL..."
sleep 10

echo "✅ Setup complete!"
echo ""
echo "📊 Dashboard: http://localhost:8501"
echo "🗄️  PostgreSQL: localhost:5432 (retail_user/retail_password)"
echo ""
echo "🔧 To stop: docker-compose down"