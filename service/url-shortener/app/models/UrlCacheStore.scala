package models {

    import com.redis.{RedisClient, RedisClientPool}
    import com.typesafe.config.{Config, ConfigFactory}

    object UrlCacheStore
    {
        def forConfig(path: String, config: Config = ConfigFactory.load()): RedisClientPool =
        {
            implicit val cacheStoreConfig = if (path.isEmpty) config else config.getConfig(path)

            val host: String = getSetting("host", {
                case Some(value) => value }
            )
            val port: Int = getSetting("port", {
                case Some(value) => value.toInt
                case _ => 6379
            })
            val maxIdle: Int = getSetting("maxIdle", {
                case Some(value) => value.toInt
                case _ => 0
            })
            val database: Int = getSetting("database", {
                case Some(value) => value.toInt
                case _ => 0
            })
            val secret: Option[String] = getSetting("secret", {
                case value => value
            })

            val timeout: Int = getSetting("timeout", {
                case Some(value) => value.toInt
                case _ => 0
            })

            new RedisClientPool(host, port, maxIdle, database, secret, timeout)
        }

        private def getSetting[T](path: String, convert: PartialFunction[Option[String], T])(implicit c: Config) : T =
        {
            //noinspection SimplifyBooleanMatch
            val value: Option[String] = c.hasPathOrNull(path) match {
                case true =>
                    c.getIsNull(path) match {
                        case false => Some(c.getString(path))
                        case _ => None
                    }
                case _ => None
            }
            if (convert.isDefinedAt(value)) {
                convert(value)
            }
            else throw new IllegalStateException()
        }
    }

}