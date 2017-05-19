package actors {

    import actors.CacheConsistencyActor.{Start, Stop}
    import akka.actor.Actor
    import com.redis.RedisClientPool
    import com.seequest.service.CacheStore
    import com.typesafe.config.Config

    class CacheConsistencyActor() extends Actor
    {
        type Start = CacheConsistencyActor.Start

        override def receive: Receive =
        {
            case Start(config: Config) =>
                this.cacheStore = CacheStore.forConfig("UrlShortenerService.cacheStore")

            case Stop() =>
                context.stop(self)
        }

        private var cacheStore: RedisClientPool = _
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
