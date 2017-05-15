import sbt.Keys._

lazy val GatlingTest = config("gatling") extend Test

scalaVersion := "2.11.11"

libraryDependencies ++= Seq(

    "com.netaporter" %% "scala-uri" % "0.4.14",
    "com.typesafe.akka" %% "akka-http" % "10.0.2",
    "com.typesafe.slick" %% "slick" % "3.2.0",
    "com.typesafe.slick" %% "slick-hikaricp" % "3.2.0",
    "com.zaxxer" % "HikariCP" % "2.6.1",
    "net.codingwell" %% "scala-guice" % "4.1.0",
    "net.debasishg" %% "redisclient" % "3.4",
    "org.postgresql" % "postgresql" % "9.3-1100-jdbc4",
    "org.slf4j" % "slf4j-nop" % "1.6.4",

    "io.gatling" % "gatling-test-framework" % "2.2.2" % Test,
    "io.gatling.highcharts" % "gatling-charts-highcharts" % "2.2.2" % Test,
    "org.scalatestplus.play" %% "scalatestplus-play" % "2.0.0" % Test
)

// The Play project itself
lazy val root = (project in file("."))
  .enablePlugins(Common, PlayScala, GatlingPlugin)
  .configs(GatlingTest)
  .settings(inConfig(GatlingTest)(Defaults.testSettings): _*)
  .settings(
    name := """url-shortener""",
    scalaSource in GatlingTest := baseDirectory.value / "/gatling/simulation"
  )

// Documentation for this project:
//    sbt "project docs" "~ paradox"
//    open docs/target/paradox/site/index.html
lazy val docs = (project in file("docs")).enablePlugins(ParadoxPlugin).
  settings(
    paradoxProperties += ("download_url" -> "https://example.lightbend.com/v1/download/play-rest-api")
  )
