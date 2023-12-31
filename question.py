import datetime
import json

from typing import Any, Dict, List, Optional, Tuple, Union


class Question:
    def __init__(
        self,
        text: str = "",
        key: str = "",
        datatype: Optional[Any] = None,
        defaultvalue: Optional[Any] = None,
        unitlabel: str = "",
        explanation: str = "",
    ):
        self.key = f"{key}".strip()
        self.text = f"{text}".strip()

        self.datatype = datatype
        self.defaultvalue = defaultvalue
        self.unitlabel = f"{unitlabel}".strip()
        self.explanation = f"{explanation}".strip()

    def __str__(self):
        s = ""
        if self.key:
            s += self.key
        if self.text:
            if s:
                s = s + ": "
            s += self.text

        sparen = []
        if self.datatype:
            sparen.append(f"{self.datatype}")
        if self.unitlabel:
            sparen.append(self.unitlabel)
        if self.defaultvalue is not None:
            sparen.append(f"default={self.defaultvalue}")
        if len(sparen):
            s += "(" + ", ".join(sparen) + ")"

        if self.explanation:
            if s:
                s += " -- "
            s += self.explanation

        return s

    def coerce_to_my_datatype(self, stringvalue: str):
        if not self.datatype:
            return stringvalue
        return Question.coerce_string_to_datatype(
            stringvalue=stringvalue, datatype=self.datatype
        )

    @staticmethod
    def coerce_string_to_datatype(stringvalue: str, datatype: Any):
        try:
            if datatype == str:
                return stringvalue

            elif datatype == int:
                return int(stringvalue)

            elif datatype == float:
                return float(stringvalue)

            elif datatype == List[str]:
                values = json.loads(stringvalue)
                return [str(x) for x in values]

            elif datatype == List[int]:
                values = json.loads(stringvalue)
                return [int(x) for x in values]

            elif datatype == List[float]:
                values = json.loads(stringvalue)
                return [float(x) for x in values]

            elif datatype == datetime.date:
                raise TypeError("Not implemented yet: date")

            elif datatype == datetime.datetime:
                raise TypeError("Not implemented yet: datetime")

            elif datatype == datetime.timedelta:
                raise TypeError("Not implemented yet: timedelta")

            elif type(datatype) == list:
                if stringvalue in datatype:
                    return stringvalue
                else:
                    return None

        except ValueError:
            return None

    @staticmethod
    def create_from(
        x: Union[
            "Question",
            dict,
            str,
            Tuple[str, str],
            Tuple[str, dict],
            Tuple[str, "Question"],
        ]
    ):
        if isinstance(x, Question):
            retval = Question(
                text=x.text,
                key=x.key,
                datatype=x.datatype,
                defaultvalue=x.defaultvalue,
                unitlabel=x.unitlabel,
                explanation=x.explanation,
            )
            return retval

        if type(x) == dict:
            retval = Question(
                text=x.get("text") or "",
                key=x.get("key") or "",
                datatype=x.get("datatype"),
                defaultvalue=x.get("defaultvalue"),
                unitlabel=x.get("unitlabel") or "",
                explanation=x.get("explanation") or "",
            )
            return retval

        if type(x) == tuple:
            questionkey = x[0]
            questionvalue = x[1]
            if type(questionvalue) == str:
                retval = Question(key=questionkey, text=questionvalue)
                return retval
            else:
                retval = Question.create_from(questionvalue)
                retval.key = questionkey
                return retval

        if type(x) == str:
            key, text = x.split(":", maxsplit=1)
            retval = Question(
                key=key,
                text=text,
            )
            return retval

        raise TypeError("Unrecognized type passed to Question.create_from")

    @staticmethod
    def create_collection(questions: Union[List[Any], Dict[str, Any]]):
        if type(questions) == dict:
            questions = [
                (questionkey, questiontext)
                for (questionkey, questiontext) in questions.items()
            ]

        retval = []
        for i, question in enumerate(questions):
            if type(question) == str:
                question = (f"question_{i + 1}", question)
            qobj = Question.create_from(question)
            retval.append(qobj)
        return retval
