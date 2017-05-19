package controllers {

    import akka.http.scaladsl.model.Uri
    import akka.http.scaladsl.model.Uri.{Authority, Host, Path}
    import models.Writes._
    import models.{UrlRecord, UrlTable}
    import play.api.libs.concurrent.Execution.Implicits._
    import play.api.libs.json._
    import play.api.mvc.{Action, AnyContent, Controller, Result}
    import utils.Writes._
    import utils.{Error, ErrorResponse}

    import scala.concurrent.Future

    class RestController extends Controller
    {
        def insert: Action[AnyContent] = Action.async { implicit request =>

            request.body.asJson match {
                case message: Some[JsValue] => message.get \ "url" match {
                    case url: JsDefined =>

                        def insert: Future[Result] =
                        {
                            for (urlRecord: UrlRecord <- UrlTable.insert(request.host, url.get.as[JsString].value))
                                yield Created(Json.toJson(urlRecord)).as(JSON)
                        }

                        insert recover { case error: Exception =>
                            InternalServerError(Json.toJson(ErrorResponse(INTERNAL_SERVER_ERROR,
                                s"Could not create shortened url record for ${url.value}",
                                Error(
                                    Error.Domain.Global,
                                    Error.Reason.Invalid,
                                    Error.LocationType.Parameter,
                                    location = "url", message = error.getLocalizedMessage
                                )
                            ))).as(JSON)
                        }
                    case _: JsUndefined =>

                        Future(BadRequest(Json.toJson(ErrorResponse(BAD_REQUEST, s"Missing url argument",
                            Error(
                                Error.Domain.Global,
                                Error.Reason.Required,
                                Error.LocationType.Parameter,
                                location = "url", message = s"a value is required"
                            )
                        ))).as(JSON))
                }
                case None =>

                    Future(BadRequest(Json.toJson(ErrorResponse(BAD_REQUEST, "Expected a JSON message body of the " +
                        "form '{\"url\": \"<long-url>\"}', not " + {
                        request.body.asText match {
                            case text: Some[String] =>
                                text.get.trim match {
                                    case text: String if text.length == 0 =>
                                        "an empty message body"
                                    case text: String if text.length <= 25 =>
                                        s"${JsString(text)}"
                                    case text: String =>
                                        s"${JsString(s"${text.slice(0, 25)}...")}"
                                }
                            case None => "an empty message body"
                        }
                    }, Error(
                        Error.Domain.Global,
                        Error.Reason.Required,
                        Error.LocationType.Parameter,
                        location = "url", message = s"a value is required"
                    )))).as(JSON))
            }
        }

        def lookup(shortUrl: String): Action[AnyContent] = Action.async { implicit request =>

            def lookup: Future[Result] =
            {
                for (urlRecord: Option[UrlRecord] <- UrlTable.lookup(request.host, Uri(shortUrl))) yield {
                    urlRecord.getOrElse(None) match {
                        case None =>
                            NotFound(Json.toJson(ErrorResponse(NOT_FOUND,
                                s"Could not find record of shortened url $shortUrl",
                                Error(
                                    Error.Domain.Global,
                                    Error.Reason.Invalid,
                                    Error.LocationType.Header,
                                    location = "shortUrl", message = "not found"
                                )
                            ))).as(JSON)
                        case urlRecord: UrlRecord => Ok(Json.toJson(urlRecord)).as("application/json")
                    }
                }
            }

            lookup recover { case error: Exception =>
                InternalServerError(Json.toJson(ErrorResponse(INTERNAL_SERVER_ERROR,
                    s"Could not find record of shortened url $shortUrl",
                    Error(
                        Error.Domain.Global,
                        Error.Reason.Invalid,
                        Error.LocationType.Parameter,
                        location = "url", message = error.getLocalizedMessage
                    )
                ))).as(JSON)
            }
        }

        def redirect(id: String): Action[AnyContent] = Action.async { implicit request =>

            def redirect: Future[Result] =
            {
                for (urlRecord: Option[UrlRecord] <- UrlTable.lookup(request.host, id)) yield {
                    urlRecord.getOrElse(None) match {
                        case None =>
                            NotFound(Json.toJson(
                                ErrorResponse(NOT_FOUND, s"Could not find record of shortened url $requestUri",
                                    Error(
                                        Error.Domain.Global,
                                        Error.Reason.Invalid,
                                        Error.LocationType.Header,
                                        location = "shortUrl", message = "not found"
                                    )
                                )
                            )).as(JSON)
                        case urlRecord: UrlRecord => Redirect(urlRecord.value, MOVED_PERMANENTLY)
                    }
                }
            }

            def requestUri: String = s"${if (request.secure) "https" else "http"}://${request.host}${request.uri}"

            redirect recover { case error: Exception =>
                InternalServerError(Json.toJson(ErrorResponse(INTERNAL_SERVER_ERROR,
                    s"Could not find record of shortened url $requestUri",
                    Error(
                        Error.Domain.Global,
                        Error.Reason.Invalid,
                        Error.LocationType.Parameter,
                        location = "url", message = error.getLocalizedMessage
                    )
                ))).as(JSON)
            }
        }
    }

}
