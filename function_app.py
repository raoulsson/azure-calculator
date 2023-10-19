from __future__ import annotations

import azure.functions as func
import logging

from abc import ABC, abstractmethod
from enum import Enum


class Operator(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

    def __repr__(self):
        return self.value


class Op(ABC):

    @abstractmethod
    def eval(self) -> Op | float:
        pass


class Number(Op):

    def __init__(self, number: float):
        self.__number = number

    def eval(self) -> Op | float:
        return self.__number

    def __repr__(self):
        return str(self.__number)


class Expression(Op):

    def __init__(self, left: Op | None = None, operator: Operator | None = None, right: Op | None = None) -> None:
        self.__left: Op | None = left
        self.__operator: Operator | None = operator
        self.__right: Op | None = right

    def eval(self) -> Op | float:
        if self.__operator == Operator.ADD:
            return self.__left.eval() + self.__right.eval()
        elif self.__operator == Operator.SUBTRACT:
            return self.__left.eval() - self.__right.eval()
        elif self.__operator == Operator.MULTIPLY:
            return self.__left.eval() * self.__right.eval()
        elif self.__operator == Operator.DIVIDE:
            return self.__left.eval() / self.__right.eval()

    def __repr__(self):
        return f'({self.__left} {self.__operator.__repr__()} {self.__right})'


class StringCharTokenizer:

    def __init__(self, s: str):
        self.__s: str = s
        self.__index: int = 0

    def peek(self) -> str:
        if self.__index < len(self.__s):
            return self.__s[self.__index]
        return 'EOF'

    def read(self) -> str:
        if self.__index < len(self.__s):
            ret_val = self.__s[self.__index]
            self.__index += 1
            return ret_val
        return 'EOF'


class ArithmeticStringParser:
    """
    Cannot handle unary plus and minus. Plus other bugs...
    """

    def __init__(self) -> None:
        pass

    def parse(self, input_value: str) -> Op:
        reader = StringCharTokenizer(input_value)
        return self.__parse_expression(reader, 0)

    def __parse_expression(self, reader: StringCharTokenizer, min_precedence: int) -> Op:
        left = self.__parse_term(reader)

        while reader.peek() in "+-" and self.__get_precedence(reader.peek()) >= min_precedence:
            operator = Operator(reader.read())
            next_min_precedence = self.__get_precedence(reader.peek())
            right = self.__parse_expression(reader, next_min_precedence)
            left = Expression(left, operator, right)

        return left

    def __parse_term(self, reader: StringCharTokenizer) -> Op:
        left = self.__parse_factor(reader)

        while reader.peek() in "*/" and self.__get_precedence(reader.peek()) >= 1:
            operator = Operator(reader.read())
            next_min_precedence = self.__get_precedence(reader.peek())
            right = self.__parse_expression(reader, next_min_precedence)
            left = Expression(left, operator, right)

        return left

    def __parse_factor(self, reader: StringCharTokenizer) -> Op:
        if reader.peek() == "(":
            reader.read()
            expression = self.__parse_expression(reader, 0)
            reader.read()
            return expression
        else:
            num = self.__parse_number(reader)
            return num

    def __parse_number(self, reader: StringCharTokenizer) -> Op:
        number = ""
        decimal = False
        while reader.peek().isdigit() or reader.peek() == ".":
            if reader.peek() == ".":
                if decimal:
                    raise Exception("Invalid number")
                decimal = True
            number += reader.read()
        num = Number(float(number))
        return num

    def __get_precedence(self, operator: str) -> int:
        if operator in ("+", "-"):
            return 1
        if operator in ("*", "/"):
            return 2
        return 0


class Calculator:

    def eval(self, input_value: str) -> float:
        expression = ArithmeticStringParser().parse(input_value)
        print(f'Parsed expression: {expression}')
        logging.info(f'Parsed expression: {expression}')
        return expression.eval()

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="calc")
def calc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    calculation = req.params.get('calculation')
    if not calculation:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            calculation = req_body.get('calculation')

    if calculation:
        try:
            calculator = Calculator()
            result = calculator.eval(calculation)
            print("Result: " + str(result))
            logging.info("Result: " + str(result))
            return func.HttpResponse(f"Hello, evaluating: {calculation} = " + str(result))
        except Exception as e:
            return func.HttpResponse(
                f"Exception: {e}",
                status_code=500
            )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a calculation in the query string or in the request body for a personalized response.",
             status_code=200
        )


if __name__ == '__main__':
    calculator = Calculator()
    result = calculator.eval("58+2*3")
    print("Result: " + str(result))
    logging.info("Result: " + str(result))
    result = calculator.eval("(58+2)*3")
    print("Result: " + str(result))
    logging.info("Result: " + str(result))
    result = calculator.eval("58+(2*3)")
    print("Result: " + str(result))
    logging.info("Result: " + str(result))
    result = calculator.eval("(58+2)*(3-1)")
    print("Result: " + str(result))
    logging.info("Result: " + str(result))
    result = calculator.eval("(58.5+2.2)*(3.8-1)")
    print("Result: " + str(result))
    logging.info("Result: " + str(result))