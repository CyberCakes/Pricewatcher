from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from app.database import get_db
from app.models import User
from app.config import settings

security = HTTPBearer()


async def get_current_user(
		credentials: HTTPAuthorizationCredentials = Depends(security),
		db: AsyncSession = Depends(get_db)
) -> User:
	token = credentials.credentials
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
		user_id: int = payload.get("sub")
		if user_id is None:
			raise HTTPException(status_code=401, detail="Invalid token")
	except JWTError:
		raise HTTPException(status_code=401, detail="Invalid token")

	result = await db.execute(select(User).where(User.id == user_id))
	user = result.scalar_one_or_none()
	if not user or not user.is_active:
		raise HTTPException(status_code=401, detail="User not found or inactive")
	return user