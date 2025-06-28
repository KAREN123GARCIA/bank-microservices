FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app

# Copiamos primero los archivos importantes para cacheo de dependencias
COPY pom.xml .
COPY src ./src

# Compilar el proyecto sin correr los tests
RUN mvn clean package -DskipTests

FROM eclipse-temurin:17
WORKDIR /app

# Copiar el jar compilado desde la etapa anterior
COPY --from=build /app/target/*.jar app.jar

# Exponer el puerto del servicio
EXPOSE 8084

# Ejecutar el jar
ENTRYPOINT ["java", "-jar", "app.jar"]
