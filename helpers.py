def bold_str(s):
    return f'**{s}**'


def modify_str(s, options={}):
    if not s:
        return ''

    modified_str = s
    if options:
        bold = options.get('bold', False)
        span = options.get('span')
        if bold:
            modified_str = bold_str(s)
        if span:
            position = span.get('position')
            value = span.get('value')
            modified_value = f'`({value})`'
            if position == 'end':
                modified_str = f'{modified_str} {modified_value}'
            else:
                modified_str = f'{modified_value} {modified_str}'
    return modified_str
