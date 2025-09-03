# Ref: https://github.com/fastapi-users/fastapi-users/blob/v14.0.1/examples/sqlalchemy/app/app.py
from fastapi import Depends, FastAPI

from app.api.deps import SessionDep
from app.models import User, UserGroup
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/user-groups/{group_id}/users")
async def get_users_by_group(
    group_id: int,
    session: SessionDep,
) -> list[UserRead]:
    group = await session.get(UserGroup, group_id)
    return group.users if group else []
