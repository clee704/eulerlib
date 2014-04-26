from abc import ABCMeta, abstractmethod, abstractproperty


class PriorityQueue(metaclass=ABCMeta):

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def add(self, item):
        """Add *item* to the queue."""

    @abstractmethod
    def pop(self):
        """Remove and return the minimum item in the queue."""

    @abstractmethod
    def peek(self):
        """Return the minimum item in the queue."""

    @abstractmethod
    def decrease_key(self, old_item, new_item):
        """Replace *old_item* with *new_item*, where *new_item* < *old_item*.
        """


# Original code by Kevin O'Connor,
# augmented by Tim Peters and Raymond Hettinger,
# modified by Choongmin Lee to add decrease_key() opereation.
#
# See the Python source code of heapq module in the standard library
# for the original code.
class BinaryHeap(PriorityQueue):

    def __init__(self):
        self._items = []
        self._indexes_by_item = {}

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._indexes_by_item

    def add(self, item):
        if item in self._indexes_by_item:
            return
        items = self._items
        items.append(item)
        self._sift_up(0, len(items) - 1)

    def pop(self):
        items = self._items
        if not items:
            raise KeyError('pop from an empty heap')
        last_item = items.pop()
        if items:
            item = items[0]
            items[0] = last_item
            self._sift_down(0)
        else:
            item = last_item
        del self._indexes_by_item[item]
        return item

    def peek(self):
        items = self._items
        if not items:
            raise KeyError('peek from an empty heap')
        return items[0]

    def decrease_key(self, old_item, new_item):
        indexes_by_item = self._indexes_by_item
        if old_item not in indexes_by_item:
            raise KeyError('{0} not in a heap'.format(old_item))
        if new_item in indexes_by_item:
            raise KeyError('{0} in a heap'.format(new_item))
        if old_item <= new_item:
            raise ValueError('{0} <= {1}'.format(old_item, new_item))
        i = indexes_by_item.pop(old_item)
        self._items[i] = new_item
        self._sift_up(0, i)

    def _sift_up(self, start, i):
        items = self._items
        indexes_by_item = self._indexes_by_item
        item = items[i]
        while start < i:
            p = (i - 1) >> 1
            parent = items[p]
            if item < parent:
                items[i] = parent
                indexes_by_item[parent] = i
                i = p
            else:
                break
        items[i] = item
        indexes_by_item[item] = i

    def _sift_down(self, i):
        items = self._items
        indexes_by_item = self._indexes_by_item
        end = len(items)
        start = i
        item = items[i]
        c = 2 * i + 1
        while c < end:
            r = c + 1
            child = items[c]
            if r < end:
                right_child = items[r]
                if right_child < child:
                    c = r
                    child = right_child
            items[i] = child
            indexes_by_item[child] = i
            i = c
            c = 2 * i + 1
        items[i] = item
        indexes_by_item[item] = i
        self._sift_up(start, i)


class FibonacciHeap(PriorityQueue):

    def __init__(self):
        self._len = 0
        self._min = None
        self._trees_by_item = {}

    def __len__(self):
        return self._len

    def __contains__(self, item):
        return item in self._trees_by_item

    def add(self, item):
        trees_by_item = self._trees_by_item
        if item in trees_by_item:
            return
        t = FibonacciTree(item)
        self._add_tree(t)
        self._len += 1
        trees_by_item[item] = t

    def pop(self):
        min = self._min
        if min is None:
            raise KeyError('pop from an empty heap')
        item = min.item
        child = min.child
        min.child = None
        self._delete_tree(min)
        if child is not None:
            start = child
            while 1:
                next = child.right
                child.parent = None
                self._add_tree(child)
                if next is start:
                    break
                child = next
        if self._min is not None:
            self._consolidate_trees()
        self._len -= 1
        del self._trees_by_item[item]
        return item

    def peek(self):
        min = self._min
        if min is None:
            raise KeyError('peek from an empty heap')
        return min.item

    def decrease_key(self, old_item, new_item):
        trees_by_item = self._trees_by_item
        if old_item not in trees_by_item:
            raise KeyError('{0} not in a heap'.format(old_item))
        if new_item in trees_by_item:
            raise KeyError('{0} in a heap'.format(new_item))
        if old_item <= new_item:
            raise ValueError('{0} <= {1}'.format(old_item, new_item))
        current = trees_by_item.pop(old_item)
        current.item = new_item
        trees_by_item[new_item] = current
        parent = current.parent
        if parent is not None and new_item < parent.item:
            while parent is not None:
                child = parent.child
                if child.right is child:
                    parent.child = None
                else:
                    while child is not current:
                        child = child.right
                    child.right.left = child.left
                    child.left.right = child.right
                    if parent.child is child:
                        parent.child = child.right
                parent.degree -= 1
                current.parent = None
                current.marked = False
                self._add_tree(current)
                current = parent
                parent = parent.parent
                if not current.marked:
                    break
            if parent is not None:
                current.marked = True
        if parent is None and new_item < self._min.item:
            self._min = current

    def _add_tree(self, tree):
        min = self._min
        if min is None:
            tree.right = tree
            tree.left = tree
            self._min = tree
        else:
            tree.right = min
            tree.left = min.left
            min.left.right = tree
            min.left = tree
            if tree.item < min.item:
                self._min = tree

    def _delete_tree(self, tree):
        if tree.right is tree:
            self._min = None
        else:
            tree.right.left = tree.left
            tree.left.right = tree.right
            if self._min is tree:
                self._min = self._update_min(tree.right)

    def _update_min(self, start):
        min = start
        current = start.right
        while current is not start:
            if current.item < min.item:
                min = current
            current = current.right
        return min

    def _consolidate_trees(self):
        trees_by_degree = {}
        start = self._min
        end = start.left
        current = start
        while 1:
            d = current.degree
            next = current.right
            if d not in trees_by_degree:
                trees_by_degree[d] = current
            else:
                merged = current
                while d in trees_by_degree:
                    t1 = merged
                    t2 = trees_by_degree[d]
                    if t2.item < t1.item:
                        t1, t2 = t2, t1
                    self._delete_tree(t2)
                    child = t1.child
                    if child is None:
                        t1.child = t2
                        t2.right = t2
                        t2.left = t2
                    else:
                        t2.right = child
                        t2.left = child.left
                        child.left.right = t2
                        child.left = t2
                    t1.degree += 1
                    t2.parent = t1
                    merged = t1
                    del trees_by_degree[d]
                    d = merged.degree
                trees_by_degree[d] = merged
            if current is end:
                break
            current = next


class FibonacciTree(object):

    def __init__(self, item):
        self.item = item
        self.parent = None
        self.right = None
        self.left = None
        self.child = None
        self.degree = 0
        self.marked = False


class WeightedGraph(metaclass=ABCMeta):

    @abstractproperty
    def nodes(self):
        "Get all nodes in the graph."

    @abstractproperty
    def edges(self):
        "Get all edges in the graph."

    @abstractmethod
    def add(self, e, w=1):
        "Add an edge e = (u, v) with weight w to the graph."

    @abstractmethod
    def weight(self, e):
        "Return the weight of the edge e = (u, v)."


class DirectedGraph(WeightedGraph):

    @abstractmethod
    def next_nodes(self, u):
        "Return all nodes that are directly connected by edges starting at u."

    @abstractmethod
    def prev_nodes(self, u):
        "Return all nodes that are directly connected by edges ending at u."

    def topological_sort(self):
        prev_nodes = self.prev_nodes
        visit = self._visit
        lst = []
        visited = set()
        for u in self.nodes:
            if not prev_nodes(u):
                visit(u, visited, lst)
        lst.reverse()
        return lst

    def _visit(self, u, visited, lst):
        visit = self._visit
        if u not in visited:
            visited.add(u)
            for v in self.next_nodes(u):
                visit(v, visited, lst)
            lst.append(u)

    def dijkstra(self, queue, *initial_nodes):
        next_nodes = self.next_nodes
        weight = self.weight
        dist = dict((u, 0) for u in initial_nodes)
        prev = dict((u, None) for u in initial_nodes)
        for u in initial_nodes:
            queue.add((0, u))
        while queue:
            d, u = queue.pop()
            for v in next_nodes(u):
                alt = d + weight((u, v))
                if v not in dist:
                    queue.add((alt, v))
                elif alt < dist[v]:
                    queue.decrease_key((dist[v], v), (alt, v))
                else:
                    continue
                dist[v] = alt
                prev[v] = u
        return dist, prev


class UndirectedGraph(WeightedGraph):

    @abstractmethod
    def adjacent_nodes(self, u):
        "Return all nodes that are directly connected with u."

    def minimum_spanning_tree(self, queue):
        nodes = self.nodes
        weight = self.weight
        adjacent_nodes = self.adjacent_nodes
        inf = float('inf')
        weights = dict((u, inf) for u in nodes)
        weights[next(iter(nodes))] = 0
        connected_nodes = {}
        for u, w in weights.items():
            queue.add((w, u))
        while queue:
            _, u = queue.pop()
            del weights[u]
            for v in adjacent_nodes(u):
                if v not in weights:
                    continue
                else:
                    w1 = weights[v]
                    w2 = weight((u, v))
                    if w2 < w1:
                        queue.decrease_key((w1, v), (w2, v))
                        weights[v] = w2
                        connected_nodes[v] = u
        return connected_nodes.items()


class AdjacencyListDigraph(DirectedGraph):

    def __init__(self):
        self._nodes = set()
        self._next_nodes = {}
        self._prev_nodes = {}
        self._weights = {}

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._weights.keys()

    def add(self, e, w=1):
        nodes = self._nodes
        u, v = e
        nodes.add(u)
        nodes.add(v)
        self._add(u, v, self._next_nodes)
        self._add(v, u, self._prev_nodes)
        self._weights[e] = w

    def weight(self, e):
        return self._weights[e]

    def next_nodes(self, u):
        next_nodes = self._next_nodes
        return next_nodes[u] if u in next_nodes else []

    def prev_nodes(self, u):
        prev_nodes = self._prev_nodes
        return prev_nodes[u] if u in prev_nodes else []

    def _add(self, u, v, lists):
        neighbors = lists.setdefault(u, [])
        if v not in neighbors:
            neighbors.append(v)


class AdjacencyListGraph(UndirectedGraph):

    def __init__(self):
        self._nodes = set()
        self._adjacent_nodes = {}
        self._weights = {}

    @property
    def nodes(self):
        return self._nodes

    @property
    def edges(self):
        return self._weights.keys()

    def add(self, e, w=1):
        nodes = self._nodes
        u, v = e
        nodes.add(u)
        nodes.add(v)
        self._add(u, v)
        self._add(v, u)
        self._weights[e if id(u) < id(v) else (v, u)] = w

    def weight(self, e):
        if id(e[0]) > id(e[1]):
            e = (e[1], e[0])
        return self._weights[e]

    def adjacent_nodes(self, u):
        adjacent_nodes = self._adjacent_nodes
        return adjacent_nodes[u] if u in adjacent_nodes else []

    def _add(self, u, v):
        neighbors = self._adjacent_nodes.setdefault(u, [])
        if v not in neighbors:
            neighbors.append(v)
