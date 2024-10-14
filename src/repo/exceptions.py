from sqlalchemy.exc import IntegrityError


class RepositoryError(Exception):
    ...


class IntegrityConflictError(Exception):
    ...


class NotFoundError(Exception):
    ...