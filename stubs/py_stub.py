from hotkeys import send
from stubs.editors.pycharm import Pycharm
from stubs.stub import Stub
from stubs.transform_case import pascal_case, snake_case


class PyStub(Stub):
    ext = '.py'
    has_privacy = False
    has_return_type = False
    has_static_classes = False
    has_abstract_classes = False

    def file_case(self, text):
        return snake_case(text)

    def class_case(self, text):
        return pascal_case(text)

    def function_case(self, text):
        return snake_case(text)

    def var_case(self, text):
        return snake_case(text)

    def process_params(self, params, flags):
        if not flags & self.FL_STATIC and flags & self.FL_ISMETHOD:
            params.insert(0, 'self')
        return params

    def _gen_function_stub(self, name, params, retrn, indent, privacy, return_type, flags):
        param_s = ', '.join(params)
        if retrn:
            last = f'{indent}    # todo really cool stuff here\n' \
                   f'{indent}    return {retrn}\n'
        elif flags & self.FL_ABSTRACT:
            last = f'{indent}    raise NotImplementedError()\n'
        else:
            last = f'{indent}    pass     # todo amaze the world\n'
        static = f'@staticmethod\n{indent}' if flags & self.FL_STATIC else ''
        return f'{static}def {name}({param_s}):\n{last}'

    def _after_function_paste(self, name, params, retrn, indent, privacy, return_type, flags):
        if flags & self.FL_ABSTRACT:
            return
        if retrn:
            self.editor.up(2)
            self.editor.end()
        else:
            self.editor.select_todo_line(1)

    def _gen_class_stub(self, name, base, interfaces, indent, privacy, flags):
        base = '' if not base else f'({base})'
        if flags & self.FL_CONSTRUCTOR:
            f_indent = indent + ' ' * 4
            last = f_indent + self._gen_function_stub('__init__', [], '', f_indent, '', '', self.FL_ISMETHOD)
        else:
            last = f'{indent}    pass    # todo Ponder and deliberate before you make a move. \n'
        return f'class {name}{base}:\n{last}'

    def _after_class_paste(self, name, base, interfaces, indent, privacy, flags):
        self.editor.select_todo_line(1)

    def _gen_print_stub(self):
        return "print(f'')"

    def _after_print_paste(self):
        self.editor.left(2)

    def _gen_this_stub(self):
        return 'self.'

    def _gen_define_stub(self, var_name):
        return f'{var_name} = '

    def _after_define_paste(self, var_name):
        if not var_name:
            self.editor.left(3)

    def _gen_for_stub(self, iterator, items, max_i, indent):
        if max_i:
            return f'for {iterator} in range({max_i}):\n' + \
                   indent + ' ' * 4 + f'x = {items}[{iterator}]\n' + \
                   indent + ' ' * 4 + '# todo\n'
        return f'for {iterator} in {items}:\n' + \
               indent + ' ' * 4 + 'pass # todo\n'

    def _after_for_paste(self, iterator, items, max_i, indent):
        c = 2 if max_i else 1
        self.editor.select_todo_line(c)

    def _gen_if_stub(self, if_text, elif_text, else_text, indent=''):
        ind = self.indent(indent)
        s = f'{indent}if {if_text}:\n' \
            f'{ind}pass\n'
        if elif_text:
            s += f'elif {elif_text}:\n' \
                 f'{ind}pass\n'
        if else_text:
            s += f'else:\n' \
                 f'{ind}pass\n'
        return s

    def _after_if_paste(self, if_text, elif_text, else_text, indent=''):
        count = 1
        if elif_text:
            count += 2
        if else_text:
            count += 2
        self.editor.select_todo_line(count)
