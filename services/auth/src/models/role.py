import uuid

from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base
from src.models.permission import Permission



role_permissions = Table('role_permissions', Base.metadata,
                         Column('role_id', UUID(as_uuid=True), ForeignKey('role.id', ondelete="CASCADE")),
                         Column('permission_id', UUID(as_uuid=True), ForeignKey('permission.id', ondelete="CASCADE"))
                         )


class Role(Base):
    __tablename__ = 'role'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship("User", secondary="user_roles", back_populates="roles")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return f'<Role {self.name}>'


Permission.roles = relationship("Role", secondary="role_permissions", back_populates="permissions")