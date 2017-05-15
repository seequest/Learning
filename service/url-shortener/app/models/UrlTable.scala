package models {

    import akka.http.scaladsl.model.Uri
    import models.ExtensionMethods._
    import slick.jdbc.PostgresProfile.api._
    import slick.lifted.{ProvenShape, TableQuery}

    import scala.concurrent.{ExecutionContext, Future}

    class UrlTable(tag: Tag) extends Table[(Long, String)](tag, "url")
    {
        override def * : ProvenShape[(Long, String)] = (id, value)

        def id: Rep[Long] = column[Long]("id", O.AutoInc, O.PrimaryKey)

        def value: Rep[String] = column[String]("value", O.Unique, O.SqlType("text"))
    }

    object UrlTable
    {
        def insert(host: String, url: String)(implicit context: ExecutionContext): Future[UrlRecord] =
        {
            val normalized_url = Uri.normalize(url)

            for ((id: Long, value: String) <- database.run(insertStatement += Tuple2(0L, normalized_url))) yield {
                UrlRecord(host, id, value)
            }
        }

        def lookup(host: String, shortUrl: Uri)(implicit context: ExecutionContext): Future[Option[UrlRecord]] =
        {
            try {
                this.lookup(host, shortUrl.toShortUrlId)
            }
            catch {
                case error: Exception => Future.failed(error)
            }
        }

        def lookup(host: String, id: String)(implicit context: ExecutionContext): Future[Option[UrlRecord]] =
        {
            try {
                this.lookup(host, id.toShortUrlId)
            }
            catch {
                case error: Exception => Future.failed(error)
            }
        }

        def lookup(host: String, id: Long)(implicit context: ExecutionContext): Future[Option[UrlRecord]] =
        {
            for (record: Option[(Long, String)] <- database.run(table.filter(_.id === id).result.headOption)) yield {
                record.getOrElse(None) match {
                    case record: Tuple2[_, _] =>
                        Some(UrlRecord(host, id = record._1.asInstanceOf[Long], value = record._2.asInstanceOf[String]))
                    case None => None
                }
            }
        }

        private lazy val database = Database.forConfig("UrlShortener.database")
        private val table = TableQuery[UrlTable]
        private val insertStatement = table returning table.map((record: UrlTable) => Tuple2(record.id, record.value))
    }

}
