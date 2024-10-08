from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import FastAPICache
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db
from app.oauth2 import get_current_user
from app.schemas import profburo_vote_schemas
from app.schemas import vote_schemas

router = APIRouter(prefix="/votes", tags=["Оценка кандидата (За/Против/Воздержался)"])


@router.post("/")
async def create_vote(
    vote: vote_schemas.VoteCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(models.Candidate)
        .filter(models.Candidate.id == vote.candidate_id)
        .first()
    )

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Кандидат с ID {vote.candidate_id} не найден.",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.candidate_id == vote.candidate_id,
    )
    founded_vote = vote_query.first()

    if founded_vote is None:
        if vote.type == 1:
            like = (
                db.query(models.Vote)
                .filter(models.Vote.user_id == current_user.id, models.Vote.type == 1)
                .first()
            )

            if like:
                like.candidate_id = vote.candidate_id
                db.commit()
                db.refresh(like)

                await FastAPICache.clear()

                return like

        new_vote = models.Vote(user_id=current_user.id, **vote.dict())
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)

        await FastAPICache.clear()

        return new_vote

    else:
        if vote.type == founded_vote.type:
            db.delete(founded_vote)
            db.commit()

            await FastAPICache.clear()

            return {"message": "Оценка удалена"}

        if vote.type == 1:
            like = (
                db.query(models.Vote)
                .filter(
                    models.Vote.user_id == current_user.id,
                    models.Vote.type == 1,
                    models.Vote.candidate_id != vote.candidate_id,
                )
                .first()
            )

            if like:
                db.delete(founded_vote)
                db.commit()

                like.candidate_id = vote.candidate_id

                db.commit()
                db.refresh(like)

                await FastAPICache.clear()

                return like

        vote_query.update({"type": vote.type}, synchronize_session=False)
        db.commit()
        db.refresh(founded_vote)

        await FastAPICache.clear()

        return founded_vote


@router.post("/profburo")
async def create_vote_profburo(
    profburo_vote: profburo_vote_schemas.ProfburoVoteCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vote_query = db.query(models.ProfburoVote).filter(
        models.ProfburoVote.user_id == current_user.id
    )
    founded_profburo_vote = vote_query.first()

    if founded_profburo_vote is None:
        new_profburo_vote = models.ProfburoVote(
            user_id=current_user.id, type=profburo_vote.type
        )
        db.add(new_profburo_vote)
        db.commit()
        db.refresh(new_profburo_vote)

        await FastAPICache.clear(namespace="users")
        await FastAPICache.clear(namespace="users/me")

        return new_profburo_vote
    else:
        if profburo_vote.type == founded_profburo_vote.type:
            db.delete(founded_profburo_vote)
            db.commit()

            await FastAPICache.clear(namespace="users")
            await FastAPICache.clear(namespace="users/me")

            return {"message": "Оценка удалена"}

        vote_query.update({"type": profburo_vote.type}, synchronize_session=False)
        db.commit()
        db.refresh(founded_profburo_vote)

        await FastAPICache.clear(namespace="users")
        await FastAPICache.clear(namespace="users/me")

        return founded_profburo_vote
