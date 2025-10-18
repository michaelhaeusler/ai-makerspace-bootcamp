#!/usr/bin/env python3
"""
Debug script to investigate why search isn't finding results.
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.core.config import settings
from app.services.pdf_processor import PDFProcessor
from app.services.vector_store import VectorStore

def debug_search():
    print("🔍 Debugging Search Issues...")
    print("=" * 50)
    
    # Initialize services
    pdf_processor = PDFProcessor(settings.pdf_processing)
    vector_store = VectorStore(settings.vector_store)
    
    policy_id = "debug_policy_123"
    pdf_path = "data/sample_policy.pdf"
    
    print(f"1️⃣ Processing PDF: {pdf_path}")
    try:
        result = pdf_processor.process_pdf(pdf_path, "sample_policy.pdf")
        print(f"   ✅ PDF processed: {result['total_chunks']} chunks")
        
        # Show first few chunks to see what we're working with
        print(f"\n📄 First 3 chunks preview:")
        for i, chunk in enumerate(result['chunks'][:3]):
            print(f"   Chunk {i}: {chunk['text'][:100]}...")
            
    except Exception as e:
        print(f"   ❌ Error processing PDF: {e}")
        return
    
    print(f"\n2️⃣ Storing in Qdrant...")
    try:
        storage_result = vector_store.store_chunks(policy_id, result['chunks'])
        print(f"   ✅ Stored {storage_result['points_stored']} chunks")
    except Exception as e:
        print(f"   ❌ Error storing: {e}")
        return
    
    print(f"\n3️⃣ Testing search with different thresholds...")
    
    # Test with different similarity thresholds
    thresholds = [0.3, 0.5, 0.7, 0.9]
    test_query = "Wartezeiten"
    
    for threshold in thresholds:
        print(f"\n   🔍 Testing threshold: {threshold}")
        try:
            # Temporarily override the threshold
            original_threshold = settings.vector_store.similarity_threshold
            settings.vector_store.similarity_threshold = threshold
            
            results = vector_store.search_similar_chunks(policy_id, test_query, limit=5)
            print(f"      Found {len(results)} results")
            
            if results:
                for i, result in enumerate(results[:2]):  # Show top 2
                    print(f"      Result {i+1}: score={result['score']:.3f}")
                    print(f"         Text: {result['text'][:100]}...")
            
            # Restore original threshold
            settings.vector_store.similarity_threshold = original_threshold
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    print(f"\n4️⃣ Testing different query formats...")
    test_queries = [
        "Wartezeiten",
        "Wartezeit", 
        "waiting period",
        "Selbstbeteiligung",
        "Selbstbehalt",
        "deductible",
        "Ausschlüsse",
        "exclusions"
    ]
    
    for query in test_queries:
        try:
            results = vector_store.search_similar_chunks(policy_id, query, limit=1)
            print(f"   '{query}': {len(results)} results")
            if results:
                print(f"      Best score: {results[0]['score']:.3f}")
        except Exception as e:
            print(f"   '{query}': Error - {e}")
    
    print(f"\n5️⃣ Checking what's actually in the collection...")
    try:
        collection_name = f"{settings.vector_store.collection_prefix}{policy_id}"
        if vector_store.qdrant_client.collection_exists(collection_name):
            info = vector_store.qdrant_client.get_collection(collection_name)
            print(f"   Collection info: {info}")
            
            # Get a few sample points
            points = vector_store.qdrant_client.scroll(
                collection_name=collection_name,
                limit=3
            )[0]
            print(f"   Sample points: {len(points)} found")
            for point in points:
                print(f"      Point ID: {point.id}")
                print(f"      Payload keys: {list(point.payload.keys())}")
                print(f"      Text preview: {point.payload.get('text', '')[:50]}...")
        else:
            print(f"   ❌ Collection {collection_name} doesn't exist")
    except Exception as e:
        print(f"   ❌ Error checking collection: {e}")
    
    # Cleanup
    print(f"\n6️⃣ Cleanup...")
    try:
        vector_store.delete_policy_collection(policy_id)
        print(f"   ✅ Cleaned up test policy")
    except Exception as e:
        print(f"   ❌ Error cleaning up: {e}")

if __name__ == "__main__":
    debug_search()
