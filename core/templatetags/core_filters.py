from django import template

register = template.Library()


@register.filter
def bar_height(wpm):
    """Convert WPM to bar height percentage (max 250 WPM = 100%)."""
    try:
        return min(100, max(5, (float(wpm) / 250) * 100))
    except (ValueError, TypeError):
        return 5


@register.filter
def format_mmss(seconds):
    """Convert seconds to MM:SS format."""
    try:
        s = int(float(seconds))
        return f"{s // 60:02d}:{s % 60:02d}"
    except (ValueError, TypeError):
        return "00:00"


@register.filter
def div_safe(value, divisor):
    """Safe division, returns rounded int."""
    try:
        if int(divisor) == 0:
            return 0
        return round(int(value) / int(divisor))
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def pct_of(part, whole):
    """Calculate percentage of part in whole."""
    try:
        if int(whole) == 0:
            return 0
        return round((int(part) / int(whole)) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
