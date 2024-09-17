from fastapi import HTTPException, status

exception_error_data = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Error getting data.",
    headers=None,
)


exception_permit_denied = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Permit denied.",
    headers=None,
)

exception_creation = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Creation error. Try again later.",
    headers=None,
)
