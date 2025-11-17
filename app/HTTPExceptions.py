from fastapi import HTTPException, status

userAlreadyReg = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь уже зарегистрирован"
)

userNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователь не найден"
)

notRightLoginPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный логин или пароль"
)

tokenAbsent = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Вы не авторизованы, войдите снова"
)

tokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек, войдите снова"
)

tokenAncorrect = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Некорректный токен"
)

DBError = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Ошибка в Базе Данных"
)

postNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пост не найден"
)

chatNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Чат не найден"
)