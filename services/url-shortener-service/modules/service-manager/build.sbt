name := "url-shortener-service:service-manager"
version := "0.0.1"
scalaVersion := "2.11.11"

libraryDependencies ++= Seq(

    "com.netaporter" %% "scala-uri" % "[0.4,)",
    "com.typesafe.slick" %% "slick" % "[3.2,)",
    "com.typesafe.slick" %% "slick-hikaricp" % "[3.2,)",
    "net.codingwell" %% "scala-guice" % "[4.1,)",
    "net.debasishg"  %% "redisclient" % "[3.4,3.5)",
    "org.postgresql" % "postgresql" % "[42.1,)",

    "io.gatling" % "gatling-test-framework" % "[2.2,)" % Test,
    "io.gatling.highcharts" % "gatling-charts-highcharts" % "[2.2,)" % Test,
    "org.scalatestplus.play" %% "scalatestplus-play" % "[2.0,)" % Test

)

// Play project configuration

enablePlugins(Common, PlayScala, GatlingPlugin)
val modules = file("..")

lazy val root = Project("service-manager", file("."), aggregate = Seq(RootProject(file("docs"))),
    dependencies = Seq(RootProject(modules / "service-library"))
)
    .configs(GatlingTest)
    .settings(inConfig(GatlingTest)(Defaults.testSettings): _*)
    .settings(scalaSource in GatlingTest := baseDirectory.value / "/gatling/simulation")

lazy val GatlingTest = config("gatling") extend Test
