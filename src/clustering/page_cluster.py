import numpy as np
import hdbscan
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class PageClusterer:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2", 
                 min_cluster_size=3, min_samples=1):
        """
        Initialize clusterer with medical text optimization
        Args:
            model_name: Sentence Transformer model
            min_cluster_size: Minimum pages per cluster (HDBSCAN param)
            min_samples: Core samples needed (HDBSCAN param)
        """
        self.model = SentenceTransformer(model_name)
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples

    def embed_pages(self, pages):
        """Generate embeddings with progress tracking"""
        return self.model.encode(pages, show_progress_bar=True)

    def cluster_pages(self, pages):
        """
        Full clustering pipeline with medical context labeling
        Returns:
            dict: {'cluster': labels, 'labels': cluster_names}
        """
        embeddings = self.embed_pages(pages)
        
        # HDBSCAN for density-based clustering
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
            metric='euclidean',
            cluster_selection_method='leaf'
        )
        cluster_labels = clusterer.fit_predict(embeddings)
        
        # Generate human-readable labels
        cluster_names = self._generate_cluster_labels(pages, cluster_labels)
        
        return {
            'cluster': cluster_labels.tolist(),
            'labels': cluster_names
        }

    def _generate_cluster_labels(self, pages, cluster_labels):
        """Auto-label clusters based on medical keywords"""
        labels = {}
        unique_clusters = set(cluster_labels)
        
        # Medical context patterns
        label_rules = [
            (['lab', 'result', 'test'], 'Lab Reports'),
            (['medication', 'prescription', 'dose'], 'Prescriptions'),
            (['diagnosis', 'assessment'], 'Clinical Diagnosis'),
            (['procedure', 'operation'], 'Medical Procedures'),
            (['history', 'background'], 'Patient History')
        ]
        
        for cluster_id in unique_clusters:
            if cluster_id == -1:  # Skip noise
                continue
                
            cluster_texts = [pages[i] for i, cid in enumerate(cluster_labels) 
                           if cid == cluster_id]
            
            # Find matching label
            label = 'General Notes'
            for keywords, potential_label in label_rules:
                if any(any(kw in text.lower() for kw in keywords) 
                     for text in cluster_texts):
                    label = potential_label
                    break
                    
            labels[cluster_id] = label
            
        return labels

    def get_cluster_contents(self, pages, cluster_data):
        """Organize pages by their clusters"""
        clusters = {}
        for idx, (page, cluster_id) in enumerate(zip(pages, cluster_data['cluster'])):
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    'label': cluster_data['labels'].get(cluster_id, 'Uncategorized'),
                    'pages': []
                }
            clusters[cluster_id]['pages'].append({
                'page_number': idx + 1,
                'content': page
            })
        return clusters

def save_clusters_to_file(clusters, output_path):
    """Save clustered content with labels"""
    with open(output_path, 'w') as f:
        for cluster_id, data in clusters.items():
            f.write(f"=== Cluster {cluster_id} ({data['label']}) ===\n")
            for page in data['pages']:
                f.write(f"\nPage {page['page_number']}:\n{page['content']}\n")
            f.write("\n" + "="*40 + "\n")
