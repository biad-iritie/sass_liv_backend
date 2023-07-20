from typing import List
from sqlalchemy import ForeignKey, Integer, String, Float, VARCHAR
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Type_User(Base):
    __tablename__ = "type_user"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    users: Mapped[List["User"]] = relationship(
        back_populates="type", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    number_rate: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0)
    total_rate: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text('now()'))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=1)
    # role: Mapped["Role"] = relationship(back_populates="users")
    type_user_id: Mapped[int] = mapped_column(ForeignKey("type_user.id"))
    type: Mapped["Type_User"] = relationship(back_populates="users")


class Role(Base):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(String(50), nullable=False)


class Comp_delivery(Base):
    __tablename__ = "comp_delivery"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    address: Mapped[str] = mapped_column(
        VARCHAR(100), nullable=False
    )


class Delivery_type(Base):
    __tablename__ = "delivery_type"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)


class Delivery_statut(Base):
    __tablename__ = "delivery_statut"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    """ users: Mapped[List["User"]] = relationship(
        back_populates="type", cascade="all, delete-orphan") """


class Item_type(Base):
    __tablename__ = "item_type"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)


class Payment_method(Base):
    __tablename__ = "payment_method"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    label: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)


class Mission(Base):
    __tablename__ = "mission"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(
        String(12), nullable=False, unique=True)
    item_weight: Mapped[float] = mapped_column(Float, nullable=False)
    item_price: Mapped[int] = mapped_column(Integer, nullable=False)
    name_sender: Mapped[str] = mapped_column(String(12), nullable=False)
    number_sender: Mapped[str] = mapped_column(String(14), nullable=False)
    district_sender: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    address_sender_description: Mapped[str] = mapped_column(
        VARCHAR(), nullable=False
    )
    name_receiver: Mapped[str] = mapped_column(String(12), nullable=False)
    number_receiver: Mapped[str] = mapped_column(String(14), nullable=False)
    district_receiver: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    address_receiver_description: Mapped[str] = mapped_column(
        VARCHAR(), nullable=False
    )
    delivery_cost: Mapped[int] = mapped_column(Integer, nullable=True)
