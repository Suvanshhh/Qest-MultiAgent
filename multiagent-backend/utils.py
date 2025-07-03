from bson import ObjectId

def fix_mongo_ids(doc):
    """Convert all ObjectId fields in a dict or list of dicts to strings."""
    if isinstance(doc, list):
        return [fix_mongo_ids(d) for d in doc]
    if isinstance(doc, dict):
        return {k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()}
    return doc
