"""
Obfuscated GCPService Loader
Loads the hidden compiled version from pickle file.
Code and prompts are protected in binary format.
"""
import pickle
from pathlib import Path

def _load_obfuscated_service():
    """Load GCPService from pickled obfuscated file."""
    pkl_path = Path(__file__).parent / "secure" / "gcp_service.pkl"
    
    if not pkl_path.exists():
        raise RuntimeError(
            f"Secure service not found: {pkl_path}\n"
            "API code is obfuscated and deployed securely."
        )
    
    with open(pkl_path, 'rb') as f:
        ServiceClass = pickle.load(f)
    
    return ServiceClass

# Load the hidden service class
GCPService = _load_obfuscated_service()
