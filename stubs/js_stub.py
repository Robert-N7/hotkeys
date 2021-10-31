from hotkeys import send
from stubs.stub import Stub
from stubs.transform_case import camel_case, kebab_case, pascal_case


class JsStub(Stub):
    ext = '.js'
    has_privacy = False
    has_return_type = False
    has_abstract_classes = False
    has_static_classes = False

    def class_case(self, text):
        return pascal_case(text)

    def file_case(self, text):
        return kebab_case(text)

    def function_case(self, text):
        return camel_case(text)

    def var_case(self, text):
        return camel_case(text)

    def _gen_function_stub(self, name, params, retrn, indent, privacy, return_type, flags):
        if flags & self.FL_ISMETHOD:
            head = ''
        else:
            head = 'function'
        params = ', '.join(params)
        head += f'{name}({params}) '
        last = ''
        if retrn:
            last += f'{indent}    return {retrn};\n'
        elif flags & self.FL_ABSTRACT:
            last += f'{indent}    throw new Error("Not implemented");\n'
        last += f'{indent}' + '}\n'
        return head + ' {\n' + f'{indent}    // todo\n' + last

    def _gen_class_stub(self, name, base, interfaces, indent, privacy, flags):
        base = ' extends ' + base if base else ''
        if flags & self.FL_CONSTRUCTOR:
            new_indent = indent + ' ' * 4
            last = new_indent + self._gen_function_stub('constructor', [], None, new_indent,
                                                        '', '', self.FL_ISMETHOD) + \
                   '}\n'
        else:
            last = indent + '    // todo\n' + \
                   '}\n'
        return f'{indent}class {name}{base} ' + '{\n' + last

    def _gen_print_stub(self):
        return 'console.log();'

    def _gen_this_stub(self):
        return 'this.'

    def _after_class_paste(self, name, base, interfaces, indent, privacy, flags):
        if flags & self.FL_CONSTRUCTOR:
            up_amount = 3
        else:
            up_amount = 2
        return self.editor.select_todo_line(up_amount)

    def _after_function_paste(self, name, params, retrn, indent, privacy, return_type, flags):
        up = 2 if not retrn else 3
        return self.editor.select_todo_line(up)

    def _after_print_paste(self):
        self.editor.left(2)

    def _gen_define_stub(self, var_name):
        if '.' in var_name:
            first = ''
        else:
            first = 'let '
        return f'{first}{var_name} = ;'

    def _after_define_paste(self, var_name):
        left = 1 if var_name else 4
        self.editor.left(left)

    def _gen_for_stub(self, iterator, items, max_i, indent):
        if max_i:
            body = indent + ' ' * 4 + f'const x = {items}[{iterator}];\n' + \
                   indent + ' ' * 4 + '// todo\n'
            return f'for (let {iterator} = 0; {iterator} < {max_i}; {iterator}++) ' + '{\n' + \
                   body + indent + '}\n'
        return f'{items}.forEach(function({iterator}, key))' + ' {\n' + \
               indent + ' ' * 4 + '// todo\n' + \
               indent + '});\n'

    def _after_for_paste(self, iterator, items, max_i, indent):
        self.editor.select_todo_line(2)

    def _gen_if_stub(self, if_text, elif_text, else_text, indent=''):
        ind = self.indent(indent)
        s = f'{indent}if({if_text}) ' + '{\n' + \
            ind + '// todo\n'
        if elif_text:
            s += indent + '} ' + f'else if({elif_text}) ' + '{\n' + \
                 ind + '// todo\n'
        if else_text:
            s += indent + '} else {\n' + \
                 ind + '// todo\n'
        s += f'{indent}' + '}\n'
        return s

    def _after_if_paste(self, if_text, elif_text, else_text, indent=''):
        up = 2
        if elif_text:
            up += 2
        if else_text:
            up += 2
        self.editor.select_todo_line(up)
