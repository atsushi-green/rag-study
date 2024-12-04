from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# ドキュメントの読み込み
loader1 = PyPDFLoader("database/屋久島.pdf")
loader2 = PyPDFLoader("database/小笠原諸島.pdf")
raw_doc_yakushima = loader1.load()
raw_doc_ogasawara = loader2.load()
print(len(raw_doc_yakushima), len(raw_doc_ogasawara))
raw_docs = raw_doc_yakushima + raw_doc_ogasawara
print(len(raw_docs))

# Document transformer（テキストデータの加工）
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs = text_splitter.split_documents(raw_docs)
print(len(docs))

# embeddingの作成（ベクトル化）
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma.from_documents(docs, embeddings)

# 検索
retriever = db.as_retriever()
query = "屋久島は鹿児島県にありますか？"
# query = "小笠原諸島は東京都にありますか？"

context_docs = retriever.invoke(query)  # コサイン類似度で検索
print(f"len = {len(context_docs)}")

first_doc = context_docs[0]
print(f"metadata = {first_doc.metadata}")
print(first_doc.page_content)
