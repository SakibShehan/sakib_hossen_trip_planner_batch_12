from werkzeug.exceptions import HTTPException

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

        # any other HTTP error becomes JSON 
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return {
            "error": error.name.upper().replace(" ", "_"),
            "message": error.description,
        }, error.code

    #  any unexpected error becomes a JSON 500
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception(error)
        return {
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
        }, 500