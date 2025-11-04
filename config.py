# Configuration file for Gesture Detection Project

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_INDEX = 0

# MediaPipe settings
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Pose matching settings
SIMILARITY_THRESHOLD = 0.85  # Threshold untuk menganggap pose cocok (0-1)
MATCH_DISPLAY_TIME = 3  # Waktu display hasil match (detik)

# Colors (BGR format)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Text settings
FONT = None  # Will use cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2

# Paths
REFERENCE_IMAGES_PATH = "reference_images"
OUTPUT_PATH = "output"
