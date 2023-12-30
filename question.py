from typing import Any, Optional, Union


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
        self.key = key
        self.text = text

        self.datatype = datatype
        self.defaultvalue = defaultvalue
        self.unitlabel = unitlabel
        self.explanation = explanation

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

    @staticmethod
    def create_from(x: Union["Question", dict, (str, str)]):
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
            retval = Question(
                key=x[0],
                text=x[1],
            )
            return retval

        raise TypeError("Unrecognized type passed to Question.create_from")
