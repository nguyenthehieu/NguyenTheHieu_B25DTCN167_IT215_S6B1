from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()
courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

class Course(BaseModel):
    code: str
    name: str
    duration: int
    fee: int

@app.get("/courses")
def get_course(
    keyword: str = None,
    min_fee: int = Query(default=2000000),
    max_fee: int = Query(default=4000000)
):
    result = courses

    if keyword:
        result = []
        for c in courses:
            if keyword.lower() in c["name"].lower() or keyword.lower() in c["code"].lower():
                result.append(c)

    if min_fee is not None:
        filtered = []
        for c in result:
            if c["fee"] >= min_fee:
                filtered.append(c)
        result = filtered

    if max_fee is not None:
        filtered = []
        for c in result:
            if c["fee"] <= max_fee:
                filtered.append(c)
        result = filtered

    return {
        "message": "Lấy danh sách khóa học thành công",
        "data": result
    }

@app.get("/courses/{course_id}")
def get_detail_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return {
                "message": "Lấy chi tiết khóa học thành công",
                "data": course
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )

@app.post("/courses")
def add_course(course: Course):
    if course.name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Tên không được rỗng"
        )

    if course.duration <= 0:
        raise HTTPException(
            status_code=409,
            detail="Duration phải lớn hơn 0"
        )

    if course.fee < 0:
        raise HTTPException(
            status_code=409,
            detail="Phí phải lớn hơn hoặc bằng 0"
        )

    for c in courses:
        if c["code"] == course.code:
            raise HTTPException(
                status_code=409,
                detail="Code đã tồn tại"
            )

    new_id = max([c["id"] for c in courses], default=0) + 1

    new_course = {
        "id": new_id,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    courses.append(new_course)

    return {
        "message": "Thêm khóa học thành công",
        "data": new_course
    }


@app.put("/courses/{course_id}")
def update_course(course_id: int, updated_course: Course):
    for index, course in enumerate(courses):
        if course["id"] == course_id:

            if updated_course.name.strip() == "":
                raise HTTPException(
                    status_code=400,
                    detail="Tên không được rỗng"
                )

            if updated_course.duration <= 0:
                raise HTTPException(
                    status_code=409,
                    detail="Duration phải lớn hơn 0"
                )

            if updated_course.fee < 0:
                raise HTTPException(
                    status_code=409,
                    detail="Phí phải lớn hơn hoặc bằng 0"
                )

            for c in courses:
                if c["code"] == updated_course.code and c["id"] != course_id:
                    raise HTTPException(
                        status_code=409,
                        detail="Khóa học đã tồn tại"
                    )

            courses[index] = {
                "id": course_id,
                "code": updated_course.code,
                "name": updated_course.name,
                "duration": updated_course.duration,
                "fee": updated_course.fee
            }

            return {
                "message": "Cập nhật khóa học thành công",
                "data": courses[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy khóa học"
    )

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for c in courses:
        if c["id"] == course_id:
            courses.remove(c)
            return {
                "message": "Đã xóa thành công",
                "data": c
            }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy khóa học"
    )