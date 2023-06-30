#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
import os
from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
storage_t = os.getenv("HBNB_TYPE_STORAGE")
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    if storage_t != "db":
        def setUp(self):
            """ Set up test environment """
            del_list = []
            for key in storage._FileStorage__objects.keys():
                del_list.append(key)
            for key in del_list:
                del storage._FileStorage__objects[key]

        def tearDown(self):
            """ Remove storage file at end of tests """
            try:
                os.remove('file.json')
            except:
                pass

        def test_obj_list_empty(self):
            """ __objects is initially empty """
            self.assertEqual(len(storage.all()), 0)

        def test_all(self):
            """ __objects is properly returned """
            new = BaseModel()
            temp = storage.all()
            self.assertIsInstance(temp, dict)

        def test_base_model_instantiation(self):
            """ File is not created on BaseModel save """
            new = BaseModel()
            self.assertFalse(os.path.exists('file.json'))

        def test_empty(self):
            """ Data is saved to file """
            new = BaseModel()
            thing = new.to_dict()
            new.save()
            new2 = BaseModel(**thing)
            self.assertNotEqual(os.path.getsize('file.json'), 0)

        def test_save(self):
            """ FileStorage save method """
            new = BaseModel()
            storage.save()
            self.assertTrue(os.path.exists('file.json'))

        def test_reload_empty(self):
            """ Load from an empty file """
            with open('file.json', 'w') as f:
                pass
            with self.assertRaises(ValueError):
                storage.reload()

        def test_reload_from_nonexistent(self):
            """ Nothing happens if file does not exist """
            self.assertEqual(storage.reload(), None)

        def test_base_model_save(self):
            """ BaseModel save method calls storage save """
            new = BaseModel()
            new.save()
            self.assertTrue(os.path.exists('file.json'))

        def test_type_path(self):
            """ Confirm __file_path is string """
            self.assertEqual(type(storage._FileStorage__file_path), str)

        def test_type_objects(self):
            """ Confirm __objects is a dict """
            self.assertEqual(type(storage.all()), dict)

        def test_storage_var_created(self):
            """ FileStorage object storage created """
            from models.engine.file_storage import FileStorage
            print(type(storage))
            self.assertEqual(type(storage), FileStorage)


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    if storage_t != "db":
        @classmethod
        def setUpClass(cls):
            """Set up for the doc tests"""
            cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

        def test_pep8_conformance_file_storage(self):
            """Test that models/engine/file_storage.py conforms to PEP8."""
            pep8s = pep8.StyleGuide(quiet=True)
            result = pep8s.check_files(['models/engine/file_storage.py'])
            self.assertEqual(result.total_errors, 0,
                             "Found code style errors (and warnings).")

        def test_file_storage_module_docstring(self):
            """Test for the file_storage.py module docstring"""
            self.assertIsNot(file_storage.__doc__, None,
                             "file_storage.py needs a docstring")
            self.assertTrue(len(file_storage.__doc__) >= 1,
                            "file_storage.py needs a docstring")

        def test_file_storage_class_docstring(self):
            """Test for the FileStorage class docstring"""
            self.assertIsNot(FileStorage.__doc__, None,
                             "FileStorage class needs a docstring")
            self.assertTrue(len(FileStorage.__doc__) >= 1,
                            "FileStorage class needs a docstring")

        def test_fs_func_docstrings(self):
            """Test for the presence of docstrings in FileStorage methods"""
            for func in self.fs_f:
                self.assertIsNot(func[1].__doc__, None,
                                 "{:s} method needs a docstring".format(
                                     func[0]))
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".format(
                    func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    if storage_t != "db":
        @unittest.skipIf(storage_t == 'db', "not testing file storage")
        def test_all_returns_dict(self):
            """Test that all returns the FileStorage.__objects attr"""
            storage = FileStorage()
            new_dict = storage.all()
            self.assertEqual(type(new_dict), dict)
            self.assertIs(new_dict, storage._FileStorage__objects)

        @unittest.skipIf(storage_t == 'db', "not testing file storage")
        def test_new(self):
            """test that new adds an object to the
            FileStorage.__objects attr"""
            storage = FileStorage()
            save = FileStorage._FileStorage__objects
            FileStorage._FileStorage__objects = {}
            test_dict = {}
            for key, value in classes.items():
                with self.subTest(key=key, value=value):
                    instance = value()
                    instance_key = "{}{}{}".format(
                        instance.__class__.__name__, ".",
                        instance.id)
                    storage.new(instance)
                    test_dict[instance_key] = instance
                    self.assertEqual(test_dict, storage._FileStorage__objects)
            FileStorage._FileStorage__objects = save

        @unittest.skipIf(storage_t == 'db', "not testing file storage")
        def test_save(self):
            """Test that save properly saves objects to file.json"""
            storage = FileStorage()
            new_dict = {}
            for key, value in classes.items():
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                new_dict[instance_key] = instance
            save = FileStorage._FileStorage__objects
            FileStorage._FileStorage__objects = new_dict
            storage.save()
            FileStorage._FileStorage__objects = save
            for key, value in new_dict.items():
                new_dict[key] = value.to_dict()
            string = json.dumps(new_dict)
            with open("file.json", "r") as f:
                js = f.read()
            self.assertEqual(json.loads(string), json.loads(js))
