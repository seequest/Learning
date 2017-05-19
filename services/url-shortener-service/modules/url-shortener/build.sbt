name := "url-shortener-service:url-shortener"
version := "0.0.1"
scalaVersion := "2.11.11"

libraryDependencies ++= Seq(

    "com.netaporter" %% "scala-uri" % "[0.4,)",
    "com.typesafe.akka" %% "akka-http" % "[10.0,)",
    "com.typesafe.slick" %% "slick" % "[3.2,)",
    "com.typesafe.slick" %% "slick-hikaricp" % "[3.2,)",
    "com.zaxxer" % "HikariCP" % "[2.6,)",
    "net.codingwell" %% "scala-guice" % "[4.1,)",
    "net.debasishg" %% "redisclient" % "[3.4,)",
    "org.postgresql" % "postgresql" % "[42.1,)",
    "org.slf4j" % "slf4j-nop" % "[1.6,)",

    "io.gatling" % "gatling-test-framework" % "[2.2,)" % Test,
    "io.gatling.highcharts" % "gatling-charts-highcharts" % "[2.2,)" % Test,
    "org.scalatestplus.play" %% "scalatestplus-play" % "[2.0,)" % Test

)

// Play project configuration

enablePlugins(Common, PlayScala, GatlingPlugin)
val modules = file("..")

lazy val root = Project("url-shortener", file("."), aggregate = Seq(RootProject(file("docs"))),
    dependencies = Seq(RootProject(modules / "service-library"))
)
    .configs(GatlingTest)
    .settings(inConfig(GatlingTest)(Defaults.testSettings): _*)
    .settings(scalaSource in GatlingTest := baseDirectory.value / "/gatling/simulation")

lazy val GatlingTest = config("gatling") extend Test
