"""
Download necessary files from Supabase for regional analysis
NO BLUFFING - Only downloads what actually exists
"""
import os
import sys
from supabase import create_client

# Add parent directory to path to import from data/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Get credentials from environment (should be set in system)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "ml-files"

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing Supabase credentials")
    print("   Set them as environment variables:")
    print("   export SUPABASE_URL='your-url'")
    print("   export SUPABASE_KEY='your-key'")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🔍 Checking what files actually exist in Supabase...")
print("="*60)

try:
    # List all files in bucket
    files = supabase.storage.from_(BUCKET_NAME).list()
    
    print(f"\n📁 Files found in '{BUCKET_NAME}' bucket:")
    for file in files:
        print(f"   • {file['name']:<30} ({file.get('metadata', {}).get('size', 'unknown')} bytes)")
    
    print("\n" + "="*60)
    
    # Files we need
    required_files = {
        'encoded_districts.csv': 'Training data with all features',
        'label_encoder.pkl': 'District encoder',
        'trained_model.pkl': 'Trained Random Forest model (if exists)',
        'random_forest_model.pkl': 'Alternative model name (if exists)',
    }
    
    print("\n✅ Downloading required files...\n")
    
    os.makedirs('analysis/data', exist_ok=True)
    
    downloaded = []
    missing = []
    
    for filename, description in required_files.items():
        if any(f['name'] == filename for f in files):
            try:
                file_bytes = supabase.storage.from_(BUCKET_NAME).download(filename)
                
                output_path = f'analysis/data/{filename}'
                with open(output_path, 'wb') as f:
                    f.write(file_bytes)
                
                print(f"✅ {filename:<30} - {description}")
                downloaded.append(filename)
            except Exception as e:
                print(f"❌ {filename:<30} - Failed: {e}")
                missing.append(filename)
        else:
            print(f"⚠️  {filename:<30} - Not found in bucket")
            missing.append(filename)
    
    print("\n" + "="*60)
    print(f"\n📊 Summary:")
    print(f"   Downloaded: {len(downloaded)} files")
    print(f"   Missing: {len(missing)} files")
    
    if 'encoded_districts.csv' in downloaded:
        print("\n✅ GOOD NEWS: We have the training data!")
        print("   We can proceed with regional analysis.")
    else:
        print("\n❌ BAD NEWS: Missing critical training data")
        print("   Cannot proceed without encoded_districts.csv")
    
    if not any('model' in f for f in downloaded):
        print("\n⚠️  NO MODEL FOUND - We'll need to re-train (takes ~2 min)")
    else:
        print("\n✅ Model found! We can use existing model.")
        
except Exception as e:
    print(f"\n❌ Error accessing Supabase: {e}")
    print("   Check your .env credentials")

print("\n" + "="*60)
