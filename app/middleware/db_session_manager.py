from sqlalchemy.orm import scoping


class DBSessionManager:
    def __init__(self, db_session):
        self._db_session = db_session

    def process_request(self, req, resp, resource=None):
        req.context['session'] = self._db_session

    def process_response(self, req, resp, resource=None, req_succeeded=True):
        session = self._db_session

        if isinstance(session, scoping.ScopedSession):
            session.remove()
        else:
            session.close()
