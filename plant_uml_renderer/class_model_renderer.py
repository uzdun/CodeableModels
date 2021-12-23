from codeable_models import CException
from codeable_models.internal.commons import is_cenum, is_cclassifier, set_keyword_args, is_cstereotype, is_cmetaclass, \
    is_cclass
from plant_uml_renderer.model_renderer import RenderingContext, ModelRenderer


class ClassifierRenderingContext(RenderingContext):
    def __init__(self):
        super().__init__()
        self.visited_associations = set()
        self.render_associations = True
        self.render_inheritance = True
        self.render_attributes = True
        self.excluded_associations = []
        self.included_associations = None
        self.render_extended_relations = True
        self.excluded_extended_classes = []
        self.included_extended_classes = None
        self.render_metaclass_as_stereotype = False


class ClassModelRenderer(ModelRenderer):
    def render_classifier_specification(self, context, cl):
        stereotype_string = ""
        tagged_value_string = ""

        if is_cstereotype(cl):
            stereotype_string = self.render_stereotypes_string("stereotype")
        if is_cmetaclass(cl):
            stereotype_string = self.render_stereotypes_string("metaclass")
        if is_cclass(cl):
            stereotype_string = self.render_stereotypes(cl.stereotype_instances)
            if context.render_tagged_values:
                tagged_value_string = self.render_tagged_values(cl, cl.stereotype_instances)
                if len(tagged_value_string) > 0:
                    tagged_value_string = tagged_value_string + "\\n"
            if context.render_metaclass_as_stereotype:
                stereotype_string = self.render_stereotypes_string(cl.metaclass.name) + stereotype_string

        if len(stereotype_string) > 0:
            stereotype_string = " " + stereotype_string + " "
        name_label = '"' + tagged_value_string + self.pad_and_break_name(cl.name, None, True) + '"'
        context.add_line(
            "class " + name_label + " as " + self.get_node_id(context, cl) +
            stereotype_string + self.render_attributes(context, cl))

    def render_attributes(self, context, cl):
        if not context.render_attributes:
            return ""
        if is_cenum(cl):
            if len(cl.values) == 0:
                return ""
            value_string = "{\n"
            for value in cl.values:
                value_string += value + "\n"
            value_string += "}\n"
            return value_string
        # this is a classifier
        if len(cl.attributes) == 0:
            return ""
        attribute_string = "{\n"
        for attribute in cl.attributes:
            attribute_string += self.render_attribute(attribute)
        attribute_string += "}\n"
        return attribute_string

    @staticmethod
    def render_attribute(attribute):
        type_ = attribute.type
        t = None
        if is_cenum(type_) or is_cclassifier(type_):
            t = type_.name
            if t is None:
                t = " "
        elif type_ == str:
            t = "String"
        elif type_ == int:
            t = "Integer"
        elif type_ == float:
            t = "Float"
        elif type_ == bool:
            t = "Boolean"
        elif type_ == list:
            t = "List"
        if t is None:
            raise CException(f"unknown type of attribute: '{attribute!s}")
        return attribute.name + ": " + t + "\n"

    def render_associations(self, context, cl, class_list):
        if not context.render_associations:
            return
        if is_cenum(cl):
            return
        for association in cl.associations:
            if context.included_associations is not None:
                if association not in context.included_associations:
                    continue
            if association in context.excluded_associations:
                continue
            if not association.source == cl:
                # only render associations outgoing from this class
                continue
            if association not in context.visited_associations:
                context.visited_associations.add(association)
                if association.target in class_list:
                    self.render_association(context, association, class_list)

    def render_association(self, context, association, class_list):
        arrow = " --> "
        if association.aggregation:
            arrow = " o-- "
        elif association.composition:
            arrow = " *-- "

        # as we cannot point directly to the association extended in a metamodel, we put a note 
        # on the association saying which stereotypes extend it
        extended_by_string = ""
        first_loop_iteration = True

        for stereotype in association.stereotypes:
            if stereotype in class_list:
                if first_loop_iteration:
                    extended_by_string = extended_by_string + "\\n" + \
                                         self.render_stereotypes_string("stereotypes") + "\\n"
                    first_loop_iteration = False
                else:
                    extended_by_string = extended_by_string + ", "
                extended_by_string = extended_by_string + f"{stereotype.name!s}"
        if extended_by_string != "":
            extended_by_string = extended_by_string + ""

        stereotype_string = self.render_stereotypes(association.stereotype_instances, True)
        if context.render_tagged_values:
            tagged_value_string = self.render_tagged_values(association, association.stereotype_instances)
            if len(tagged_value_string) > 0:
                stereotype_string += "\\n" + tagged_value_string

        label = ""
        if association.name is not None and len(association.name) != 0:
            label = association.name
        if extended_by_string != "":
            label = label + extended_by_string
        if len(label) > 0:
            label = self.break_name(label)
        if stereotype_string != "":
            if len(label) > 0:
                label = label + '\\n'
            label = label + stereotype_string
        if len(label) > 0:
            label = ': "' + label + '"'

        head_label = ""
        if not (association.aggregation or association.composition):
            head_label = " \" " + association.source_multiplicity + " \" "
        tail_label = " \" " + association.multiplicity + " \" "

        context.add_line(self.get_node_id(context, association.source) + head_label +
                         arrow + tail_label + self.get_node_id(context, association.target) + label)

    def render_extended_relations(self, context, stereotype, class_list):
        if not context.render_extended_relations:
            return
        for extended in stereotype.extended:
            if is_cmetaclass(extended):
                if context.included_extended_classes:
                    if extended not in context.included_extended_classes:
                        continue
                if extended in context.excluded_extended_classes:
                    continue
                if extended in class_list:
                    context.add_line(self.get_node_id(context, stereotype) + " --> " +
                                     self.get_node_id(context, extended) + ': "' +
                                     self.render_stereotypes_string("extended") + '"')

    def render_inheritance_relations(self, context, class_list):
        if not context.render_inheritance:
            return
        for cl in class_list:
            if is_cenum(cl):
                continue
            for sub_class in cl.subclasses:
                if sub_class in class_list:
                    context.add_line(self.get_node_id(context, cl) + " <|--- " + self.get_node_id(context, sub_class))

    def render_classes(self, context, class_list):
        for cl in class_list:
            if not is_cclassifier(cl) and not is_cenum(cl):
                raise CException(f"'{cl!s}' handed to class renderer is not a classifier or enum'")
            self.render_classifier_specification(context, cl)
        self.render_inheritance_relations(context, class_list)
        for cl in class_list:
            self.render_associations(context, cl, class_list)
            if is_cstereotype(cl):
                self.render_extended_relations(context, cl, class_list)

    def render_class_model(self, class_list, **kwargs):
        context = ClassifierRenderingContext()
        set_keyword_args(context,
                         ["render_associations", "render_inheritance", "render_attributes", "excluded_associations",
                          "included_associations", "render_extended_relations",
                          "excluded_extended_classes", "included_extended_classes",
                          "render_metaclass_as_stereotype", "render_tagged_values"],
                         **kwargs)
        self.render_start_graph(context)
        self.render_classes(context, class_list)
        self.render_end_graph(context)
        return context.result

    def render_class_model_to_file(self, file_name_base, class_list, **kwargs):
        source = self.render_class_model(class_list, **kwargs)
        self.render_to_files(file_name_base, source)
