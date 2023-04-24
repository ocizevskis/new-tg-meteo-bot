val scala3Version = "3.2.2"

lazy val root = project
  .in(file("."))
  .settings(
    name := "tests",
    version := "0.1.0-SNAPSHOT",

    scalaVersion := scala3Version,

    libraryDependencies += "org.scalameta" %% "munit" % "0.7.29" % Test,
    libraryDependencies += "com.lihaoyi" %% "requests" % "0.8.0",
    libraryDependencies += "org.json4s" %% "json4s-jackson" % "4.0.6",
    libraryDependencies += "org.xerial" % "sqlite-jdbc" % "3.27.2.1"

  )
