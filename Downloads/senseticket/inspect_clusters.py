import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    from analysis import perform_clustering
    from app import app
    
    with app.app_context():
        print("Running clustering analysis...")
        result = perform_clustering()
        
        if result and result.get('status') == 'success':
            print("\nCluster Summary (Average values per feature):")
            summary = result['summary']
            feature_names = result['feature_names']
            
            with open('cluster_results.txt', 'w', encoding='utf-8') as f:
                f.write(f"{'Feature':<20} | {'Cluster 0 (Red)':<20} | {'Cluster 1 (Blue)':<20} | {'Cluster 2 (Yellow)':<20}\n")
                f.write("-" * 90 + "\n")
                
                for feature in feature_names:
                    c0 = summary.get(feature, {}).get(0, 0)
                    c1 = summary.get(feature, {}).get(1, 0)
                    c2 = summary.get(feature, {}).get(2, 0)
                    f.write(f"{feature:<20} | {c0:<20.2f} | {c1:<20.2f} | {c2:<20.2f}\n")
                    
                f.write("\nInterpretation:\n")
                for i, color in enumerate(['Red', 'Blue', 'Yellow']):
                    f.write(f"Cluster {i} ({color}):\n")
                    max_feat = max(feature_names, key=lambda f: summary.get(f, {}).get(i, 0))
                    max_val = summary.get(max_feat, {}).get(i, 0)
                    f.write(f"  - Highest feature: {max_feat} ({max_val:.2f})\n")
            print("Analysis written to cluster_results.txt")
        else:
            print("Clustering failed or not enough data.")
            if result:
                print(result)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
