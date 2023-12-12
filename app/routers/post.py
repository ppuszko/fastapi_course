from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import  List, Optional 
from sqlalchemy import func


#creates an insatnce of APIRouter, which allows to split path methods in many files, so i dont have to 
#store all the code of PATH operations in main file. Prefix parameter allows me to set a prefix path to all my methods, since
#all of them are tied to operations on posts, the prefix to any of these operations will be /posts. 
#tags parameter groups all post-tied operations to Posts group - this element allows me to make more clear documentation in 
#fastAPI /docs panel
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
   #posts = db.query(models.Posts, func.count(models.Vote.post_id).label(
        #"votes")).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(
            models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    
   # print(results)
    # a way to get only posts published by actually logged in user is to change from:
    # posts = db.query(models.Posts).all() to  posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
    #there are few methods of filtering the result, like limit, filter, etc and for the filter method, i can set 
    #a phrase in URL, then the filter method will check if any of my posts contains(phrase) in it's parameter
    # (which i have to specify as i did above) however i cant have spaces in URL, so to overcome this trouble, i need to 
    #input %20 in URL, which is equivlent of space
    return results
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)  
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)) : 
    
    
    new_post = models.Posts(owner_id = current_user.id, **post.dict()) #**post.dict() convert Post class object to dictionary, and unpacks it, so it;s not necessary to assign every value 
    #in constructor of new_post object
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model = schemas.PostOut) 
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   # post = db.query(models.Posts).filter(models.Posts.id == id).first()
    post = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found") #czystsza forma zapisu tego, co wykomentowalem ponizej, wymaga importu 
                                                                        #HTTPException z fastapi
        #response.status_code = status.HTTP_404_NOT_FOUND - w tym przypadku jako argument funkcji trzeba tez podac zmienna response: Response
        #return {"message":f"post with id: {id} was not found"}
    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) #dzialanie DELETE z zasady nie może nic zwrócić, bo jego zadaniem jest pozbycie sie tresci
                                                            #więc klasyczny return nie zadziala, zamiast tego nalezy uzyc Response(status.code)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title=%s, content=%s, published = %s WHERE id=%s RETURNING *""",( post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query =  db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
   
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
   
    return post