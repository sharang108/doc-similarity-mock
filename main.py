import os

from dotenv import load_dotenv
from utils.db_utils import DBUtils
from utils.embedding_utils import EmbeddingUtils
from utils.gdrive_utils import GdriveUtils


# ** Assuming work to be done only with text files **
if __name__ == "__main__":
    load_dotenv()
    file_id = input(
        "Give file id for any text file (if any leave empty if dont want to scan new file)"
    ).strip()
    input_prompt = input("Give prompt").strip()

    drive_utils = GdriveUtils()
    db_utils = DBUtils()
    embedding_utils = EmbeddingUtils(prompt=input_prompt)

    # If file id is empty will print list of all files in the drive with its id
    if file_id:
        file_contents = drive_utils.read_files(file_id=file_id)
        documents = file_contents.strip().splitlines()
        embeddings = embedding_utils.create_embeddings(documents)
        db_utils.insert_embeddings(embeddings)
    else:
        page = 1
        offset = 0
        doc_count = db_utils.get_doc_count()
        limit = min(doc_count, 100)
        sim_threshold = float(os.getenv("DOC_SIMILARITY_THRESHOLD"))
        max_pages = doc_count // limit
        global_result = {"score": 0, "text": ""}
        while page <= max_pages:
            offset = 0 if page == 1 else page * limit
            data = db_utils.get_doc_data(offset=offset, limit=limit)
            page += 1
            max_result = embedding_utils.compare_embeddings(
                embeddings=data, threshold=sim_threshold
            )
            if max_result.get("score") >= sim_threshold:
                print(f"Result: {global_result.get('text')}")
                break
            elif max_result.get("score") > global_result.get("score"):
                global_result = max_result

        print(f"Result: {global_result.get('text')}")
