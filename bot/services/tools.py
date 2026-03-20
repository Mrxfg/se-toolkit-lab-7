from services.api import get_items, get_scores

def get_items_tool():
    return get_items()

def get_pass_rates_tool(lab):
    return get_scores(lab)
