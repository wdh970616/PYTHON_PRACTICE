from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/statics", StaticFiles(directory="statics"), name="statics")


class Expression(BaseModel):
    expression: str


def calculate(expression: str):
    result = eval(expression)

    # 결과가 정수인지 확인
    if result.is_integer():
        # 정수일 경우 정수로 변환하여 반환
        return str(int(result))
    else:
        # 최대 소수점 10자리로 제한
        formatted_result = f"{result:.10f}"

        # 불필요한 소수점 마지막의 0 제거
        formatted_result = formatted_result.rstrip("0")

        return formatted_result


@app.get("/")
async def get_calculator(request: Request):
    return templates.TemplateResponse("calculator.html", {"request": request})


# 계산 결과를 처리하는 API 엔드포인트
@app.post("/calculate")
async def calculate_expression(expression: Expression):
    result = calculate(expression.expression)
    return {"result": result}
