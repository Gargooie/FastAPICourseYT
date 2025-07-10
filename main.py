
from fastapi import FastAPI
from blog import schemas
import uvicorn

app = FastAPI()


@app.get("/")
def root():
    return "Hello World"

@app.get("/blog")
def say_hello1(limit):
    return f"{limit} of books"

@app.get("/blog/{id}")
def say_hello2(id: int):
    return {"message": id}


@app.post("/blog")
def create_blog(blog: schemas.Blog):
    return {'data': f"blog created with {blog.title}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)