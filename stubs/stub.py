import os
from hotkeys import clip, send

from stubs.transform_case import pascal_case, snake_case


class Stub:
    # Flags
    FL_STATIC = 0x1
    FL_STUB = 0x2   # No function body
    FL_FINAL = 0x4
    FL_VIRTUAL = 0x8
    FL_OVERRIDE = 0x10
    FL_SEALED = 0x20
    FL_ASYNC = 0x40
    FL_DELEGATE = 0x80
    FL_UNSAFE = 0x100
    FL_ABSTRACT = 0x202
    FL_CONSTRUCTOR = 0x400
    FL_ISMETHOD = 0x800

    FL_KEYWORDS = {
        FL_STATIC: 'static',
        FL_STUB: 'stub',
        FL_FINAL: 'final',
        FL_VIRTUAL: 'virtual',
        FL_OVERRIDE: 'override',
        FL_SEALED: 'sealed',
        FL_ASYNC: 'async',
        FL_DELEGATE: 'delegate',
        FL_UNSAFE: 'unsafe',
        FL_ABSTRACT: 'abstract'
    }

    ext = '.py'
    default_privacy = None
    has_privacy = True
    has_return_type = True
    has_abstract_classes = True
    has_static_classes = True
    possible_flags = FL_STATIC | FL_ABSTRACT

    @staticmethod
    def keyword(flag, with_space=False):
        t = Stub.FL_KEYWORDS[flag]
        if with_space:
            t += ' '
        return t

    @staticmethod
    def indent(indent):
        return indent + ' ' * 4

    def class_case(self, text):
        raise NotImplementedError()

    def file_case(self, text):
        raise NotImplementedError()

    def function_case(self, text):
        raise NotImplementedError()

    def var_case(self, text):
        raise NotImplementedError()

    def __init__(self, editor, project_dir=''):
        self.project_dir = project_dir
        self.editor = editor

    def _gen_function_stub(self, name, params, retrn, indent, privacy, return_type, flags):
        raise NotImplementedError()

    def _gen_class_stub(self, name, base, interfaces, indent, privacy, flags):
        raise NotImplementedError()

    def _gen_file_stub(self, name, directory, class_info):
        return '\n' * 2

    def _gen_print_stub(self):
        raise NotImplementedError()

    def _gen_this_stub(self):
        raise NotImplementedError()

    def _gen_define_stub(self, var_name):
        raise NotImplementedError()

    def _gen_for_stub(self, iterator, items, max_i, indent):
        raise NotImplementedError()

    def _after_for_paste(self, iterator, items, max_i, indent):
        pass

    def _after_define_paste(self, var_name):
        pass

    def _after_function_paste(self, name, params, retrn, indent, privacy, return_type, flags):
        pass

    def _after_class_paste(self, name, base, interfaces, indent, privacy, flags):
        pass

    def _after_print_paste(self):
        pass

    def _after_file_create(self, name, directory, class_info):
        clip(os.path.join(directory, name))

    def __send_to_editor(self, s):
        clip(s)
        self.editor.paste()

    def create_function(self, name, params, retrn, indent=None, privacy=None, return_type=None, flags=0):
        if indent is None:
            indent = ' ' * 4 if flags & self.FL_ISMETHOD else ''
        name = self.function_case(name)
        self.__send_to_editor(self._gen_function_stub(name, params, retrn, indent, privacy or self.default_privacy,
                                                      return_type, flags))
        self._after_function_paste(name, params, retrn, indent, privacy or self.default_privacy, return_type, flags)
        return True

    def create_class(self, name, base, interfaces, indent='', privacy=None, flags=0):
        name = self.class_case(name)
        self.__send_to_editor(self._gen_class_stub(name, base, interfaces, indent,
                                                   privacy or self.default_privacy, flags))
        self._after_class_paste(name, base, interfaces, indent, privacy or self.default_privacy, flags)
        return True

    def create_file(self, name, directory, class_info=None):
        name = self.file_case(name)
        if not name.endswith(self.ext):
            name += self.ext
        path = os.path.join(directory, name)
        if not os.path.exists(path):
            text = self._gen_file_stub(name, directory, class_info)
            if class_info and class_info[0]:
                class_info[1] = self.class_case(class_info[1])
                text += self._gen_class_stub(*class_info)
            with open(path, 'w') as f:
                f.write(text)
            self._after_file_create(name, directory, class_info)
            return True
        return False

    def create_print(self):
        self.__send_to_editor(self._gen_print_stub())
        self._after_print_paste()
        return True

    def create_this(self):
        self.__send_to_editor(self._gen_this_stub())
        return True

    def create_define(self, var_name):
        var_name = self.var_case(var_name)
        self.__send_to_editor(self._gen_define_stub(var_name))
        self._after_define_paste(var_name)
        return True

    def create_for(self, iterator, items, max_i=0, indent=''):
        self.__send_to_editor(self._gen_for_stub(iterator, items, max_i, indent))
        self._after_for_paste(iterator, items, max_i, indent)
        return True
