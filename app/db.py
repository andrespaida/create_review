from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class Neo4jConnection:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def execute_write(self, query, parameters=None):
        with self.driver.session() as session:
            return session.execute_write(lambda tx: tx.run(query, parameters or {}).data())
