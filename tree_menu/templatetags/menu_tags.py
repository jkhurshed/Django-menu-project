from django import template
from django.urls import resolve, Resolver404
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    
    try:
        current_url_name = resolve(current_path).url_name
    except Resolver404:
        current_url_name = None

    # Get all menu items for the specified menu in a single query
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    
    # Convert queryset to dictionary for O(1) lookups
    items_dict = {item.id: item for item in menu_items}
    
    # Create tree structure and find active items
    root_items = []
    active_branch = set()
    
    # First pass: build the tree and find the active item
    for item in menu_items:
        # Set parent-child relationships
        if item.parent_id:
            parent = items_dict.get(item.parent_id)
            if not hasattr(parent, 'children'):
                parent.children = []
            parent.children.append(item)
        else:
            root_items.append(item)
            
        # Check if this item is active
        if (item.url and item.url == current_path) or \
           (item.named_url and item.named_url == current_url_name):
            # Mark all parents as active
            active_item = item
            while active_item:
                active_branch.add(active_item.id)
                active_item = items_dict.get(active_item.parent_id)

    # Sort all children lists
    for item in menu_items:
        if hasattr(item, 'children'):
            item.children.sort(key=lambda x: x.order)

    return {
        'menu_items': root_items,
        'active_branch': active_branch,
    }
