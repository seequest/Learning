package utils {

    case class ErrorResponse(status: Int, message: String, errors: Error*)

}