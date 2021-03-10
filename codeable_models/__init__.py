"""

Codeable Models is a Python API for programmatically creating del akin to UML or EMF del.
The goal of the module is to provide a lightweight codeable modeling API. The module is used as a
foundation for working programmatically with del.

Typical use case for Codeable Models are:

- Create del textually and be able to use textual tools such as search & replace, copy & paste, grep,
  and so on to edit them.
- Ease model creation and manipulation through code - provided in Python scripts with little to no boilerplate code.
- Using Python code to ensure model consistency, perform constraint checking, perform analyses, and calculate metrics.
- Create domain del in your code and use them at runtime in your Python project, e.g. to realize a
  portion of the software system to reflect the domain model in a very literal way
  as envisaged in Domain-driven Design (DDD).
- Generate visual representations of those del such as  UML diagrams and tables,
  e.g. used to support understanding the big picture and communicating the model.
- Generate other textual representations, such as Markdown or Latex texts.
- Generate code and/or configuration scripts from the del.

Import it with::

    import codeable_models

or import its classes and functions, e.g.::

    from codeable_models import CClass, CMetaclass, CBundle, CException, CStereotype, add_links

"""

from codeable_models.cexception import CException
from codeable_models.cnamedelement import CNamedElement
from codeable_models.cbundlable import CBundlable
from codeable_models.cattribute import CAttribute
from codeable_models.cclassifier import CClassifier
from codeable_models.cmetaclass import CMetaclass
from codeable_models.cstereotype import CStereotype
from codeable_models.cclass import CClass
from codeable_models.cobject import CObject
from codeable_models.cenum import CEnum
from codeable_models.cbundle import CBundle, CPackage, CLayer
from codeable_models.cassociation import CAssociation
from codeable_models.clink import CLink, set_links, add_links, delete_links
