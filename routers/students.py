from fastapi import (
    HTTPException,
    Depends,
    APIRouter
)   
from sqlalchemy.orm import Session, joinedload
from typing import List
from sqlalchemy.exc import IntegrityError


from models import (
    User, 
    Student,
    Course
    )
from schemas import (
    StudentRegisterSchema,
    SetCourseRequest,
    StudentResponse,
    LevelUpdate,
    CurrencyUpdate,
    XPUpdate
)

from db_helpher import get_db

router = APIRouter(prefix="/students")

@router.get("/alt")
def students_page_alt(
    db: Session = Depends(get_db)
):
    users = db.query(Student).options(joinedload(Student.user)).all()
    
    return users


@router.post("/register")
def students_register(
    student: StudentRegisterSchema,
    db: Session = Depends(get_db)
):
    
    user = db.query(User).filter(User.id == student.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db_student = Student(user_id=student.user_id)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        return {"message": "Student registered successfully", "student_id": db_student.id}
    
    except IntegrityError as e:
        db.rollback()
        return {"message": "This user is already a student"}
    
    
    

# Эндпоинт для установки курса студенту
@router.post("/{student_id}/set-course")
def set_student_course(
    student_id: int, 
    request: SetCourseRequest, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    course = db.query(Course).filter(Course.id == request.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    student.current_course_id = request.course_id  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Course set successfully", "student": student}




# Эндпоинты для управления студентами
@router.get("/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).options(joinedload(Student.user)).all()
    return students

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).options(joinedload(Student.user)).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}/xp")
def update_student_xp(
    student_id: int, 
    xp_data: XPUpdate, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.xp = xp_data.xp #type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student XP updated successfully", "student": student}

@router.put("/{student_id}/level")
def update_student_level(
    student_id: int, 
    level_data: LevelUpdate, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.lvl = level_data.level #type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student level updated successfully", "student": student}





@router.put("/{student_id}/currency")
def update_student_currency(
    student_id: int, 
    currency_data: CurrencyUpdate, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.currency = currency_data.currency #type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student currency updated successfully", "student": student}







# Эндпоинты для управления опытом, уровнем и валютой студентов
@router.post("/{student_id}/add-xp/{xp_amount}")
def add_student_xp(student_id: int, xp_amount: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.xp += xp_amount  # type: ignore
    
    # Автоматическое повышение уровня (например, каждые 100 опыта)
    if student.xp >= student.lvl * 100:  # type: ignore
        student.lvl += 1  # type: ignore
    
    db.commit()
    db.refresh(student)
    
    return {"message": f"Added {xp_amount} XP to student", "student": student}

@router.post("/{student_id}/remove-xp/{xp_amount}")
def remove_student_xp(student_id: int, xp_amount: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.xp = max(0, student.xp - xp_amount)  # type: ignore
    
    # Автоматическое понижение уровня (если опыт меньше необходимого для текущего уровня)
    if student.xp < (student.lvl - 1) * 100:  # type: ignore
        student.lvl = max(1, student.lvl - 1)  # type: ignore
    
    db.commit()
    db.refresh(student)
    
    return {"message": f"Removed {xp_amount} XP from student", "student": student}

@router.post("/{student_id}/add-currency/{currency_amount}")
def add_student_currency(student_id: int, currency_amount: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.currency += currency_amount  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": f"Added {currency_amount} currency to student", "student": student}

@router.post("/{student_id}/remove-currency/{currency_amount}")
def remove_student_currency(student_id: int, currency_amount: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.currency = max(0, student.currency - currency_amount)  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": f"Removed {currency_amount} currency from student", "student": student}

@router.post("/{student_id}/level-up")
def level_up_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.lvl += 1  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student leveled up", "student": student}

@router.post("/{student_id}/level-down")
def level_down_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.lvl = max(1, student.lvl - 1)  # type: ignore
    db.commit()
    db.refresh(student)
    
    return {"message": "Student leveled down", "student": student}

# Эндпоинт для получения валюты по user_id
@router.get("/user/{user_id}/currency")
def get_student_currency_by_user_id(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == user_id).first()
    
    if not student:
        return {"currency": 0}
    
    return {"currency": student.currency}

# Эндпоинт для получения полной информации о студенте по user_id
@router.get("/user/{user_id}")
def get_student_by_user_id(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).options(joinedload(Student.user)).filter(Student.user_id == user_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student

# Эндпоинт для получения опыта по user_id
@router.get("/user/{user_id}/xp")
def get_student_xp_by_user_id(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == user_id).first()
    
    if not student:
        return {"xp": 0}
    
    return {"xp": student.xp}

# Эндпоинт для получения уровня по user_id
@router.get("/user/{user_id}/level")
def get_student_level_by_user_id(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == user_id).first()
    
    if not student:
        return {"level": 0}
    
    return {"level": student.lvl}
