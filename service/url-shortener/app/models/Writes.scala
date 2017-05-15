package models {

    import java.nio.ByteBuffer
    import java.util.Base64

    import play.api.libs.json.{JsObject, Json, OWrites}

    object Writes
    {
        implicit val UrlRecordWrites = new OWrites[UrlRecord]
        {
            def writes(urlRecord: UrlRecord): JsObject =
            {
                Json.obj("id" -> this.encode(urlRecord.host, urlRecord.id), "url" -> urlRecord.value)
            }

            private def encode(host: String, id: Long): String =
            {
                val buffer = ByteBuffer.allocate(8).putLong(id).array()
                val start = buffer.indexWhere(byte => byte != 0)
                val stem = encoder.encodeToString(buffer.slice(start, buffer.length))

                s"http://$host/$stem"
            }

            private val encoder = Base64.getUrlEncoder.withoutPadding
        }
    }

}
