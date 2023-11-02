import boto3
import json
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
import numpy as np
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

bedrock = boto3.client(service_name='bedrock-runtime')

# create the Titan embeddings model
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)

def sample_pdf_ingestion(save_loc):
    loader = PyPDFDirectoryLoader("./data/")

    documents = loader.load()
    # - in our testing Character split works better with this PDF data set
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 1000,
        chunk_overlap  = 100,
    )
    docs = text_splitter.split_documents(documents)

    avg_doc_length = lambda documents: sum([len(doc.page_content) for doc in documents])//len(documents)
    avg_char_count_pre = avg_doc_length(documents)
    avg_char_count_post = avg_doc_length(docs)
    print(f'Average length among {len(documents)} documents loaded is {avg_char_count_pre} characters.')
    print(f'After the split we have {len(docs)} documents, more than the original {len(documents)}.')
    print(f'Average length among {len(docs)} documents (after split) is {avg_char_count_post} characters.')

    sample_embedding = np.array(bedrock_embeddings.embed_query(docs[0].page_content))
    print("Sample embedding of a document chunk: ", sample_embedding)
    print("Size of the embedding: ", sample_embedding.shape)

    vectorstore_faiss = FAISS.from_documents(
        docs,
        bedrock_embeddings,
    )

    vectorstore_faiss.save_local(save_loc)


def main() -> None:
    # save vector store to local index folder named below
    sample_pdf_ingestion("local_index_test")

if __name__ == "__main__":
    main()
