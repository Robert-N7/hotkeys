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

    def _gen_function_stub(self, name, params, retrn, indent, privacy, return_type, flags):
        params = ', '.join(params)
        head = f'function {name}({params}) '
        last = ''
        if retrn:
            last += f'{indent}    return {retrn}\n'
        last += f'{indent}' + '}\n'
        return head + ' {\n' + f'{indent}    // todo\n' + last

    def _gen_class_stub(self, name, base, interfaces, indent, privacy, flags):
        base = ' extends ' + base if base else ''
        return f'{indent}class {name}{base} ' + '{\n' + \
               indent + '    // todo Ponder and deliberate before you make a move.\n' + '}\n'

    def after_class_paste(self, name, base, interfaces, indent, privacy, flags):
        return self.editor.select_todo_line(2)

    def after_function_paste(self, name, params, retrn, indent, privacy, return_type, flags):
        up = 2 if not retrn else 3
        return self.editor.select_todo_line(up)
