from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from . import schemas, models, hashing
from . database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app=FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"done"}

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog {id} not found")
    # Обновляем атрибуты объекта
    for key, value in request.dict().items():
        setattr(blog, key, value)
    db.commit() 
    return 'updated'
    
@app.get('/blog',response_model=List[schemas.ShowBlog])
def all(db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200,response_model=schemas.ShowBlog)
def show(id, response: Response, db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with id {id} is not found"}
    return blog

@app.post('/user', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    new_user=models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

@app.get('/user/{id}', response_model=schemas.ShowUser)
def get_user(id:int,  db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            
                            detail=f"User {id} is not found.")
    return user