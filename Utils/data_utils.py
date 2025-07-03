import math

def replace_nan_with_none(obj):
    """
    Đệ quy chuyển tất cả giá trị float('nan') trong dict/list thành None.
    """
    if isinstance(obj, dict):
        return {k: replace_nan_with_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan_with_none(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    else:
        return obj 