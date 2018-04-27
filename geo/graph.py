"""
graph structure
"""
from itertools import chain, combinations
from geo.quadrant import Quadrant
from geo.union import UnionFind
from geo.segment import Segment
from geo.hash import ordered_segments

class Graph:
    """
    create a graph from given set of segments.
    each endpoint is a vertex, each segment an edge.
    """
    def __init__(self, segments):
        self.vertices = dict()
        for segment in segments:
            for point in segment.endpoints:
                if point not in self.vertices:
                    self.vertices[point] = []
                self.vertices[point].append(segment)

    def bounding_quadrant(self):
        """
        return min quadrant containing underlying objects.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.vertices:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """
        svg for tycat.
        """
        edges = (e for (p, edges) in self.vertices.items() for e in edges if e.endpoints[0] == p)
        return "\n".join(c.svg_content() for c in chain(self.vertices.keys(), edges))


    def reconnect(self, hash_points):
        """
        greedily add edges until graph is fully connected.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points:
            C=UnionFind(self.vertices.keys())
            for point in self.vertices.keys():
                for segment in self.vertices[point]:
                    C.union(*segment.endpoints)
            for segment in ordered_segments(self.vertices.keys()):
                p1,p2 = tuple(segment.endpoints)
                if C.find(p1) != C.find(p2):
                    self.vertices[p1].append(segment)
                    self.vertices[p2].append(segment)
                    C.union(p1,p2)
                if C.ranks[C.find(p1)] == C.size - 1:
                    return
        else:
            pass

    def even_degrees(self, hash_points):
        """
        greedily add edges until all degrees are even.
        if hash_points is true then use hashed segments iterator
        else use quadratic segments iterator.
        """
        if hash_points:
            iterator = ordered_segments(self.vertices.keys())
            impairs = 0
            for point in self.vertices.keys():
                if len(self.vertices[point])%2 ==1:
                    impairs += 1
            while impairs:
                segment = next(iterator)
                p1,p2=tuple(segment.endpoints)
                if (len(self.vertices[p1])%2 == 1) and (len(self.vertices[p2])%2 == 1):
                    self.vertices[p1].append(segment)
                    self.vertices[p2].append(segment)
                    impairs -=2
        else:
            pass

    def eulerian_cycle(self):
        """
        return eulerian cycle. precondition: all degrees are even.
        """
        pass
