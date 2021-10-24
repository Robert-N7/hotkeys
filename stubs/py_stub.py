from hotkeys import send
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

    def after_function_paste(self, name, params, retrn, indent, privacy, return_type, flags):
        if retrn:
            self.editor.move_up(2)
            self.editor.move_end_of_line()
        else:
            self.editor.select_todo_line(1)

    def _gen_class_stub(self, name, base, interfaces, indent, privacy, flags):
        base = '' if not base else f'({base})'
        last = f'{indent}    pass    # todo Ponder and deliberate before you make a move. \n'
        return f'class {name}{base}:\n{last}'

    def after_class_paste(self, name, base, interfaces, indent, privacy, flags):
        self.editor.select_todo_line()

