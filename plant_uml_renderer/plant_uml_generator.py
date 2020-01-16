import os
import shutil

from plant_uml_renderer.class_model_renderer import ClassModelRenderer
from plant_uml_renderer.object_model_renderer import ObjectModelRenderer


class PlantUMLGenerator(object):
    def __init__(self, delete_gen_dir=True):
        self._directory = "../_generated"
        self._plant_uml_jar_path = "../../libs/plantuml.jar"
        if delete_gen_dir:
            if os.path.exists(self.directory):
                shutil.rmtree(self.directory)
            os.makedirs(self.directory)
        self.classModelRenderer = ClassModelRenderer(plant_uml_jar_path=self._plant_uml_jar_path,
                                                     directory=self._directory)
        self.objectModelRenderer = ObjectModelRenderer(plant_uml_jar_path=self._plant_uml_jar_path,
                                                       directory=self._directory)

    @staticmethod
    def get_file_name(element_name):
        name = element_name.replace(' ', '_')
        return name

    def generate_class_model(self, bundle, **kwargs):
        self.classModelRenderer.render_class_model_to_file(self.get_file_name(bundle.name), bundle.elements, **kwargs)

    def generate_object_model(self, bundle, **kwargs):
        self.objectModelRenderer.render_object_model_to_file(self.get_file_name(bundle.name), bundle.elements, **kwargs)

    def generate_class_models(self, dir_name, view_list):
        main_dir = self.directory
        self.directory = f"{main_dir!s}/{self.get_file_name(dir_name)!s}"
        for bundle, kwargs in zip(view_list[::2], view_list[1::2]):
            self.generate_class_model(bundle, **kwargs)
        self.directory = main_dir

    def generate_object_models(self, dir_name, view_list):
        main_dir = self.directory
        self.directory = f"{main_dir!s}/{self.get_file_name(dir_name)!s}"
        for bundle, kwargs in zip(view_list[::2], view_list[1::2]):
            self.generate_object_model(bundle, **kwargs)
        self.directory = main_dir

    @property
    def plant_uml_jar_path(self):
        return self._plant_uml_jar_path

    @plant_uml_jar_path.setter
    def plant_uml_jar_path(self, plant_uml_jar_path):
        self._plant_uml_jar_path = plant_uml_jar_path
        self.classModelRenderer.plant_uml_jar_path = plant_uml_jar_path
        self.objectModelRenderer.plant_uml_jar_path = plant_uml_jar_path

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, directory):
        self._directory = directory
        self.classModelRenderer.directory = directory
        self.objectModelRenderer.directory = directory
