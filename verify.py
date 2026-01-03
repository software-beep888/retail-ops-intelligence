print("✅ GitHub Repository Verification")
print("=" * 40)

import os
import subprocess

# Check git status
result = subprocess.run(["git", "status"], capture_output=True, text=True)
if "nothing to commit" in result.stdout:
    print("✅ Repository is clean")
else:
    print("⚠️  Uncommitted changes detected")

# Check remote
result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
if "origin" in result.stdout:
    print("✅ Remote configured")
    print(result.stdout)
else:
    print("❌ No remote configured")

# Check files
required_files = ["README.md", "run.py", "dashboard/app.py", "ingestion/pipeline.py"]
for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file} exists")
    else:
        print(f"❌ {file} missing")

print("\n🎯 Next: Share your GitHub link!")
