package utils

import play.api.libs.json.{JsObject, Json, OWrites}

object Writes
{
    implicit val ErrorWrites = new OWrites[Error]
    {
        def writes(error: Error): JsObject =
        {
            Json.obj(
                "domain" -> error.domain,
                "reason" -> error.reason,
                "message" -> error.message,
                "location" -> error.location,
                "locationType" -> error.locationType
            )
        }
    }

    implicit val ErrorResponseWrites = new OWrites[ErrorResponse]
    {
        def writes(response: ErrorResponse): JsObject =
        {
            Json.obj("error" ->
                Json.obj("errors" -> response.errors, "code" -> response.status, "message" -> response.message)
            )
        }
    }
}
