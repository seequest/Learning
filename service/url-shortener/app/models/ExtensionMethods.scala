package models {

    import java.nio.ByteBuffer
    import java.util.Base64

    import akka.http.scaladsl.model.Uri
    import play.api.libs.json.JsString

    object ExtensionMethods
    {

        implicit class StringAdditions(self: String)
        {
            def toShortUrlId: Long =
            {
                try {
                    ByteBuffer.wrap(decoder.decode(self).reverse.padTo(8, 0.toByte).reverse).getLong()
                }
                catch {
                    case _: Exception =>
                        throw new IllegalArgumentException(s"Expected short URL, not ${JsString(self)}")
                }
            }

            private val decoder = Base64.getUrlDecoder
        }

        implicit class UriAdditions(self: Uri)
        {
            def toShortUrlId: Long =
            {
                val path = self.path

                val id = path.length match {
                    case 1 if !path.startsWithSlash =>
                        path.head
                    case 2 =>
                        if (path.startsWithSlash) {
                            path.tail
                        }
                        else {
                            path.head
                        }
                    case 3 if path.startsWithSlash =>
                        path.tail.head
                    case _ =>
                        throw new IllegalArgumentException(s"Expected short URL, not ${JsString(self.toString)}")
                }

                id.toString.toShortUrlId
            }
        }

    }

}
