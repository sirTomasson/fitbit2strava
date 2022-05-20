import unittest


class SandboxTest(unittest.TestCase):

    def test_merge_dicts(self):
        dict1 = {"a": None, "b": 2}
        dict2 = {"a": 2, "b": 4, "c": 3}
        dict3 = {**dict1, **dict2}

        self.assertEqual(dict3["a"], 2, "a should be 2")
        self.assertEqual(dict3["b"], 4, "a should be 4")
        self.assertEqual(dict3["c"], 3, "a should be 3")

        dict3 = {**dict2, **dict1}

        self.assertEqual(dict3["a"], None, "a should be None")
        self.assertEqual(dict3["b"], 2, "a should be 2")
        self.assertEqual(dict3["c"], 3, "a should be 3")





if __name__ == "__main__":
    unittest.main()
