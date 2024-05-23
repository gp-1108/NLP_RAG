# Import necessary modules
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import argparse

def main(dataset_path, faiss_path, embedding_model):
    # Load documents from the specified directory
    loader = DirectoryLoader(
        path=dataset_path,
        glob="*.txt",
        use_multithreading=True,
        loader_cls=TextLoader
    )

    # Load all text files from the directory
    data = loader.load()

    # Initialize the text splitter with specified chunk size and overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=20
    )

    # Split the loaded documents into chunks
    docs = text_splitter.split_documents(data)

    # Initialize the embeddings model with the specified or default model
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

    # Create a FAISS vector store from the document chunks and embeddings
    db = FAISS.from_documents(docs, embeddings)

    # Example query to demonstrate similarity search
    query = "What happened in 1946?"
    query_res = db.similarity_search(query)

    # Print the result of the query
    print(f"Query: {query}\nQuery result: {query_res[0].page_content}")

    # Save the FAISS index to the specified path
    db.save_local(faiss_path)

    # Now we will load the saved FAISS index and perform the same query
    # to make sure that the loaded FAISS index works as expected

    # Load the FAISS index from the saved path
    new_db = FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)

    # Perform the same query on the loaded FAISS index
    query_res = new_db.similarity_search(query)

    # Print the result of the query from the loaded FAISS index
    print(f"Query: {query}\nQuery result: {query_res[0].page_content}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Create and save a FAISS index from a dataset.')
    parser.add_argument('dataset_path', type=str, help='Path to the dataset directory containing text files.')
    parser.add_argument('faiss_path', type=str, help='Path to save the FAISS index.')
    parser.add_argument('--embedding_model', type=str, default='sentence-transformers/all-MiniLM-L6-v2',
                        help='Name of the HuggingFace embedding model to use (default: sentence-transformers/all-MiniLM-L6-v2)')

    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.dataset_path, args.faiss_path, args.embedding_model)
