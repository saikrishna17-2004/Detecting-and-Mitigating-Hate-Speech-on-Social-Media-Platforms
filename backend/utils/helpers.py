"""
Utility functions for the hate speech detection system
"""

def format_timestamp(timestamp):
    """Format timestamp for display"""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def calculate_severity(confidence_score):
    """Calculate severity level based on confidence score"""
    if confidence_score >= 0.8:
        return "High"
    elif confidence_score >= 0.5:
        return "Medium"
    else:
        return "Low"

def get_category_color(category):
    """Get color code for violation category"""
    colors = {
        'racial': '#ff0000',
        'gender': '#ff6600',
        'religious': '#ff9900',
        'homophobic': '#ffcc00',
        'general': '#999999'
    }
    return colors.get(category, '#cccccc')
