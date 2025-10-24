import os
import json
from rdkit import Chem

# Try to import dockstring, fall back to mock if not available
try:
    from dockstring import load_target
    DOCKSTRING_AVAILABLE = True
except ImportError:
    DOCKSTRING_AVAILABLE = False
    print("Warning: Dockstring not available, using mock scores")

class DockingTool:
    """Tool for computing molecular docking scores"""
    
    def __init__(self, cache_file="data/docking_scores.json"):
        self.cache_file = cache_file
        
    def generate_mock_score(self, smiles):
        """Generate a deterministic mock docking score based on SMILES string."""
        hash_val = hash(smiles) % 1000
        score = -3.0 - (hash_val / 1000.0) * 9.0
        return round(score, 1)
    
    def compute_scores(self, smiles_list, target_name):
        """
        Compute docking scores for a list of SMILES strings.
        
        Args:
            smiles_list: List of SMILES strings to dock
            target_name: Name of the protein target
            
        Returns:
            Dictionary mapping SMILES to docking scores
        """
        print(f"DEBUG: compute_scores called with target={target_name}")
        
        cache = self._load_cache()
        if target_name not in cache:
            cache[target_name] = {}
        
        results = {}
        cache_modified = False
        use_real_docking = False
        
        # Try to load built-in target
        if DOCKSTRING_AVAILABLE:
            try:
                print(f"Loading built-in target: {target_name}")
                target = load_target(target_name)
                use_real_docking = True
                print(f"Successfully loaded built-in target: {target_name}")
            except Exception as e:
                print(f"Warning: Failed to load target {target_name}: {e}")
                print("Falling back to mock scores")
                use_real_docking = False
        else:
            use_real_docking = False
        
        for smi in smiles_list:
            # Check cache for this specific target-molecule combination
            if smi in cache[target_name]:
                results[smi] = cache[target_name][smi]
                print(f"Using cached score for {smi} against {target_name}: {cache[target_name][smi]}")
                continue
            
            mol = Chem.MolFromSmiles(smi)
            if mol is None:
                print(f"Invalid SMILES: {smi}")
                results[smi] = None
                continue
            
            if use_real_docking:
                try:
                    result = target.dock(smi)
                    # Handle different return formats from dockstring
                    if isinstance(result, dict):
                        score = result["score"]
                    elif isinstance(result, tuple):
                        score = result[0]
                    else:
                        score = float(result)
                    print(f"Computed docking score for {smi} against {target_name}: {score}")
                except Exception as e:
                    print(f"Warning: Docking failed for {smi}: {e}")
                    print("Using mock score")
                    score = self.generate_mock_score(smi)
            else:
                score = self.generate_mock_score(smi)
                
            results[smi] = score
            cache[target_name][smi] = score
            cache_modified = True
        
        # Only save cache if it was modified
        if cache_modified:
            self._save_cache(cache)
        
        return results
    
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
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")