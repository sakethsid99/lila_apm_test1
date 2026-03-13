"""
Coordinate conversion module for LILA BLACK visualizations.
Converts 3D world coordinates to 2D minimap pixel coordinates.
"""

# Map configurations based on the README definitions
MAP_CONFIGS = {
    "AmbroseValley": {
        "scale": 900,
        "origin_x": -370,
        "origin_z": -473
    },
    "GrandRift": {
        "scale": 581,
        "origin_x": -290,
        "origin_z": -290
    },
    "Lockdown": {
        "scale": 1000,
        "origin_x": -500,
        "origin_z": -500
    }
}

def get_pixel_coords(x: float, z: float, map_id: str) -> tuple[float, float]:
    """
    Converts world coordinates (x, z) to minimap pixel coordinates (pixel_x, pixel_y).
    
    Args:
        x (float): World X coordinate
        z (float): World Z coordinate 
        map_id (str): The map identifier ("AmbroseValley", "GrandRift", "Lockdown")
        
    Returns:
        tuple: (pixel_x, pixel_y) on a 1024x1024 pixel minimap image
    """
    if map_id not in MAP_CONFIGS:
        raise ValueError(f"Unknown map_id: {map_id}. Must be one of {list(MAP_CONFIGS.keys())}")
        
    config = MAP_CONFIGS[map_id]
    scale = config["scale"]
    origin_x = config["origin_x"]
    origin_z = config["origin_z"]
    
    # Step 1: Convert world coords to UV (0-1 range)
    u = (x - origin_x) / scale
    v = (z - origin_z) / scale
    
    # Step 2: Convert UV to pixel coords (1024x1024 image)
    pixel_x = u * 1024
    pixel_y = (1 - v) * 1024  # Y is flipped (image origin is top-left)
    
    return pixel_x, pixel_y
