package models {

    import akka.http.scaladsl.model.Uri
    import com.redis._
    import com.seequest.service.CacheStore
    import models.ExtensionMethods._
    import slick.jdbc.PostgresProfile.api._
    import slick.lifted.{ProvenShape, TableQuery}

    import scala.concurrent.{ExecutionContext, Future, Promise}
    import scala.util.Success

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
            catch {case error: Exception => Future.failed(error)}
        }

        def lookup(host: String, id: String)(implicit context: ExecutionContext): Future[Option[UrlRecord]] =
        {
            try {
                this.lookup(host, id.toShortUrlId)
            }
            catch {case error: Exception => Future.failed(error)}
        }

        def lookup(host: String, id: Long)(implicit context: ExecutionContext): Future[Option[UrlRecord]] =
        {
            // Check cache store for longUrl: String value

            val promisedMaybeString = Promise[Option[String]]()

            def get(): Option[String] = cacheStore.withClient { client =>
                client.get(id)
            }

            def set(value: String): Boolean = cacheStore.withClient { client =>
                client.set(id, value)
            }

            for (value: Option[String] <- Future(get())) yield {
                promisedMaybeString success value
            }

            // When the cache check completes:
            // * accept the cached value, if it's present; otherwise
            // * check the UrlShortener database and, if a value's present, add it to the cache store
            // Whatever the case, return the promised result: Some(UrlRecord) or None

            val promisedMaybeRecord = Promise[Option[UrlRecord]]()

            promisedMaybeString.future onComplete {
                case Success(value: Option[String]) if value.isDefined =>
                    promisedMaybeRecord success Some(UrlRecord(host, id, value.get))
                case _ =>
                    for (record: Option[(Long, String)] <- database.run(table.filter(_.id === id).result.headOption))
                        yield {
                            val result: Option[UrlRecord] = record match {
                                case Some((_: Long, value: String)) =>
                                    Future(() => set(value)); Some(UrlRecord(host, id, value))
                                case None => None
                            }
                            promisedMaybeRecord success result
                        }
            }

            promisedMaybeRecord.future
        }

        private lazy val cacheStore: RedisClientPool = CacheStore.forConfig("UrlShortenerService.cacheStore")
        private lazy val database = Database.forConfig("UrlShortenerService.database")
        private val table = TableQuery[UrlTable]

        private val insertStatement = table returning table.map((record: UrlTable) => Tuple2(record.id, record.value))
    }

}
