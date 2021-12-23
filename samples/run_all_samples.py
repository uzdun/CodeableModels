from plant_uml_renderer import PlantUMLGenerator
import os
from shutil import copyfile
from multiprocessing import Process

DOCS_DIR = "../docsrc"


def run_shopping_model1():
    import samples.shopping_model1 as shopping_model1
    shopping_model1.run()


def run_shopping_model2():
    import samples.shopping_model2 as shopping_model2
    shopping_model2.run()


def run_shopping_model3():
    import samples.shopping_model3 as shopping_model3
    shopping_model3.run()


def run_shopping_instances1():
    import samples.shopping_instances1 as shopping_instances1
    shopping_instances1.run()


def run_shopping_instances2():
    import samples.shopping_instances2 as shopping_instances2
    shopping_instances2.run()


def shopping_activities1_instance_model():
    import samples.shopping_activities1_instance_model as shopping_activities1_instance_model
    shopping_activities1_instance_model.run()


def shopping_activities1_class_model():
    import samples.shopping_activities1_class_model as shopping_activities1_class_model
    shopping_activities1_class_model.run()


def run_shopping_shopping_activity_model2():
    import samples.shopping_activity_model2 as shopping_activity_model2
    shopping_activity_model2.run()


def run_microservice_component_model1_class_model():
    import samples.microservice_component_model1_class_model as microservice_component_model1_class_model
    microservice_component_model1_class_model.run()


def run_microservice_component_model1_instance_model():
    import samples.microservice_component_model1_class_model as microservice_component_model1_instance_model
    microservice_component_model1_instance_model.run()


def run_microservice_component_model2_class_model():
    import samples.microservice_component_model2_class_model as microservice_component_model2_class_model
    microservice_component_model2_class_model.run()


def run_microservice_component_model2_instance_model():
    import samples.microservice_component_model2_instance_model as microservice_component_model2
    microservice_component_model2.run()


def run_microservice_component_model3_class_model():
    import samples.microservice_component_model3_class_model as microservice_component_model3_class_model
    microservice_component_model3_class_model.run()


def run_microservice_component_model3_instance_model():
    import samples.microservice_component_model3_instance_model as microservice_component_model3
    microservice_component_model3.run()


def run_metamodel_rendering():
    import samples.metamodel_rendering as metamodel_rendering
    metamodel_rendering.run()


def run_codeable_models_class_relations():
    import samples.codeable_models_class_relations as codeable_models_class_relations
    codeable_models_class_relations.run()


def run_in_process(method):
    p = Process(target=method)
    p.start()
    p.join()


def run_all():
    generator = PlantUMLGenerator()
    generator.delete_gen_dir()

    for method in [run_shopping_model1, run_shopping_model2, run_shopping_model3,
                   run_shopping_instances1, run_shopping_instances2,
                   shopping_activities1_class_model, shopping_activities1_instance_model,
                   run_shopping_shopping_activity_model2,
                   run_microservice_component_model1_class_model(),
                   run_microservice_component_model1_instance_model(),
                   run_microservice_component_model2_class_model(),
                   run_microservice_component_model2_instance_model(),
                   run_microservice_component_model3_class_model(),
                   run_microservice_component_model3_instance_model(),
                   run_metamodel_rendering,
                   run_codeable_models_class_relations
                   ]:
        run_in_process(method)

    return generator.directory


def copy_all_png_images_to_docs(directory):
    print("***************** Copying Files to Docs *****************")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                src = os.path.join(root, file)
                dst = os.path.join(f"{DOCS_DIR!s}/source/images", file)
                print(f"... copy {src!s} to {dst!s}")
                copyfile(src, dst)


if __name__ == "__main__":
    gen_dir = run_all()
    copy_all_png_images_to_docs(gen_dir)
