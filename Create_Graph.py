import json
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

# 连接数据库
graph = Graph("http://localhost:7474", auth=("neo4j", "123456789"),name="neo4j")

# graph.delete_all()
matcher_node = NodeMatcher(graph)
matcher_relation = RelationshipMatcher(graph)

with open("baseline_all_kg_triples.txt", "r", encoding="utf-8") as file:
    # i = 0
    for line in file.readlines():
        # i = i + 1
        # if i % 10000 == 0:
            # print(i)
        entity_1, entity_2, relation = line.split("\t")
        # print(entity_1,"",entity_2,"",relation)
        node_1 = matcher_node.match(name=entity_1).first()
        if node_1 is None:
            node_1 = Node(name=entity_1)
            graph.create(node_1)

        # relation为第二个节点的label
        node_2 = matcher_node.match(name=entity_2).first()
        if node_2 is None:
            node_2 = Node(relation, name=entity_2)
            graph.create(node_2)
        if not node_2.has_label(relation):
            # print(i)
            node_2.add_label(relation)
            graph.push(node_2)

        r = Relationship(node_1, relation, node_2)
        graph.create(r)