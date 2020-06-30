from plant_uml_renderer import PlantUMLGenerator
import os
from shutil import copyfile

DOCS_DIR = "../docs"


def run_all():
    generator = PlantUMLGenerator()
    generator.delete_gen_dir()

    import samples.shopping_model1 as shopping_model1
    shopping_model1.run()
    import samples.shopping_model2 as shopping_model2
    shopping_model2.run()
    import samples.shopping_model3 as shopping_model3
    shopping_model3.run()
    import samples.shopping_instances1 as shopping_instances1
    shopping_instances1.run()
    import samples.shopping_instances2 as shopping_instances2
    shopping_instances2.run()
    import samples.shopping_activity_model1 as shopping_activity_model1
    shopping_activity_model1.run()
    import samples.shopping_activity_model2 as shopping_activity_model2
    shopping_activity_model2.run()
    import samples.microservice_component_model1 as microservice_component_model1
    microservice_component_model1.run()
    import samples.microservice_component_model2 as microservice_component_model2
    microservice_component_model2.run()
    import samples.microservice_component_model3 as microservice_component_model3
    microservice_component_model3.run()
    import samples.metamodel_rendering as metamodel_rendering
    metamodel_rendering.run()
    import samples.codeable_models_class_relations as codeable_models_class_relations
    codeable_models_class_relations.run()

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
