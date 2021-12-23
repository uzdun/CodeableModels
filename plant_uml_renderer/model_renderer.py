import os
from enum import Enum
from subprocess import call

from codeable_models import *
from codeable_models.internal.commons import set_keyword_args, is_cobject


def get_encoded_name(element):
    if isinstance(element, CNamedElement):
        name = f"_{element.name}"
        if name is None:
            return ""
        # put a placeholder _ in the name for special characters as plantuml does not
        # support many of them
        name = "".join([c if c.isalnum() else "_" for c in name])
        return name
    return ""


class RenderingContext(object):
    def __init__(self):
        super().__init__()
        self.result = ""
        self.indent = 0
        self.indent_cache_string = ""
        self.node_ids = {}
        self.current_node_id = 0
        self.render_tagged_values = True

    def get_node_id(self, element):
        if is_cobject(element) and element.class_object_class is not None:
            # use the class object's class rather than the class object to identify them uniquely
            element = element.class_object_class
        if element in self.node_ids:
            return self.node_ids[element]
        else:
            self.current_node_id += 1
            name = f"__{self.current_node_id!s}" + get_encoded_name(element)
            self.node_ids[element] = name
            return name

    def add_line(self, string):
        self.result += self.indent_cache_string + string + "\n"

    def add_with_indent(self, string):
        self.result += self.indent_cache_string + string

    def add(self, string):
        self.result += string

    def increase_indent(self):
        self.indent += 2
        self.indent_cache_string = " " * self.indent

    def decrease_indent(self):
        self.indent -= 2
        self.indent_cache_string = " " * self.indent


class ModelStyle(Enum):
    PLAIN = 0
    HANDWRITTEN = 1
    PLAIN_HELVETICA = 2
    ORIGINAL = 3


class ModelRenderer(object):
    def __init__(self, **kwargs):
        # defaults for config parameters
        self.directory = "./gen"
        self.plant_uml_jar_path = "../libs/plantuml.jar"
        self.render_png = True
        self.render_svg = True

        self.name_break_length = 25
        self.name_padding = ""
        self.style = ModelStyle.PLAIN
        self.left_to_right = False

        self.ID = 0

        super().__init__()
        self._init_keyword_args(**kwargs)

    def _init_keyword_args(self, legal_keyword_args=None, **kwargs):
        if legal_keyword_args is None:
            legal_keyword_args = ["directory", "plant_uml_jar_path", "genSVG", "genPNG"]
        set_keyword_args(self, legal_keyword_args, **kwargs)

    def render_start_graph(self, context):
        context.add_line("@startuml")
        if (self.style == ModelStyle.HANDWRITTEN or self.style == ModelStyle.PLAIN or
                self.style == ModelStyle.PLAIN_HELVETICA):
            context.add_line("skinparam monochrome true")
            context.add_line("skinparam ClassBackgroundColor White")
            context.add_line("hide empty members")
            context.add_line("hide circle")
            if self.style == ModelStyle.HANDWRITTEN:
                # context.addLine("skinparam defaultFontName MV Boli")
                context.add_line("skinparam defaultFontName Segoe Print")
                context.add_line("skinparam defaultFontSize 14")
                context.add_line("skinparam handwritten true")
                context.add_line("skinparam shadowing false")
            if self.style == ModelStyle.PLAIN:
                context.add_line("skinparam defaultFontName Arial")
                context.add_line("skinparam defaultFontSize 11")
                # context.add_line("skinparam classfontstyle bold")
            if self.style == ModelStyle.PLAIN_HELVETICA:
                context.add_line("skinparam defaultFontName Helvetica")
                context.add_line("skinparam defaultFontSize 11")
                # context.add_line("skinparam classfontstyle bold")
        if self.left_to_right:
            context.add_line("left to right direction")

    @staticmethod
    def render_end_graph(context):
        context.add_line("@enduml")

    @staticmethod
    def render_stereotypes_string(stereotypes_string):
        return "<<" + stereotypes_string + ">>"

    @staticmethod
    def render_stereotypes(stereotypes, add_line_breaks=False):
        if len(stereotypes) == 0:
            return ""
        result = ""
        first_stereotype = True
        for stereotype in stereotypes:
            if first_stereotype:
                first_stereotype = False
            else:
                if add_line_breaks:
                    result += "\\n"
            result += "<<" + stereotype.name + ">>"
        return result

    def render_tagged_values(self, stereotyped_element_instance, stereotypes):
        if len(stereotypes) == 0:
            return ""

        tagged_values_string = "{"
        rendered_tagged_values = []

        for stereotype in stereotypes:
            stereotype_class_path = stereotype.class_path

            for stereotypeClass in stereotype_class_path:
                for taggedValue in stereotypeClass.attributes:
                    if not [taggedValue.name, stereotypeClass] in rendered_tagged_values:
                        value = stereotyped_element_instance.get_tagged_value(taggedValue.name, stereotypeClass)
                        if value is not None:
                            if len(rendered_tagged_values) != 0:
                                tagged_values_string += ", \\n"
                            tagged_values_string += self.render_attribute_value(taggedValue, taggedValue.name, value)
                            rendered_tagged_values.append([taggedValue.name, stereotypeClass])

        if len(rendered_tagged_values) != 0:
            tagged_values_string += "}"
        else:
            tagged_values_string = ""
        return tagged_values_string

    def render_attribute_values(self, context, obj):
        if not context.render_attribute_values:
            return ""
        attribute_value_added = False
        attribute_value_string = " {\n"
        rendered_attributes = set()
        for cl in obj.classifier.class_path:
            attributes = cl.attributes
            for attribute in attributes:
                name = attribute.name
                value = obj.get_value(name, cl)

                # don't render the same attribute twice, but only the one that is lowest in the class hierarchy
                if name in rendered_attributes:
                    continue
                else:
                    rendered_attributes.add(name)

                if not context.render_empty_attributes:
                    if value is None:
                        continue
                attribute_value_added = True
                attribute_value_string += self.render_attribute_value(attribute, name, value) + "\n"
        attribute_value_string += "}\n"
        if not attribute_value_added:
            attribute_value_string = ""
        return attribute_value_string

    def render_attribute_value(self, attribute, name, value):
        type_ = attribute.type
        if type_ == str:
            value = '"' + str(value) + '"'
        elif type_ == list and value is not None:
            result = []
            for elt in value:
                if isinstance(elt, str):
                    result.append('"' + str(elt) + '"')
                else:
                    result.append(str(elt))
            value = "[" + ", ".join(result) + "]"
        _check_for_illegal_value_characters(str(value))
        return self.break_name(name + ' = ' + str(value))

    def pad_and_break_name(self, name, name_padding=None, make_bold=False):
        if name_padding is None:
            name_padding = self.name_padding

        if name is None:
            name = " "

        if len(name) <= self.name_break_length:
            line = name_padding + name + name_padding
            if make_bold:
                line = "<b>" + line + "</b>"
            return line

        result = ""
        count = 0
        current_first_index = 0
        for i, v in enumerate(name):
            if v == ' ' and count >= self.name_break_length:
                if name[i - 1] == ':':
                    # we don't want to end the line with a ':', break on next occasion
                    continue
                if i + 1 < len(name) and name[i + 1] == '=':
                    # we don't want to break if the next line starts with '=' as this leads to some 
                    # undocumented font size increase in plant uml, break on next occasion
                    continue
                count = 0
                new_line = name_padding + name[current_first_index:i] + name_padding
                if make_bold:
                    new_line = "<b>" + new_line + "</b>"
                result = result + new_line + "\\n"
                current_first_index = i + 1
            count += 1
        new_line = name_padding + name[current_first_index:len(name)] + name_padding
        if make_bold:
            new_line = "<b>" + new_line + "</b>"
        result = result + new_line
        return result

    def break_name(self, name):
        return self.pad_and_break_name(name, "")

    @staticmethod
    def get_node_id(context, element):
        return context.get_node_id(element)

    def render_to_files(self, file_name_base, source):
        file_name_base_with_dir = f"{self.directory!s}/{file_name_base!s}"
        file_name_txt = file_name_base_with_dir + ".txt"
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        file = open(file_name_txt, "w")
        file.write(source)
        file.close()
        if self.render_png:
            call(["java", "-jar", f"{self.plant_uml_jar_path!s}", f"{file_name_txt!s}"])
        if self.render_svg:
            call(["java", "-jar", f"{self.plant_uml_jar_path!s}", f"{file_name_txt!s}", "-tsvg"])


def _check_for_illegal_value_characters(value):
    if '(' in value or ')' in value:
        raise CException(
            f"in value `{value!s}`: " +
            "do not use `(` or `)` in attribute values, as PlantUML interprets them as method parameters " +
            "and would start a new compartment if they are part of an attribute value")
