package com.seequest.service {

    import com.redis.RedisClientPool
    import com.typesafe.config.{Config, ConfigFactory, ConfigValue, ConfigValueType}

    import scala.collection.JavaConverters._

    object CacheStore
    {
        def forConfig(path: String, config: Config = ConfigFactory.load()): RedisClientPool =
        {
            implicit val applicationConfig = (if (path.isEmpty) config else config.getConfig(path)) withFallback
                referenceConfig

            val host: String = getSetting("host", {
                case value: String => value
            })

            val port: Int = getSetting("port", {
                case value: Number => value.intValue()
            })

            val maxIdle: Int = getSetting("maxIdle", {
                case value: Number => value.intValue()
            })

            val database: Int = getSetting("database", {
                case value: Number => value.intValue()
            })

            val secret: Option[String] = getSetting("secret", {
                case value if value == null => None
                case value: String => Some(value)
            })

            val timeout: Int = getSetting("timeout", {
                case value: Number => value.intValue()
            })

            new RedisClientPool(host, port, maxIdle, database, secret, timeout)
        }

        private val referenceConfig: Config = ConfigFactory.parseMap(
            Map(
                "host" -> null, "port" -> 6379, "maxIdle" -> 0, "database" -> 0, "secret" -> None, "timeout" -> 0
            ).asJava, "cacheStore defaults"
        )

        private def getSetting[T](path: String, convert: PartialFunction[AnyRef, T])(implicit c: Config) : T =
        {
            val value: ConfigValue = c.getValue(path)
            if (convert.isDefinedAt(value)) {
                convert(value.valueType(), value)
            }
            else throw new IllegalStateException()
        }
    }

}