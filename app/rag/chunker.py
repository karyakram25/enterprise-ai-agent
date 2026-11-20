from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_into_chunks(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    return splitter.split_text(text)