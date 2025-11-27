import os

# Limit threads for shared hosting to avoid OpenBLAS errors
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from models.database import db_manager, Message, AIResponse, Action
from sqlalchemy import desc

def get_all_conversations_v2():
    """Retrieve all user messages from V2 database"""
    session = db_manager.get_session()
    try:
        messages = session.query(Message).filter(Message.is_bot == False).all()
        return [
            {
                'user_id': msg.author_id,
                'channel_id': msg.channel_id,
                'content': msg.content,
                'category': 'General', # V2 doesn't have category yet
                'timestamp': msg.timestamp
            }
            for msg in messages
        ]
    finally:
        session.close()

def get_all_actions_v2():
    """Retrieve all actions from V2 database"""
    session = db_manager.get_session()
    try:
        actions = session.query(Action).all()
        return [
            {
                'user_id': a.user_id,
                'action_type': a.action_type,
                'timestamp': a.timestamp
            }
            for a in actions
        ]
    finally:
        session.close()

def perform_clustering(n_clusters=3):
    conversations = get_all_conversations_v2()
    actions = get_all_actions_v2()
    
    if not conversations and not actions:
        return None

    # Process Conversations
    df_conv = pd.DataFrame(conversations)
    if not df_conv.empty:
        # Count categories per user
        user_conv_features = df_conv.pivot_table(
            index='user_id', 
            columns='category', 
            aggfunc='size', 
            fill_value=0
        )
    else:
        user_conv_features = pd.DataFrame()

    # Process Actions
    df_actions = pd.DataFrame(actions)
    if not df_actions.empty:
        # Count actions per user
        user_action_features = df_actions.groupby('user_id').size().to_frame(name='action_count')
    else:
        user_action_features = pd.DataFrame()

    # Combine Features
    features = user_conv_features.join(user_action_features, how='outer').fillna(0)
    
    if features.empty or len(features) < n_clusters:
        return {
            'status': 'not_enough_data',
            'message': f'Need at least {n_clusters} users to cluster.'
        }

    # Normalize features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    features['cluster'] = kmeans.fit_predict(scaled_features)
    
    # Prepare result for visualization
    result = features.reset_index().to_dict(orient='records')
    
    # Summarize clusters
    cluster_summary = features.groupby('cluster').mean().to_dict()
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_to_native(obj):
        if isinstance(obj, dict):
            return {k: convert_to_native(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_native(item) for item in obj]
        elif hasattr(obj, 'item'):  # numpy scalar
            return obj.item()
        return obj
    
    return {
        'status': 'success',
        'data': convert_to_native(result),
        'summary': convert_to_native(cluster_summary),
        'feature_names': features.columns.tolist()
    }

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

# Global Cache
_SMART_CACHE = {
    'matrix': None,
    'vectorizer': None,
    'conversations': [],
    'last_count': 0,
    'last_update': 0
}

# Global Cache for AI Responses
_RESPONSE_CACHE = {
    'matrix': None,
    'vectorizer': None,
    'pairs': [], # List of (request_content, response_content)
    'last_count': 0,
    'last_update': 0
}

def find_smart_context(query, limit=3, threshold=0.2):
    """
    Find most relevant past conversations using TF-IDF cosine similarity.
    """
    global _SMART_CACHE
    
    session = db_manager.get_session()
    try:
        current_count = session.query(Message).count()
    finally:
        session.close()
        
    time_since_update = time.time() - _SMART_CACHE['last_update']
    
    should_reload = (
        _SMART_CACHE['matrix'] is None or 
        (current_count > _SMART_CACHE['last_count'] and time_since_update > 30) or
        time_since_update > 300
    )
    
    if should_reload:
        # print(f"🔄 Reloading Smart Memory (Count: {current_count})")
        conversations = get_all_conversations_v2()
        
        valid_convs = [
            c for c in conversations 
            if c['content'] and len(c['content']) > 5 and not c['content'].startswith('!')
        ]
        
        if not valid_convs:
            return []
        
        corpus = [c['content'] for c in valid_convs]
        
        vectorizer = TfidfVectorizer(
            stop_words=None,
            min_df=1,
            ngram_range=(1, 3),
            max_features=20000,
            lowercase=True,
            analyzer='word',
            token_pattern=r'\b\w+\b'
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            
            _SMART_CACHE['matrix'] = tfidf_matrix
            _SMART_CACHE['vectorizer'] = vectorizer
            _SMART_CACHE['conversations'] = valid_convs
            _SMART_CACHE['last_count'] = current_count
            _SMART_CACHE['last_update'] = time.time()
            
        except Exception as e:
            print(f"Error training smart model: {e}")
            return []
    
    try:
        if _SMART_CACHE['matrix'] is None:
            return []
            
        vectorizer = _SMART_CACHE['vectorizer']
        tfidf_matrix = _SMART_CACHE['matrix']
        valid_convs = _SMART_CACHE['conversations']
        
        query_vec = vectorizer.transform([query])
        cosine_sim = cosine_similarity(query_vec, tfidf_matrix)
        sim_scores = cosine_sim.flatten()
        related_indices = sim_scores.argsort()[::-1]
        
        results = []
        seen_content = set()
        
        for idx in related_indices:
            score = sim_scores[idx]
            if score < threshold:
                break
                
            match = valid_convs[idx]
            if match['content'] not in seen_content:
                match['score'] = float(score)
                results.append(match)
                seen_content.add(match['content'])
                
            if len(results) >= limit:
                break
                
        return results
        
    except Exception as e:
        print(f"Error in smart context search: {e}")
        return []

def find_best_cached_response(query: str, threshold: float = 0.5) -> str:
    """
    Find the best matching response from past successful AI interactions.
    Used when the AI API is down.
    """
    global _RESPONSE_CACHE
    
    session = db_manager.get_session()
    try:
        current_count = session.query(AIResponse).count()
        
        time_since_update = time.time() - _RESPONSE_CACHE['last_update']
        should_reload = (
            _RESPONSE_CACHE['matrix'] is None or 
            (current_count > _RESPONSE_CACHE['last_count'] and time_since_update > 60)
        )
        
        if should_reload:
            # Fetch successful AI pairs
            # Join AIResponse with Message (request) and Message (response)
            ai_pairs = session.query(AIResponse).all()
            
            valid_pairs = []
            for pair in ai_pairs:
                if pair.request_message and pair.response_message:
                    valid_pairs.append({
                        'request': pair.request_message.content,
                        'response': pair.response_message.content
                    })
            
            if not valid_pairs:
                return None
                
            corpus = [p['request'] for p in valid_pairs]
            
            vectorizer = TfidfVectorizer(
                min_df=1,
                ngram_range=(1, 2),
                lowercase=True
            )
            
            tfidf_matrix = vectorizer.fit_transform(corpus)
            
            _RESPONSE_CACHE['matrix'] = tfidf_matrix
            _RESPONSE_CACHE['vectorizer'] = vectorizer
            _RESPONSE_CACHE['pairs'] = valid_pairs
            _RESPONSE_CACHE['last_count'] = current_count
            _RESPONSE_CACHE['last_update'] = time.time()
            
    except Exception as e:
        print(f"Error updating response cache: {e}")
        return None
    finally:
        session.close()
        
    # Search
    try:
        if _RESPONSE_CACHE['matrix'] is None:
            return None
            
        vectorizer = _RESPONSE_CACHE['vectorizer']
        tfidf_matrix = _RESPONSE_CACHE['matrix']
        pairs = _RESPONSE_CACHE['pairs']
        
        query_vec = vectorizer.transform([query])
        cosine_sim = cosine_similarity(query_vec, tfidf_matrix)
        
        # Get best match
        best_idx = cosine_sim.argmax()
        best_score = cosine_sim[0, best_idx]
        
        if best_score >= threshold:
            return pairs[best_idx]['response']
            
        return None
        
    except Exception as e:
        print(f"Error searching response cache: {e}")
        return None
