from typing import Any, List, Dict, Tuple, Union


class Document:
    def __init__(self, *, id: str = "", description: str = "", body: str = ""):
        self.id = id
        self.description = description
        self.body = body

    def to_gpt_messages(self, systemprompt: str = ""):
        messages = []

        if systemprompt:
            messages.append({"role": "system", "content": systemprompt})

        if self.id:
            # We include the document ID because sometimes the metadata of the document,
            # such as its filename, is actually quite informative.
            messages.append({"role": "user", "content": f"Document ID: {self.id}"})
        if self.description:
            messages.append(
                {"role": "user", "content": f"Document description: {self.description}"}
            )
        if self.body:
            messages.append({"role": "user", "content": f"{self.body}"})
        return messages

    @staticmethod
    def create_from(
        x: Union[
            "Document",
            dict,
            str,
            Tuple[str, str],
            Tuple[str, str, str],
            Tuple[str, str, dict],
            Tuple[str, str, "Document"],
            Tuple[str, dict],
            Tuple[str, "Document"],
        ]
    ):
        if isinstance(x, Document):
            retval = Document(id=x.id, description=x.description, body=x.body)
            return retval

        if type(x) == dict:
            retval = Document(
                id=x.get("id") or "",
                description=x.get("description") or "",
                body=x.get("body") or "",
            )
            return retval

        if type(x) == str:
            retval = Document(body=x)
            return retval

        if type(x) == tuple:
            if len(x) != 2 and len(x) != 3:
                raise ValueError(f"Don't know how to unpack tuple of length {len(x)}")
            retval = Document.create_from(x[-1])
            retval.id = x[0]
            if len(x) > 2:
                retval.description = x[1]
            return retval

    @staticmethod
    def create_collection(
        documents: Union[List[Any], Dict[str, Any]], *, document_description: str = ""
    ):
        if documents is None:
            return []

        if type(documents) == str or isinstance(documents, Document):
            # We've been given a single instance instead of a collection.
            documents = [documents]

        if type(documents) == dict:
            documents = [
                Document.create_from((dockey, docvalue))
                for (dockey, docvalue) in documents.items()
            ]

        charlen = len(f"{len(documents)}")

        retval = []
        for i, doc in enumerate(documents):
            doc = Document.create_from(doc)
            if not doc.id:
                istr = f"{i + 1}".rjust(charlen, "0")
                doc.id = f"document_{istr}"

            if document_description:
                doc.description = document_description

            retval.append(doc)
        return retval
