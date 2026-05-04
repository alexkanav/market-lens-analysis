# --- Data processing ---
MIN_ROWS = 125
STEP = 5

# --- Trend detection ---
TIMEFRAMES_DAYS = (131, 65, 23)
PEAKS_MIN = 2
PEAKS_MAX = 10

# --- Plotting ---
X_INDEX_RANGE_START = 50
X_INDEX_RANGE_END = 300
CHART_DATE_LABEL_INTERVAL = 5

# --- Styling ---
LINE_STYLES = (
    ('red', 'solid', '6-Month Trend'),
    ('blue', 'solid', '3-Month Trend'),
    ('green', 'dotted', '1-Month Trend')
)
UP_COLOR = 'green'
DOWN_COLOR = 'red'

# --- Runtime ---
ENABLE_VISUALIZATION = True
