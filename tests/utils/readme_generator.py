import inspect
import os
import textwrap


class Readme:

    def __init__(self, readme_file: str):
        self._readme_file = open(readme_file, 'w')

    def append(self, data):
        self._readme_file.write(data)

    def append_doc(self, data):
        dedent_data = textwrap.dedent(data)
        self.append(f"{dedent_data}{os.linesep}")

    def append_python_src(self, python_src):
        dedent_python_src = textwrap.dedent(python_src)
        self.append(f"```python{os.linesep}{dedent_python_src}```{os.linesep}")

    @staticmethod
    def extract_doc_string(python_entity):
        doc_string = inspect.getdoc(python_entity)
        return doc_string

    @staticmethod
    def extract_python_src(python_entity):
        doc_string = Readme.extract_doc_string(python_entity)


        source = inspect.getsource(python_entity)

        index_of_doc = -1
        tries = 0
        while index_of_doc < 0:
            try:
                index_of_doc = source.index(doc_string)
            except ValueError as e:
                tries += 1
                if tries > 100:
                    raise e
                doc_string = textwrap.indent(doc_string, ' ')

        source_start = index_of_doc + len(doc_string)
        python_src = source[source_start:]
        python_src = python_src.lstrip().lstrip('"')
        # python_src = textwrap.dedent(python_src)
        # python_src = python_src.lstrip()
        return python_src

    def process_python_src(self, python_src: str):
        dedent_python_src = textwrap.dedent(python_src)
        lines_itr = iter(dedent_python_src.splitlines(keepends=True))
        line = next(lines_itr)
        self.process_python_src_segment(line, lines_itr)

    def process_python_src_segment(self, line, lines_itr):
        buffer = line
        for line in lines_itr:
            if not line.startswith('#'):
                buffer += line
            else:
                if not buffer.isspace():
                    self.append_python_src(buffer)
                self.process_comment_segment(line, lines_itr)
                return
        self.append_python_src(buffer)

    def process_comment_segment(self, line, lines_itr):
        buffer = line[1:]
        for line in lines_itr:
            if line.startswith('#'):
                buffer += line[1:]
            elif not line.strip():
                buffer += line
            else:
                self.append_doc(buffer)
                self.process_python_src_segment(line, lines_itr)
                return
        self.append_doc(buffer)

    def append_function(self, function):
        doc_string = self.extract_doc_string(function)
        self.append_doc(doc_string)

        python_src = self.extract_python_src(function)
        self.process_python_src(python_src)

        return function

    def __iadd__(self, p2):
        dedent_txt = textwrap.dedent(p2)
        self.append(dedent_txt)
        self.append(os.linesep)
        return self
