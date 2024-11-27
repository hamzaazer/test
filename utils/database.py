from sqlmodel import Session
from typing import TypeVar, Type, List, Optional
from database import get_session

T = TypeVar('T')

class DatabaseManager:
    @staticmethod
    def get_all(model: Type[T]) -> List[T]:
        session = next(get_session())
        return session.query(model).all()
    
    @staticmethod
    def get_by_id(model: Type[T], id: int) -> Optional[T]:
        session = next(get_session())
        return session.query(model).filter(model.id == id).first()
    
    @staticmethod
    def create(instance: T) -> T:
        session = next(get_session())
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance
    
    @staticmethod
    def update(instance: T) -> T:
        session = next(get_session())
        session.merge(instance)
        session.commit()
        return instance
    
    @staticmethod
    def delete(instance: T) -> None:
        session = next(get_session())
        session.delete(instance)
        session.commit()

    @staticmethod
    def get_session() -> Session:
        return next(get_session())