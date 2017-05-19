name := "url-shortener-service:service-library"
version := "0.0.1"
scalaVersion := "2.11.11"

lazy val GatlingTest = config("gatling") extend Test

libraryDependencies ++= Seq(
    "net.debasishg" %% "redisclient" % "3.4"
)
