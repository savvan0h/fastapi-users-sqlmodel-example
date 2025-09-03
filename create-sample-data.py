import asyncio

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import async_session_maker, get_user_db
from app.models import UserGroup
from app.schemas import UserCreate
from app.users import UserManager


async def create_sample_groups(session: AsyncSession) -> dict[str, UserGroup]:
    """Create sample user groups."""
    groups_data = ["Admin", "Developer", "Guest"]

    created_groups = {}

    for group_name in groups_data:
        # Check if group already exists
        existing_group = (
            await session.exec(select(UserGroup).where(UserGroup.name == group_name))
        ).first()

        if existing_group:
            print(f"Group '{group_name}' already exists")
            created_groups[group_name] = existing_group
        else:
            group = UserGroup(name=group_name)
            session.add(group)
            await session.flush()
            created_groups[group_name] = group
            print(f"Created group: {group_name}")

    await session.commit()
    return created_groups


async def create_sample_users(
    session: AsyncSession, groups: dict[str, UserGroup]
) -> None:
    """Create sample users."""
    users_data = [
        {
            "email": "admin@example.com",
            "password": "admin123",
            "group": "Admin",
            "is_superuser": True,
        },
        {"email": "dev1@example.com", "password": "dev123", "group": "Developer"},
        {"email": "dev2@example.com", "password": "dev456", "group": "Developer"},
        {"email": "guest1@example.com", "password": "guest123", "group": "Guest"},
        {"email": "guest2@example.com", "password": "guest456", "group": "Guest"},
        {"email": "guest3@example.com", "password": "guest789", "group": "Guest"},
    ]

    user_db = await anext(get_user_db(session))
    user_manager = UserManager(user_db)

    for user_data in users_data:
        try:
            # Check if user already exists
            existing_user = await user_manager.get_by_email(user_data["email"])
            if existing_user:
                print(f"User '{user_data['email']}' already exists")
                continue
        except Exception:
            # User doesn't exist, create new one
            pass

        try:
            # Create user
            user_create = UserCreate(
                email=user_data["email"],
                password=user_data["password"],
                is_superuser=user_data.get("is_superuser", False),
            )

            user = await user_manager.create(user_create)

            # Assign group
            group = groups.get(user_data["group"])
            if group:
                user.group = group
                session.add(user)
                await session.commit()

            print(f"Created user: {user_data['email']} (group: {user_data['group']})")

        except Exception as e:
            print(f"Failed to create user {user_data['email']}: {e}")
            await session.rollback()


async def main():
    """Main function."""
    print("Creating sample data...")

    async with async_session_maker() as session:
        try:
            # Create groups
            print("\n=== Creating Groups ===")
            groups = await create_sample_groups(session)

            # Create users
            print("\n=== Creating Users ===")
            await create_sample_users(session, groups)

            print("\n✅ Sample data created successfully!")

        except Exception as e:
            print(f"❌ Error: {e}")
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(main())
