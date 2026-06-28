from tree_sitter_language_pack import get_parser

def initialize_parser():
    global parser
    parser = get_parser('python')

def extract_node_text(node, field_name, default):
    field_node = node.child_by_field_name(field_name)
    return field_node.text.decode('utf-8') if field_node else default

def get_function_signature(function_node):
    function_name = extract_node_text(function_node, 'name', '<unknown>')
    parameters = extract_node_text(function_node, 'parameters', '()')

    return f'{function_name}{parameters}'

def get_function_body(function_node):
    return function_node.text.decode('utf-8')

def extract_functions(content):
    try:
        root_node = parse_file(content)
        functions = {}
               
        if root_node is not None:
            
            def traverse(node):
                if node.type == 'function_definition':
                    function_signature = get_function_signature(node)
                    function_body = get_function_body(node)
                    functions[function_signature] = function_body
                for child in node.children:
                    traverse(child)

            traverse(root_node)
        return functions
    
    except Exception as e:
        # print(f"Error processing: {e}")
        return functions

def parse_file(content): 
    root_node = None
    if content and len(content) != 0:
        tree = parser.parse(bytes(content, "utf8"))
        root_node = tree.root_node

    return root_node