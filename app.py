from flask import Flask, render_template , jsonify, request
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader , DirectoryLoader
from langchain_community.llms.ctransformers import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.hepler import *
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

app = Flask(__name__)


documents = DirectoryLoader(path="Data",loader_cls=PyPDFLoader,glob="*.pdf").load()

text_spliter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)

docs = text_spliter.split_documents(documents)

embedding = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")

doc_search = FAISS.from_documents(documents=docs, embedding= embedding)

llm = CTransformers(model="model/llama-2-7b-chat.ggmlv3.q8_0.bin",
                    model_type="llama",
                    verbose=True,
                    config={'max_new_tokens':128, 'temperature':0.7})

prompt = PromptTemplate(template=template, input_variables=["context","question"])

qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=doc_search.as_retriever(),
                                 chain_type_kwargs={"prompt":prompt},
                                 return_source_documents=True)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        input = request.form['msg']
        print(input)

        result = qa.invoke({"query":input})
        print(f"Result: {result['result']}")

    return jsonify({"response": str(result['result'])})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)