from django import template
from django.urls import resolve, Resolver404
from ..models import MenuItem

register = template.Library()

def draw_menu(context, menu_name):
    request = context.get('request')
    if not request:
        return {'menu_items': [], 'active_branch': set()}
        
    current_path = request.path
    
    try:
        current_url_name = resolve(current_path).url_name
    except Resolver404:
        current_url_name = None

    # Get all menu items for the specified menu in a single query
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent').order_by('order')
    
    # Create tree structure and find active items
    root_items = []
    active_branch = set()
    items_dict = {}
    
    # First, collect all items in a dictionary
    for item in menu_items:
        items_dict[item.id] = {
            'item': item,
            'children': []
        }

    # Second, build the tree structure
    for item in menu_items:
        if item.parent_id:
            if item.parent_id in items_dict:
                items_dict[item.parent_id]['children'].append(items_dict[item.id])
        else:
            root_items.append(items_dict[item.id])
            
        # Check if this item is active
        if (item.url and item.url == current_path) or \
           (item.named_url and item.named_url == current_url_name):
            # Mark all parents as active
            active_item = item
            while active_item:
                active_branch.add(active_item.id)
                active_item = active_item.parent

    return {
        'menu_items': root_items,
        'active_branch': active_branch,
    }

register.inclusion_tag('tree_menu/menu.html', takes_context=True)(draw_menu)
