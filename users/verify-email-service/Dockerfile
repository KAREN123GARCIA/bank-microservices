# Etapa 1: Build del proyecto con Maven
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app

# Copiar los archivos del proyecto
COPY pom.xml .
COPY src ./src

# Copiar también el archivo de credenciales
COPY src/main/resources/credentials/credentials.json ./src/main/resources/credentials/credentials.json

# Compilar sin tests
RUN mvn clean package -DskipTests

# Etapa 2: Imagen final para ejecutar el microservicio
FROM eclipse-temurin:17
WORKDIR /app

# Copiar el jar generado
COPY --from=build /app/target/*.jar app.jar

# Exponer el puerto
EXPOSE 8084

# Comando para iniciar la aplicación
ENTRYPOINT ["java", "-jar", "app.jar"]
