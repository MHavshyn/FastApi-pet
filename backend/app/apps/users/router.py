from fastapi import APIRouter, status

from apps.users.schemas import RegisterUserSchema, RegisteredUserSchema

router_users = APIRouter()


@router_users.post("/create", status_code=status.HTTP_201_CREATED)
def create_users(new_uses: RegisterUserSchema) -> RegisteredUserSchema:
    created_user = RegisteredUserSchema(id=123, **new_uses.model_dump())
    return created_user

