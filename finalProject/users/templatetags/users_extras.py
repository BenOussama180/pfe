from django import template

# modifying a pre-existing template tag so we can conserve the query(link) of the filter when paginating ( refreshing page)
register = template.Library()

@register.simple_tag
def my_url(value, field_name, urlencode=None):
    
    url='?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        #join is a method that seprates the itrerable (url in this case ) by the string giving ( '&' in this case)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url
