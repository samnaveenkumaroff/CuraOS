import sys
import os

# --- Ensure src is in the Python path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from clustering.page_cluster import PageClusterer, save_clusters_to_file

# --- Test Data ---
SAMPLE_PAGES = [
    # Cluster 0: COVID-19
    "Positive COVID-19 PCR test results confirmed",
    "CT scan reveals bilateral ground-glass opacities",
    "Patient reports anosmia and ageusia",
    
    # Cluster 1: Influenza
    "Rapid influenza test positive for type A",
    "Prescribed oseltamivir 75mg BID for 5 days",
    "Patient presents with high fever and myalgia",
    
    # Cluster 2: Vaccination
    "Administered Pfizer COVID-19 vaccine dose #2",
    "Documented influenza vaccination batch XG-2024",
    "Patient scheduled for tetanus booster next month"
]

OUTPUT_PATH = "/home/usersxm/Desktop/Sys/MRRM_Project/data/cleaned_output.txt"

# --- Tests ---
def test_basic_clustering():
    """Test clustering of distinct medical categories"""
    clusterer = PageClusterer(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        similarity_threshold=0.82
    )
    clusters = clusterer.group_pages_by_cluster(SAMPLE_PAGES)
    
    print("\n🔄 Cluster Distribution:")
    for cid, indices in clusters.items():
        print(f"  Cluster {cid}: {len(indices)} pages")
        print(f"    Sample content: {SAMPLE_PAGES[indices[0]][:50]}...")
    
    assert 2 <= len(clusters) <= 3, "Expected 2-3 distinct clusters"
    
    # Verify COVID cluster
    covid_terms = ["COVID", "PCR", "ground-glass"]
    assert any(all(any(term in SAMPLE_PAGES[i] for term in covid_terms) 
               for i in indices) for indices in clusters.values()), "COVID cluster missing"

def test_output_file():
    """Test file output with medical content"""
    clusterer = PageClusterer(similarity_threshold=0.8)
    clusters = clusterer.group_pages_by_cluster(SAMPLE_PAGES)
    
    # Clean previous test file
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)
    
    save_clusters_to_file(clusters, OUTPUT_PATH)
    
    assert os.path.exists(OUTPUT_PATH), "Output file not created"
    with open(OUTPUT_PATH, 'r') as f:
        content = f.read()
        assert "Cluster 0" in content and "Cluster 1" in content, "Missing cluster headers"

def main():
    print("🏥 Running Medical Document Cluster Tests...")
    try:
        print("\n=== Testing Basic Clustering ===")
        test_basic_clustering()
        
        print("\n=== Testing File Output ===")
        test_output_file()
        
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        if os.path.exists(OUTPUT_PATH):
            print("\nLast output file contents:")
            with open(OUTPUT_PATH, 'r') as f:
                print(f.read())

if __name__ == "__main__":
    main()
