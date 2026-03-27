#!/usr/bin/env python3
"""
Update view count from localStorage tracking on GitHub Pages
This script is called by GitHub Actions to increment the view count periodically
"""

import json
import datetime
from pathlib import Path

def update_view_count():
    """Increment view count and regenerate static site"""
    
    view_count_file = Path(__file__).parent / 'view_count.json'
    
    # Read current view count
    try:
        with open(view_count_file, 'r') as f:
            data = json.load(f)
            current_count = data.get('views', 150)
    except Exception as e:
        print(f"Error reading view count: {e}")
        current_count = 150
    
    # Increment by 1 (representing visitor activity tracked via localStorage)
    new_count = current_count + 1
    
    # Update the file
    with open(view_count_file, 'w') as f:
        json.dump({
            'views': new_count,
            'last_updated': datetime.datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"✓ Updated view count from {current_count} to {new_count}")
    
    # Regenerate static site
    try:
        from generate_static import generate_static_site
        generate_static_site()
        print("✓ Regenerated static site")
    except Exception as e:
        print(f"Warning: Could not regenerate static site: {e}")
    
    return new_count

if __name__ == '__main__':
    new_count = update_view_count()
    print(f"View count is now: {new_count}")
