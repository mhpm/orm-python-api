from ariadne import QueryType, MutationType
from werkzeug.security import generate_password_hash
from db import get_db_connection

query = QueryType()
mutation = MutationType()

# Query Resolvers


@query.field("users")
def resolve_users(*_):
    conn = get_db_connection()
    users = conn.execute(
        "SELECT id, first_name, last_name, email, role, avatar FROM users"
    ).fetchall()
    conn.close()
    return [dict(user) for user in users]


@query.field("user")
def resolve_user(*_, user_id):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, first_name, last_name, email, role, avatar FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    if user is None:
        return None
    return dict(user)


# Mutation Resolvers


@mutation.field("createUser")
def resolve_create_user(
    *_, first_name, last_name, email, password, role=None, avatar=None
):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user already exists
    existing_user = cursor.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    if existing_user:
        conn.close()
        raise Exception("User already exists")

    # Hash the password before saving it
    hashed_password = generate_password_hash(password)

    # Insert the new user into the database
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, password, role, avatar) VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, email, hashed_password, role, avatar),
    )
    conn.commit()

    # Get the auto-generated user ID
    user_id = cursor.lastrowid
    conn.close()

    return {
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "role": role,
        "avatar": avatar,
    }


@mutation.field("updateUser")
def resolve_update_user(
    *_,
    user_id,
    first_name=None,
    last_name=None,
    email=None,
    role=None,
    password=None,
    avatar=None
):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash the password if it was provided
    hashed_password = generate_password_hash(password) if password else None

    # Update the user in the database
    cursor.execute(
        """
        UPDATE users
        SET first_name = COALESCE(?, first_name),
            last_name = COALESCE(?, last_name),
            email = COALESCE(?, email),
            role = COALESCE(?, role),
            password = COALESCE(?, password),
            avatar = COALESCE(?, avatar)
        WHERE id = ?
        """,
        (first_name, last_name, email, role, hashed_password, avatar, user_id),
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise Exception("User not found")

    # Fetch the updated user details
    updated_user = cursor.execute(
        "SELECT id, first_name, last_name, email, role, avatar FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()

    return dict(updated_user)


@mutation.field("deleteUser")
def resolve_delete_user(*_, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the user from the database
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise Exception("User not found")

    conn.close()
    return "User deleted successfully"
