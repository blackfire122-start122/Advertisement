from django import template


register = template.Library()


@register.filter
def show_category_parents(cat):
	res = cat.category
	while cat.parent:
		cat = cat.parent
		res = cat.category+'/'+res
	return res

