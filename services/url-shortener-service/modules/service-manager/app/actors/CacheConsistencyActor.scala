package actors {

    import actors.CacheConsistencyActor.{Start, Stop}
    import akka.actor.Actor
    import com.redis.RedisClientPool
    import com.seequest.service.CacheStore
    import com.typesafe.config.Config
    import slick.jdbc.PostgresProfile.api._

    class CacheConsistencyActor() extends Actor
    {
        type Start = CacheConsistencyActor.Start

        override def receive: Receive =
        {
            case Start(config: Config) =>
                this.start()

            case Stop() =>
                this.stop()
        }

        // region Privates

        private var cacheStore: RedisClientPool = _
        private var database: Database = _

        private def start(): Unit =
        {
            this.cacheStore = CacheStore.forConfig("UrlShortenerService.cacheStore")
            this.database = Database.forConfig("UrlShortenerService.database")
        }

        private def stop(): Unit =
        {
            context.stop(self)  // guarantees that no further messages are processed
            this.database.close
            this.cacheStore.close
        }

        // endregion
    }

    object CacheConsistencyActor
    {

        class Operation

        case class Start(config: Config)
            extends Operation

        case class Stop()
            extends Operation

    }

}
