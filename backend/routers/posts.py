from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/api/places/{place_id}/posts",
    tags=["posts"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@router.get("", response_model=schemas.PaginatedPosts)
def list_posts(
    place_id: int,
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    db: Session = Depends(get_db)
):
    # 장소 존재 여부 확인
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 장소입니다.")

    query = db.query(models.Post).filter(models.Post.place_id == place_id)
    total = query.count()
    items = query.order_by(models.Post.created_at.desc(), models.Post.id.desc()).offset((page - 1) * size).limit(size).all()

    return schemas.PaginatedPosts(
        items=items,
        total=total,
        page=page,
        size=size
    )


@router.get("/{post_id}", response_model=schemas.PostDetail)
def get_post(
    place_id: int,
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(
        models.Post.id == post_id,
        models.Post.place_id == place_id
    ).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")
    return post


@router.post("", response_model=schemas.PostDetail, status_code=status.HTTP_201_CREATED)
def create_post(
    place_id: int,
    post_in: schemas.PostCreate,
    db: Session = Depends(get_db)
):
    # 장소 존재 여부 확인
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 장소입니다.")

    # 4자리 숫자 문자열 검증 (400 Bad Request)
    if len(post_in.password) != 4 or not post_in.password.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호는 정확히 4자리 숫자 문자열이어야 합니다.")

    hashed_pw = get_password_hash(post_in.password)
    db_post = models.Post(
        place_id=place_id,
        nickname=post_in.nickname or "익명",
        password=hashed_pw,
        title=post_in.title,
        content=post_in.content
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.put("/{post_id}", response_model=schemas.PostDetail)
def update_post(
    place_id: int,
    post_id: int,
    post_in: schemas.PostUpdate,
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(
        models.Post.id == post_id,
        models.Post.place_id == place_id
    ).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")

    # 비밀번호 대조 (403 Forbidden)
    if not verify_password(post_in.password, post.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="비밀번호가 일치하지 않습니다.")

    post.title = post_in.title
    post.content = post_in.content
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    place_id: int,
    post_id: int,
    post_in: schemas.PostDelete,
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(
        models.Post.id == post_id,
        models.Post.place_id == place_id
    ).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="게시글을 찾을 수 없습니다.")

    # 비밀번호 대조 (403 Forbidden)
    if not verify_password(post_in.password, post.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="비밀번호가 일치하지 않습니다.")

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
