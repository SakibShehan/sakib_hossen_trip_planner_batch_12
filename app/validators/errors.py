class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return {"error": "VALIDATION_ERROR", "message": error.message}, 400

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        return {"error": "NOT_FOUND", "message": error.message}, 404

    @app.errorhandler(ConflictError)
    def handle_conflict_error(error):
        return {"error": error.code, "message": error.message}, 409

    @app.errorhandler(404)
    def handle_unknown_url(error):
        return {"error": "NOT_FOUND", "message": "The requested URL was not found."}, 404

    @app.errorhandler(405)
    def handle_wrong_method(error):
        return {"error": "METHOD_NOT_ALLOWED", "message": "This method is not allowed for this URL."}, 405