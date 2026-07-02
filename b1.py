from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

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

@app.get('/courses')
def get_course(
    keyword: str = None,
    min_fee: int = Field(default=2000000),
    max_fee: int = Field(default=4000000)
):
    result = courses
    if keyword:
        result = []
        for c in courses:
            if keyword.lower() in c['name'].lower() or keyword.lower() in c['code'].lower():
                result.append(c)
    
    if min_fee is not None:
        flag = []
        for c in result:
            if c['fee'] >= min_fee:
                flag.append(c)

        result = flag
    
    if max_fee is not None:
        for c in result:
            if c['fee'] >= max_fee:
                flag.append(c)

        result = flag
            

@app.get('/courses/{course_id}')
def get_detail_course(course_id:int):
    print("giá trị id nhận về ",course_id)
    for course in courses :
        if course["id"] == course_id:
            return {
                "message" : "lấy chi tiết sinh viên thành công !",
                "data" : course 
            }
    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )

@app.post('/courses')
def add_course(course:Course):
    if course.name == "":
        raise HTTPException(
            status_code=400,
           detail="Tên không được rỗng")

    if course.duration <= 0:
        raise HTTPException(
            status_code=409,
            detail="Ngày nghỉ phải lớn hơn 0")

    if course.fee < 0:
        raise HTTPException(
            status_code=409,
            detail="Phí phải lớn hơn hoặc bằng 0")

    for c in courses:
        if c["code"] == course.code:
            raise HTTPException(
                status_code=409,        
                detail="Code đã tồn tại")

    new_course = {
        "id": courses[-1]['id']+1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    courses.append(new_course)
    return new_course

@app.put("/courses/{course_id}")
def update_course(course_id: int, updated_course: Course):
    for index, course in enumerate(courses):
        if course["id"] == course_id:
            for c in courses:
                if c["code"] == updated_course.code and c["id"] != course_id:
                    raise HTTPException(
                        status_code=409,
                        detail="KHoá học đã tồn tại"
                    )

            courses[index] = {
                "id": course_id,
                "code": updated_course.code,
                "name": updated_course.name,
                "duration": updated_course.duration,
                "fee": updated_course.fee
            }

            return courses[index]

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy khoá học"
    )

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for c in courses:
        if c["id"] == course_id:
            courses.remove(c)
            return {
                "message": "Đã xoá thành công",
                "course": c
            }

    raise HTTPException(
        status_code=404,
        detail="KHồn tìm thấy khoá học"
    )