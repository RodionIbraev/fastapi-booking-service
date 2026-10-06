import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CreatedAtMixin

MIN_SEATS = 1
MAX_SEATS = 5
IDEMPOTENCY_KEY_MAX_LENGTH = 255


class BookingStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


SEAT_HOLDING_STATUSES_SQL = "status IN ('pending', 'confirmed')"


class Booking(CreatedAtMixin, Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint(f"seats BETWEEN {MIN_SEATS} AND {MAX_SEATS}", name="seats_range"),
        CheckConstraint(
            "(status = 'confirmed') = (confirmed_at IS NOT NULL)", name="confirmed_at_matches"
        ),
        CheckConstraint(
            "(status = 'cancelled') = (cancelled_at IS NOT NULL)", name="cancelled_at_matches"
        ),
        CheckConstraint(
            "(status = 'expired') = (expired_at IS NOT NULL)", name="expired_at_matches"
        ),
        UniqueConstraint("user_id", "idempotency_key"),
        Index(
            "ix_bookings_event_id_holding",
            "event_id",
            postgresql_where=text(SEAT_HOLDING_STATUSES_SQL),
            postgresql_include=["status", "seats", "expires_at"],
        ),
        Index(
            "ix_bookings_user_id_event_id_holding",
            "user_id",
            "event_id",
            postgresql_where=text(SEAT_HOLDING_STATUSES_SQL),
        ),
        Index(
            "ix_bookings_expires_at_pending",
            "expires_at",
            postgresql_where=text("status = 'pending'"),
        ),
        Index("ix_bookings_user_id_created_at", "user_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    event_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("events.id", ondelete="RESTRICT"))
    seats: Mapped[int] = mapped_column(SmallInteger)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(
            BookingStatus,
            name="booking_status",
            values_callable=lambda enum: [member.value for member in enum],
        ),
        server_default=BookingStatus.PENDING.value,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    idempotency_key: Mapped[str] = mapped_column(String(IDEMPOTENCY_KEY_MAX_LENGTH))
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
