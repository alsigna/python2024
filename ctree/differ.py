from .abstract import ConfigTree

__all__ = ("ConfigTreeDiffer",)


class ConfigTreeDiffer:
    @classmethod
    def _diff_list(cls, a: ConfigTree, b: ConfigTree, negative: bool = False) -> list[ConfigTree]:
        result = []
        for child in a.children.values():
            if child.line not in b.children:
                node = child.copy(children=not negative)
                result.append(node)
                if negative:
                    while len(node.children) != 0:
                        node = list(node.children.values())[0]
                    new_line = f"{node.UNDO} {node.line}"
                    if new_line in node.parent.children:
                        del node.parent.children[node.line]
                    else:
                        node.parent.children[new_line] = node
                        node.line = new_line
            else:
                nested_result = cls._diff_list(child, b.children.get(child.line), negative)
                result.extend(nested_result)
        return result

    # @classmethod
    # def _delete_node(cls, tree: ConfigTree, raw_line: str) -> None:
    #     tree.children = [child for child in tree.children if not child.raw_line.startswith(raw_line)]

    @classmethod
    def _post_remove_doubled_undo(cls, tree: ConfigTree) -> None:
        processed_children = {}
        for child in tree.children.values():
            if child.children:
                cls._post_remove_doubled_undo(child)
            if child.line.startswith(f"{child.UNDO} {child.UNDO}"):
                new_line = child.line.replace(f"{child.UNDO} {child.UNDO}", "").strip()
                if new_line not in child.parent.children:
                    processed_children[new_line] = child
                    child.line = new_line
            elif child.line not in processed_children:
                processed_children[child.line] = child
        tree.children = processed_children

    @classmethod
    def _post_sort(cls, tree: ConfigTree) -> None:
        for child in tree.children.values():
            if child.children:
                cls._post_sort(child)
        tree.children = dict(sorted(tree.children.items(), key=lambda item: len(item[1].children)))

    @classmethod
    def diff(cls, a: ConfigTree, b: ConfigTree) -> ConfigTree:
        if a.__class__ != b.__class__:
            raise TypeError("сравнивать можно только конфигурации одного производителя")

        root = a.__class__()

        diff_list = cls._diff_list(a, b, negative=True)
        for leaf in diff_list:
            root.merge(leaf)

        diff_list = cls._diff_list(b, a, negative=False)
        for leaf in diff_list:
            root.merge(leaf)

        cls._post_remove_doubled_undo(root)
        cls._post_sort(root)
        return root
