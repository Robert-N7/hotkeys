import os

from hotkeys import send
from stubs.stub import Stub
from stubs.transform_case import pascal_case, snake_case, camel_case


class PhpStub(Stub):
    ext = '.php'
    has_privacy = True
    has_return_type = True
    has_static_classes = False

    def class_case(self, text):
        return pascal_case(text)

    def file_case(self, text):
        return pascal_case(text)

    def function_case(self, text):
        return camel_case(text)

    def _gen_function_stub(self, name, params, retrn, indent, privacy, return_type, flags):
        for i in range(len(params)):
            if not params[i].startswith('$'):
                x = params[i].split(' ', 1)
                if len(x) > 1:
                    if not x[1].startswith('$'):
                        params[i] = x[0] + ' $' + x[1]
                else:
                    params[i] = '$' + params[i]
        params = ', '.join(params)
        return_type = ': ' + return_type if return_type else ''
        retrn = indent + '    return ' + retrn + '\n' if retrn else ''
        privacy = privacy + ' ' if privacy else ''
        abstract = Stub.keyword(Stub.FL_ABSTRACT, True)
        static = Stub.keyword(Stub.FL_STATIC, True)
        head = f'{abstract}{privacy}{static}function {name}({params}){return_type}\n'
        if flags & Stub.FL_STUB:
            return head + ';'
        return head + \
               indent + '{\n' + \
               f'{indent}    // todo cool stuff here\n' + \
               f'{retrn}' + \
               indent + '}\n'

    def _gen_class_stub(self, name, base, interfaces, indent, privacy, flags):
        abstract = Stub.keyword(Stub.FL_ABSTRACT)
        base = ' extends ' + self.class_case(base) if base else ''
        interfaces = ' implements ' + ', '.join(interfaces) if interfaces else ''
        return f'{abstract}class {name}{base}{interfaces}\n' + \
               indent + '{\n' + \
               f'{indent}    // todo really cool things\n' + \
               indent + '}\n'

    def __get_namespace(self, directory):
        folders = []
        while directory != self.project_dir:
            directory, base = os.path.split(directory)
            folders.append(pascal_case(base))
        folders.reverse()
        return '\\'.join(folders)

    def _gen_file_stub(self, name, directory, class_info):
        return f'<?php\n\n' + \
               f'namespace {self.__get_namespace(directory)};\n\n\n'

    def _after_function_paste(self, name, params, retrn, indent, privacy, return_type, flags):
        up = 3 if retrn else 2
        self.editor.select_todo_line(up)

    def _after_class_paste(self, name, base, interfaces, indent, privacy, flags):
        self.editor.select_todo_line(2)

    def _gen_print_stub(self):
        return 'echo  . PHP_EOL;'

    def _after_print_paste(self):
        self.editor.left()
        self.editor.ctrl_left(2)
        self.editor.left()

    def _gen_this_stub(self):
        return 'this.'
