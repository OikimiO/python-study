# 믹스인 클래스로 같은 결과를 얻을 수 있다면 다중 상속을 사용하지 말자
# 인스턴스 수준에서 동작을 교체할 수 있게 만들어서 믹스인 클래스가 요구할 때 클래스별로 원하는 동작을 하게 하자
# 간단한 동작들로 복잡한 기능을 생성하려면 믹스인을 조합하자
import json

class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

class BinaryTree(ToDictMixin):
    def __init__(self, value, left =None, right=None):
        self.value = value
        self.left = left
        self.right = right
# {'value': 10,
# 'left': {'value': 7, 'left': None,
#          'right': {'value': 9, 'left': None, 'right': None}
#          },
# 'right': {'value': 13,
#           'left': {'value': 11, 'left': None, 'right': None},
#           'right': None}
#           }
tree = BinaryTree(10,
                  left=BinaryTree(7, right=BinaryTree(9)),
                  right=BinaryTree(13, left=BinaryTree(11)))
print(tree.to_dict())

class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if(isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value # 순환방지
        else:
            return super()._traverse(key, value)


root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
# {'value': 10,
#  'left': {'value': 7,
#           'left': None,
#           'right': {'value': 9,
#                     'left': None,
#                     'right': None,
#                     'parent': 7},
#           'parent': 10},
#  'right': None,
#  'parent': None}
print(root.to_dict())

class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent

my_tree = NamedSubTree('footbar', root.left.right)
# {'name': 'footbar',
#  'tree_with_parent': {'value': 9,
#                       'left': None,
#                       'right': None,
#                       'parent': 7
#                       }
# }
print(my_tree.to_dict())

class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())

class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machine = [Machine(**kwargs) for kwargs in machines]

class Switch(ToDictMixin, JsonMixin):
    def __init__(self):
        self.to_dict()

class Machine(ToDictMixin, JsonMixin):
    def __init__(self):
        self.to_dict()
