from fastapi import (
    HTTPException,
    Depends,
    Request,
    APIRouter
)
from sqlalchemy.orm import Session, joinedload
from typing import List
from templates import templates


from models import (
    Course,
    TestAnswerOption,
    TestQuestion
    )
from schemas.testing import (
    TestQuestionSchema,
    TestAnswerOptionSchema,
    TestSubmissionSchema,
    TestRecommendationResponse,
    TestAnswerCreate,
    TestQuestionCreate,
    TestQuestionUpdate,
    TestAnswerUpdate
)



from utils.db_helpher import get_db


router = APIRouter(prefix="/test", tags=["Test"])

@router.get("/questions", response_model=List[TestQuestionSchema])
def get_test_questions(db: Session = Depends(get_db)):
    """Получить все вопросы теста с вариантами ответов"""
    questions = db.query(TestQuestion).options(
        joinedload(TestQuestion.answer_options)
    ).order_by(TestQuestion.order).all()
    
    return questions

@router.post("/submit", response_model=TestRecommendationResponse)
def submit_test_answers(
    submission: TestSubmissionSchema,
    db: Session = Depends(get_db)
):
    """Обработать ответы теста и вернуть рекомендацию"""
    creative_total = 0
    analytical_total = 0
    
    # Получаем все ответы из базы для проверки
    all_answers = {}
    for answer in db.query(TestAnswerOption).all():
        all_answers[answer.id] = {
            "creative": answer.creative_value,
            "analytical": answer.analytical_value
        }
    
    # Суммируем баллы за выбранные ответы
    for answer in submission.answers:
        if answer.answer_id in all_answers:
            creative_total += all_answers[answer.answer_id]["creative"]
            analytical_total += all_answers[answer.answer_id]["analytical"]
    
    # Определяем рекомендованный курс
    if creative_total >= 5:
        recommended_course = "Веб-разработка"
    elif analytical_total >= 5:
        recommended_course = "Аналитика данных"
    else:
        recommended_course = "Основы программирования"
    
    return TestRecommendationResponse(
        creative_score=creative_total,
        analytical_score=analytical_total,
        recommended_course=recommended_course
    )

@router.get("/", name="test")
def test_page(request: Request, db: Session = Depends(get_db)):
    """Страница с тестом"""
    questions = db.query(TestQuestion).options( #type: ignore
        joinedload(TestQuestion.answer_options) #type: ignore
    ).order_by(TestQuestion.order).all() #type: ignore
    
    return templates.TemplateResponse(
        request=request,
        name="test.html",
        context={"request": request, "questions": questions}
    )





# Эндпоинты для вопросов
@router.post("/questions", response_model=TestQuestionSchema)
def create_question(question: TestQuestionCreate, db: Session = Depends(get_db)):
    db_question = TestQuestion(
        text=question.text,
        order=question.order
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/questions", response_model=List[TestQuestionSchema])
def get_all_questions(db: Session = Depends(get_db)):
    questions = db.query(TestQuestion).order_by(TestQuestion.order).all()
    return questions

@router.get("/questions/{question_id}", response_model=TestQuestionSchema)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/questions/{question_id}", response_model=TestQuestionSchema)
def update_question(question_id: int, question_data: TestQuestionUpdate, db: Session = Depends(get_db)):
    db_question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_question.text = question_data.text #type: ignore
    db_question.order = question_data.order #type: ignore
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Удаляем связанные ответы
    db.query(TestAnswerOption).filter(TestAnswerOption.question_id == question_id).delete()
    
    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}

# Эндпоинты для ответов
@router.post("/api/test/answers", response_model=TestAnswerOptionSchema)
def create_answer_option(answer: TestAnswerCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли вопрос
    question = db.query(TestQuestion).filter(TestQuestion.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_answer = TestAnswerOption(
        question_id=answer.question_id,
        answer_text=answer.answer_text,
        creative_value=answer.creative_value,
        analytical_value=answer.analytical_value
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

@router.get("/api/test/questions/{question_id}/answers", response_model=List[TestAnswerOptionSchema])
def get_question_answers(question_id: int, db: Session = Depends(get_db)):
    # Проверяем, существует ли вопрос
    question = db.query(TestQuestion).filter(TestQuestion.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    answers = db.query(TestAnswerOption).filter(TestAnswerOption.question_id == question_id).all()
    return answers

@router.put("/api/test/answers/{answer_id}", response_model=TestAnswerOptionSchema)
def update_answer_option(answer_id: int, answer_data: TestAnswerUpdate, db: Session = Depends(get_db)):
    db_answer = db.query(TestAnswerOption).filter(TestAnswerOption.id == answer_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer option not found")
    
    db_answer.answer_text = answer_data.answer_text #type: ignore
    db_answer.creative_value = answer_data.creative_value #type: ignore
    db_answer.analytical_value = answer_data.analytical_value #type: ignore
    
    db.commit()
    db.refresh(db_answer)
    return db_answer

@router.delete("/api/test/answers/{answer_id}")
def delete_answer_option(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(TestAnswerOption).filter(TestAnswerOption.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer option not found")
    
    db.delete(answer)
    db.commit()
    return {"message": "Answer option deleted successfully"}


@router.get("/test/result")
def test_result_page(
    request: Request,
    creative_score: int,
    analytical_score: int,
    db: Session = Depends(get_db)
):
    """Страница с результатами теста"""
    # Получаем все курсы из базы данных
    all_courses = db.query(Course).all()
    
    # Детерминированная логика выбора курса на основе баллов
    if creative_score >= 7 and analytical_score >= 7:
        # Универсальный талант - курс полного цикла
        recommended_course = db.query(Course).filter(Course.id == 4).first()  
    elif creative_score >= 7:
        # Творческий тип - фронтенд или дизайн
        recommended_course = db.query(Course).filter(Course.id == 5).first()  
    elif analytical_score >= 7:
        # Аналитический тип - бэкенд или данные
         recommended_course = db.query(Course).filter(Course.id == 3).first()  
    elif creative_score >= 5 and analytical_score >= 5:
        # Сбалансированный профиль - универсальный курс
        recommended_course = db.query(Course).filter(Course.id == 2).first()  
    elif creative_score > analytical_score:
        # Склонность к творчеству
        recommended_course = db.query(Course).filter(Course.id == 2).first()  
    elif analytical_score > creative_score:
        # Склонность к аналитике
        recommended_course = db.query(Course).filter(Course.id == 6).first()  
    else:
        # Нейтральный результат - базовый курс
        recommended_course = db.query(Course).filter(Course.id == 1).first()  
    
    
    recommended_course = db.query(Course).filter(Course.id == 3).first()   # Формируем список других курсов (исключая рекомендованный)
    other_courses = [c for c in all_courses if c.id != recommended_course.id] # type: ignore
    
    # Ограничиваем количество отображаемых курсов до 3
    other_courses = other_courses[:3]
    
    return templates.TemplateResponse(
        request=request,
        name="test_result.html",
        context={
            "request": request,
            "creative_score": creative_score,
            "analytical_score": analytical_score,
            "recommended_course": recommended_course,
            "other_courses": other_courses
        }
    )