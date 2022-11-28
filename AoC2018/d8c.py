
with open('d8.txt') as f:
    datalines = [int(i) for i in f.read().strip().split()]

def recursive_fill(data):
    node = {
        'children': [],
        'value': 0
    }
    metadata_sum = 0
    node_metadata = 0
    num_children = data[0]
    num_metadata = data[1]
    total_size = 1 + 1 + num_metadata
    starting_offset = 2
    for i in range(num_children):
        size, curr_node, curr_meta = recursive_fill(data[starting_offset:])
        starting_offset += size
        total_size += size
        node_metadata += curr_meta
        node['children'].append(curr_node)
    for i in range(num_metadata):
        metadata_sum += data[starting_offset + i]
    if num_children == 0:
        node['value'] = metadata_sum
    else:
        for i in range(num_metadata):
            metadata_index = data[starting_offset + i] - 1
            if metadata_index < len(node['children']):
                node['value'] += node['children'][metadata_index]['value']
    return (total_size, node, metadata_sum+node_metadata)


root_node = recursive_fill(datalines)
print('Part 1:')
print(root_node[2])
print('Part 2:')
print(root_node[1]['value'])