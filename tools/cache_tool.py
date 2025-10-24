import os
import json
from datetime import datetime

class CacheTool:
    """Tool for managing cached docking results and user interactions"""
    
    def __init__(self, cache_file="data/docking_scores.json"):
        self.cache_file = cache_file
        self._ensure_cache_directory()
    
    def _ensure_cache_directory(self):
        """Ensure cache directory exists"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
    
    def get_cached_results(self, molecules, target):
        """Get cached docking results for specific molecules and target"""
        cache = self._load_cache()
        target_key = target or "default"
        
        if target_key not in cache:
            return {}
        
        return {mol: cache[target_key].get(mol) for mol in molecules 
               if mol in cache[target_key]}
    
    def save_results(self, molecules, target, results):
        """Save docking results to cache"""
        cache = self._load_cache()
        target_key = target or "default"
        
        if target_key not in cache:
            cache[target_key] = {}
        
        # Add timestamp and metadata
        for mol, score in results.items():
            cache[target_key][mol] = {
                "score": score,
                "timestamp": datetime.now().isoformat(),
                "computed": True
            }
        
        self._save_cache(cache)
    
    def get_cache_stats(self):
        """Get statistics about cached data"""
        cache = self._load_cache()
        
        total_targets = len(cache)
        total_molecules = sum(len(target_data) for target_data in cache.values())
        
        # Count by target
        target_counts = {target: len(molecules) for target, molecules in cache.items()}
        
        return {
            "total_targets": total_targets,
            "total_molecules": total_molecules,
            "target_counts": target_counts,
            "cache_file": self.cache_file
        }
    
    def clear_cache(self, target=None):
        """Clear cache for specific target or all cache"""
        if target:
            cache = self._load_cache()
            if target in cache:
                del cache[target]
                self._save_cache(cache)
                print(f"Cleared cache for target: {target}")
        else:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                print("Cleared entire cache")
    
    def get_cache_hit_rate(self, molecules, target):
        """Calculate cache hit rate for a set of molecules"""
        cached = self.get_cached_results(molecules, target)
        return len(cached) / len(molecules) if molecules else 0.0
    
    def _load_cache(self):
        """Load cache from file"""
        if not os.path.exists(self.cache_file):
            return {}
        
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
            return {}
    
    def _save_cache(self, cache):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

class MemoryTool:
    """Tool for managing conversation memory and context"""
    
    def __init__(self, memory_file="data/memory.json"):
        self.memory_file = memory_file
        self._ensure_memory_directory()
    
    def _ensure_memory_directory(self):
        """Ensure memory directory exists"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
    
    def save_interaction(self, query, response, context):
        """Save user interaction to memory"""
        memory = self._load_memory()
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "context": context
        }
        
        memory["interactions"].append(interaction)
        
        # Keep only last 100 interactions to prevent memory from growing too large
        if len(memory["interactions"]) > 100:
            memory["interactions"] = memory["interactions"][-100:]
        
        self._save_memory(memory)
    
    def get_recent_interactions(self, limit=5):
        """Get recent user interactions"""
        memory = self._load_memory()
        return memory["interactions"][-limit:]
    
    def get_user_preferences(self):
        """Extract user preferences from interaction history"""
        memory = self._load_memory()
        preferences = {
            "frequent_targets": {},
            "common_operations": {},
            "preferred_output_format": "detailed"
        }
        
        # Analyze recent interactions
        for interaction in memory["interactions"][-20:]:  # Last 20 interactions
            context = interaction.get("context", {})
            
            # Track frequent targets
            target = context.get("target")
            if target:
                preferences["frequent_targets"][target] = preferences["frequent_targets"].get(target, 0) + 1
            
            # Track common operations
            operation = context.get("operation")
            if operation:
                preferences["common_operations"][operation] = preferences["common_operations"].get(operation, 0) + 1
        
        return preferences
    
    def find_similar_queries(self, query):
        """Find similar queries from memory"""
        memory = self._load_memory()
        similar = []
        
        query_words = set(query.lower().split())
        
        for interaction in memory["interactions"]:
            interaction_query = interaction["query"].lower()
            interaction_words = set(interaction_query.split())
            
            # Simple similarity based on word overlap
            overlap = len(query_words.intersection(interaction_words))
            if overlap > 2:  # At least 3 words in common
                similar.append({
                    "query": interaction["query"],
                    "response": interaction["response"],
                    "similarity": overlap,
                    "timestamp": interaction["timestamp"]
                })
        
        # Sort by similarity and return top 3
        similar.sort(key=lambda x: x["similarity"], reverse=True)
        return similar[:3]
    
    def _load_memory(self):
        """Load memory from file"""
        if not os.path.exists(self.memory_file):
            return {"interactions": []}
        
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading memory: {e}")
            return {"interactions": []}
    
    def _save_memory(self, memory):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(memory, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
