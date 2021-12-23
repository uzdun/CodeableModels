from codeable_models import CException
from codeable_models.internal.commons import set_keyword_args, is_cclass, is_cobject
# from enum import Enum 
# from codeable_models import CNamedElement
from plant_uml_renderer.model_renderer import RenderingContext, ModelRenderer


class ObjectRenderingContext(RenderingContext):
    def __init__(self):
        super().__init__()
        self.visited_links = set()
        self.render_attribute_values = True
        self.render_empty_attributes = False
        self.render_association_names_when_no_label_is_given = False
        self.excluded_links = []


class ObjectModelRenderer(ModelRenderer):
    def render_object_specification(self, context, object_):
        obj_name = object_.name
        if obj_name is None:
            obj_name = ""
        if is_cclass(object_):
            object_ = object_.class_object

        stereotype_string = ""
        tagged_value_string = ""
        if object_.class_object_class is not None:
            stereotype_string = self.render_stereotypes(object_.class_object_class.stereotype_instances)
            if context.render_tagged_values:
                tagged_value_string = self.render_tagged_values(object_.class_object_class,
                                                                object_.class_object_class.stereotype_instances)
                if len(tagged_value_string) > 0:
                    tagged_value_string = tagged_value_string + "\\n"

        cl_name = object_.classifier.name
        if cl_name is None:
            cl_name = ""

        obj_string = " : " + cl_name
        if obj_name != "":
            obj_string = obj_name + obj_string

        if len(stereotype_string) > 0:
            stereotype_string = " " + stereotype_string + " "

        context.add_line("class \"" + tagged_value_string + self.pad_and_break_name(obj_string, None, True) + "\" as " +
                         self.get_node_id(context, object_) + stereotype_string + self.render_attribute_values(
            context, object_))

    def render_link(self, context, link):
        association = link.association

        arrow = " --> "
        if association.aggregation:
            arrow = " o-- "
        elif association.composition:
            arrow = " *-- "

        stereotype_string = self.render_stereotypes(link.stereotype_instances, True)
        if context.render_tagged_values:
            tagged_value_string = self.render_tagged_values(link, link.stereotype_instances)
            if len(tagged_value_string) > 0:
                stereotype_string += "\\n" + tagged_value_string

        label = ""
        if link.label is not None and len(link.label) != 0:
            label = link.label
        elif context.render_association_names_when_no_label_is_given and association.name is not None and len(
                association.name) != 0:
            label = association.name
        if stereotype_string != "" and len(label) > 0:
            stereotype_string = stereotype_string + "\\n"
        label = stereotype_string + self.break_name(label)
        if len(label) > 0:
            label = ": " + label

        context.add_line(
            self.get_node_id(context, link.source) + arrow + self.get_node_id(context, link.target) + label)

    def render_links(self, context, obj, obj_list):
        for classifier in obj.classifier.class_path:
            for association in classifier.associations:
                links = [l for l in obj.links if l.association == association]
                for link in links:
                    if link in context.excluded_links:
                        continue
                    source = link.source
                    if is_cclass(source):
                        source = source.class_object
                    target = link.target
                    if is_cclass(target):
                        target = target.class_object
                    if source != obj:
                        # only render links outgoing from this object
                        continue
                    if link not in context.visited_links:
                        context.visited_links.add(link)
                        if target in obj_list:
                            self.render_link(context, link)

    def render_objects(self, context, objects):
        obj_list = []
        for obj in objects:
            if is_cclass(obj):
                # use class objects and not classes in this renderer
                obj_list.extend([obj.class_object_])
            elif is_cobject(obj):
                obj_list.extend([obj])
            else:
                raise CException(f"'{obj!s}' handed to object renderer is no an object or class'")
        for obj in obj_list:
            self.render_object_specification(context, obj)
        for obj in obj_list:
            self.render_links(context, obj, obj_list)

    def render_object_model(self, object_list, **kwargs):
        context = ObjectRenderingContext()
        set_keyword_args(context,
                         ["render_attribute_values", "render_empty_attributes",
                          "render_association_names_when_no_label_is_given",
                          "excluded_links", "render_tagged_values"], **kwargs)
        self.render_start_graph(context)
        self.render_objects(context, object_list)
        self.render_end_graph(context)
        return context.result

    def render_object_model_to_file(self, file_name_base, class_list, **kwargs):
        source = self.render_object_model(class_list, **kwargs)
        self.render_to_files(file_name_base, source)
