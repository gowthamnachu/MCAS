"""
Shared utilities for Blink-PIN registration and authentication.

This module centralizes constants, MediaPipe setup, EAR computation,
landmark helpers, and simple user storage helpers.
"""

from __future__ import annotations

import os
import json
import time
import hashlib
from typing import List, Dict, Any

import numpy as np

# Reduce TensorFlow/Mediapipe verbose logging (INFO/WARN)
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import mediapipe as mp

# -------------------
# CONSTANTS (keep in sync across scripts)
# -------------------

# Standard EAR threshold for blink detection
EAR_THRESHOLD: float = 0.25

# Quick vs Long blink threshold (seconds)
BLINK_DURATION_THRESHOLD: float = 0.4

# Minimum interval between two blinks (seconds)
MIN_BLINK_INTERVAL: float = 0.5

# Consecutive frames required to confirm a blink
CONSEC_FRAMES: int = 3

# PIN length (number of blinks)
MAX_BLINKS: int = 4

# Mapping from blink type to digit
BLINK_TO_DIGIT = {
    "quick": "0",
    "long": "1",
}

# MediaPipe face mesh helpers
mp_face_mesh = mp.solutions.face_mesh

# Eye landmark indices (MediaPipe Face Mesh)
# Left eye: outer corner, top, top, inner corner, bottom, bottom
LEFT_EYE_LANDMARKS = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_LANDMARKS = [362, 385, 387, 263, 373, 380]


# -------------------
# MATH / VISION HELPERS
# -------------------

def hash_pin(pin: str) -> str:
    """Hash PIN using SHA-256"""
    return hashlib.sha256(pin.encode()).hexdigest()


def calculate_ear(eye_points: List[List[float]]) -> float:
    """
    Calculate Eye Aspect Ratio using the standard formula.
    eye_points should be 6 landmarks in this order:
    [0] = outer corner
    [1] = top point 1
    [2] = top point 2
    [3] = inner corner
    [4] = bottom point 1
    [5] = bottom point 2
    """
    points = np.array(eye_points, dtype=np.float32)

    A = np.linalg.norm(points[1] - points[5])  # Vertical distance 1
    B = np.linalg.norm(points[2] - points[4])  # Vertical distance 2
    C = np.linalg.norm(points[0] - points[3])  # Horizontal distance

    if C == 0:
        return 0.0
    return float((A + B) / (2.0 * C))


def get_landmark_coords(landmarks, indices: List[int], width: int, height: int) -> List[List[int]]:
    """Extract landmark coordinates and convert to pixel positions."""
    coords: List[List[int]] = []
    for idx in indices:
        lm = landmarks.landmark[idx]
        x = int(lm.x * width)
        y = int(lm.y * height)
        coords.append([x, y])
    return coords


def create_face_mesh():
    """Create a configured MediaPipe FaceMesh instance."""
    return mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )


# -------------------
# USER STORE HELPERS
# -------------------

def users_store_path() -> str:
    """Return the absolute path to the users.json in the current directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "users.json")


def load_users() -> Dict[str, Any]:
    """Load users database from JSON, returning a dict with a 'users' key."""
    path = users_store_path()
    if not os.path.exists(path):
        return {"users": {}}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "users" not in data:
            return {"users": {}}
        if not isinstance(data["users"], dict):
            data["users"] = {}
        return data
    except Exception:
        # Corrupt file fallback
        return {"users": {}}


def save_users(data: Dict[str, Any]) -> None:
    """Persist users database to JSON."""
    path = users_store_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_user_pin(username: str, pin_plain: str) -> None:
    """Set or update the user's PIN hash and metadata."""
    db = load_users()
    db.setdefault("users", {})
    db["users"][username] = {
        "pin_hash": hash_pin(pin_plain),
        "pin_length": len(pin_plain),
        "updated_at": time.time(),
    }
    save_users(db)


def get_user_pin_hash(username: str) -> str | None:
    """Return stored PIN hash for the username, if present."""
    db = load_users()
    user = db.get("users", {}).get(username)
    if not user:
        return None
    return user.get("pin_hash")


def get_user_pin_length(username: str, default_length: int = MAX_BLINKS) -> int:
    db = load_users()
    user = db.get("users", {}).get(username)
    if not user:
        return default_length
    return int(user.get("pin_length", default_length))
