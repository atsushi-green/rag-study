# neo4j 上でナレッジグラフを構築する
# https://qiita.com/ksonoda/items/98a6607f31d0bbb237ef を参照。

from os import environ

from google.cloud import aiplatform
from ipyvis.graphwidget import GraphWidget
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_google_vertexai import VertexAI
from langchain_text_splitters import CharacterTextSplitter
from neo4j import GraphDatabase

# .env に記載されている環境変数を読み込む
project_id = environ["project_id"]
location = environ["location"]
model_id = environ["model_id"]
aiplatform.init(project=project_id, location=location)
vertex_ai_llm = VertexAI(model_name=model_id)  # Replace with your specific model


# ドキュメントの読み込み
loader1 = PyPDFLoader("database/屋久島.pdf")
loader2 = PyPDFLoader("database/種子島.pdf")
raw_doc_yakushima = loader1.load()
raw_doc_tanegashima = loader2.load()
print(f"屋久島のページ数: {len(raw_doc_yakushima)}")
print(f"種子島のページ数: {len(raw_doc_tanegashima)}")
raw_docs = raw_doc_yakushima + raw_doc_tanegashima
print(f"合計のページ数: {len(raw_docs)}")
assert len(raw_doc_yakushima) + len(raw_doc_tanegashima) == len(raw_docs)

# Document transformer（テキストデータの加工）
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=200)
docs = text_splitter.split_documents(raw_docs)


llm_transformer = LLMGraphTransformer(llm=vertex_ai_llm)

graph = Neo4jGraph()


graph_documents = llm_transformer.convert_to_graph_documents(docs)
# 抽出されたノードやエッジを1つ確認
print(graph_documents[0].nodes)
print(graph_documents[0].relationships)

graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)

default_cypher = "MATCH (s)-[r:!MENTIONS]->(t) RETURN s,r,t LIMIT 1000"


def showGraph(cypher: str = default_cypher):
    driver = GraphDatabase.driver(
        uri=environ["NEO4J_URI"],
        auth=(environ["NEO4J_USERNAME"], environ["NEO4J_PASSWORD"]),
    )
    session = driver.session()
    widget = GraphWidget(graph=session.run(cypher).graph())
    widget.node_label_mapping = "id"
    return widget


showGraph()
