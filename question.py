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
        required: bool = False,
    ):
        self.key = f"{key}".strip()
        self.text = f"{text}".strip()

        self.datatype = datatype
        self.defaultvalue = defaultvalue
        self.unitlabel = f"{unitlabel}".strip()
        self.explanation = f"{explanation}".strip()

        self.required = required

    def __str__(self):
        s = ""
        if self.key:
            s += self.key
        if self.required:
            s += "*"
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

    def instructions_for_my_datatype(self):
        return Question.instructions_for_datatype(self.datatype)

    @staticmethod
    def instructions_for_datatype(datatype: Any):
        if datatype == str:
            return 'a JSON string (e.g. "foo")'

        elif datatype == int:
            return "an int (e.g. 5)"

        elif datatype == float:
            return "a floating-point decimal value (e.g. 123.45)"

        elif datatype == List[str]:
            return 'a JSON list of strings (e.g. ["foo", "bar", "baz"])'

        elif datatype == List[int]:
            return "a JSON list of integers (e.g. [23, 55, 777])"

        elif datatype == List[float]:
            return "a JSON list of floating-point decimal values (e.g. [23.5, 55.0, 777.777])"

        elif datatype == datetime.date:
            return 'a JSON object indicating the year, month, and day, with all values being integers and negative years indicating BC (e.g. Jan 12, 2015 would be {"year": 2015, "month": 1, "day": 12})'

        elif datatype == datetime.datetime:
            return 'a JSON object indicating the year, month, day, hour, minute, and second, with all values being integers except for seconds which are float (e.g. 4:15:00 PM on Jan 12, 2015 would be {"year": 2015, "month": 1, "day": 12, "hour": 16, "minute": 15, "second": 0.0})'

        elif datatype == datetime.timedelta:
            return 'a JSON object indicating a span of years, months, days, hours, minutes, and seconds, with all values being integers except for seconds which are float (e.g. a difference of 2 years, 3 months, and 6-and-a-half hours would be {"years": 2, "month": 3, "hours": 6, "minutes": 30, "seconds": 0.0})'

        elif type(datatype) == list:
            s = " a JSON string containing exactly one of the following values, written exactly as follows: "
            s += ",".join([f'"{x}"' for x in datatype])
            return s

        else:
            return "unspecified"

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
                required=x.required,
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
                required=x.get("required") or False,
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
        if questions is None:
            return []

        if type(questions) == str or isinstance(questions, Question):
            # We've been given a single instance instead of a collection.
            questions = [questions]

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
